#!/usr/bin/env python3
"""
cast_chart.py — Cast a horary chart for a given moment and location.

Uses pyswisseph (Swiss Ephemeris) for planetary positions and house cusps.
Supports any location (lat/lon) and any timezone offset.

USAGE:
    # As a script:
    python cast_chart.py --datetime "2026-04-24 20:29:30" --tz 0 \\
        --location "London" --lat 51.5074 --lon -0.1278 \\
        --question "Your question here"

    # As a module:
    from cast_chart import cast
    chart = cast(year=2026, month=4, day=24, hour=20, minute=29, second=30,
                 tz_offset=0, lat=51.5074, lon=-0.1278,
                 location="London", question="Your question")
    print(chart["report"])

DEPENDENCIES:
    pip install pyswisseph

DESIGN NOTE:
    Local civil time is the natural input — the astrologer asks "when did
    I understand the question?" and that answer comes in their local clock.
    Internally we convert to UTC for the ephemeris call, but the input is
    local-time-friendly. Remember to account for DST where it applies.
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass, field, asdict
from typing import Optional

try:
    import swisseph as swe
except ImportError:
    raise SystemExit(
        "pyswisseph not installed. Run: pip install pyswisseph"
    )

SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]

TRADITIONAL_RULERS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
    "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
    "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
    "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter",
}

# Day rulers: 0 = Monday ... 6 = Sunday
DAY_RULERS = {0: "Moon", 1: "Mars", 2: "Mercury", 3: "Jupiter",
              4: "Venus", 5: "Saturn", 6: "Sun"}

# Chaldean order for planetary hours
CHALDEAN_ORDER = ["Saturn", "Jupiter", "Mars", "Sun",
                  "Venus", "Mercury", "Moon"]

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
}


def deg_to_sign(longitude: float):
    """Convert ecliptic longitude (0-360) to (sign, degree, minute)."""
    sign_idx = int(longitude / 30) % 12
    deg_in_sign = longitude - sign_idx * 30
    d = int(deg_in_sign)
    m = int(round((deg_in_sign - d) * 60))
    if m == 60:
        m = 0
        d += 1
    return SIGNS[sign_idx], d, m


def planetary_hour(jd_ut: float, lat: float, lon: float, weekday: int) -> str:
    """
    Compute the planetary hour lord at a given moment.

    weekday: 0 = Monday ... 6 = Sunday (Python's weekday())
    """
    geopos = (lon, lat, 0.0)
    sunrise = swe.rise_trans(jd_ut - 1.0, swe.SUN, swe.CALC_RISE,
                             geopos, 0.0, 0.0, swe.FLG_SWIEPH)
    sunset = swe.rise_trans(jd_ut - 1.0, swe.SUN, swe.CALC_SET,
                            geopos, 0.0, 0.0, swe.FLG_SWIEPH)
    next_sunrise = swe.rise_trans(jd_ut, swe.SUN, swe.CALC_RISE,
                                  geopos, 0.0, 0.0, swe.FLG_SWIEPH)

    sunrise_jd = sunrise[1][0]
    sunset_jd = sunset[1][0]
    next_sunrise_jd = next_sunrise[1][0]

    is_day = sunrise_jd <= jd_ut < sunset_jd
    if is_day:
        elapsed = jd_ut - sunrise_jd
        hour_length = (sunset_jd - sunrise_jd) / 12
        ref_weekday = weekday
    else:
        if jd_ut >= sunset_jd:
            elapsed = jd_ut - sunset_jd
            hour_length = (next_sunrise_jd - sunset_jd) / 12
            ref_weekday = weekday  # night belongs to its starting day
        else:
            # before sunrise — night of the previous day
            prev_sunset = swe.rise_trans(jd_ut - 1.5, swe.SUN, swe.CALC_SET,
                                         geopos, 0.0, 0.0, swe.FLG_SWIEPH)
            prev_sunset_jd = prev_sunset[1][0]
            elapsed = jd_ut - prev_sunset_jd
            hour_length = (sunrise_jd - prev_sunset_jd) / 12
            ref_weekday = (weekday - 1) % 7

    hour_index = int(elapsed / hour_length)
    if hour_index < 0:
        hour_index = 0
    if hour_index > 11:
        hour_index = 11

    day_lord = DAY_RULERS[ref_weekday]
    chaldean_start = CHALDEAN_ORDER.index(day_lord)

    if is_day:
        # 1st daylight hour = day lord
        hour_lord = CHALDEAN_ORDER[(chaldean_start + hour_index) % 7]
    else:
        # 1st night hour = 4 positions after day lord in Chaldean order
        hour_lord = CHALDEAN_ORDER[(chaldean_start + 12 + hour_index) % 7]

    return hour_lord


def cast(year: int, month: int, day: int,
         hour: int, minute: int, second: int = 0,
         tz_offset: float = 0.0,
         lat: float = 51.4769, lon: float = -0.0005,
         location: str = "Greenwich",
         question: str = "",
         house_system: bytes = b'R'):
    """
    Cast a horary chart.

    Args:
        year, month, day: Local civil date.
        hour, minute, second: Local civil time.
        tz_offset: Hours offset from UTC (e.g. London winter = 0, New York = -5).
        lat, lon: Latitude (+N) and longitude (+E) of the astrologer.
        location: Human-readable name of the location.
        question: The horary question.
        house_system: b'R' Regiomontanus (default for horary), b'P' Placidus.

    Returns:
        Dict with planets, houses, hour_lord, day_lord, and a formatted report.
    """
    # Convert local time to UTC
    ut_hour_local = hour + minute / 60 + second / 3600
    ut_hour = ut_hour_local - tz_offset
    # Note: julday handles fractional hours that fall outside 0-24 by
    # adjusting the day; we do the same explicitly for clarity.
    if ut_hour >= 24:
        ut_hour -= 24
        # Not adjusting day here — pyswisseph handles non-normalized hours.
        ut_hour += 24
    elif ut_hour < 0:
        ut_hour += 24
        # Same — let swe.julday treat as previous-day.
        ut_hour -= 24

    jd = swe.julday(year, month, day, ut_hour)
    swe.set_ephe_path(None)

    # Planetary positions
    planets_data = {}
    for name, idx in PLANETS.items():
        result = swe.calc_ut(jd, idx)
        longitude = result[0][0]
        speed = result[0][3]
        sign, d, m = deg_to_sign(longitude)
        planets_data[name] = {
            "longitude": longitude,
            "sign": sign,
            "degree": d,
            "minute": m,
            "retrograde": speed < 0,
            "speed": speed,
        }

    # House cusps (Regiomontanus by default)
    cusps, ascmc = swe.houses(jd, lat, lon, house_system)
    asc = ascmc[0]
    mc = ascmc[1]

    houses_data = []
    for i, cusp in enumerate(cusps[:12], 1):
        sign, d, m = deg_to_sign(cusp)
        houses_data.append({
            "house": i,
            "longitude": cusp,
            "sign": sign,
            "degree": d,
            "minute": m,
            "ruler": TRADITIONAL_RULERS[sign],
        })

    # Determine house of each planet
    for name, pos in planets_data.items():
        long_p = pos["longitude"]
        for i in range(12):
            cusp_a = cusps[i]
            cusp_b = cusps[(i + 1) % 12]
            if cusp_b < cusp_a:
                in_house = (long_p >= cusp_a) or (long_p < cusp_b)
            else:
                in_house = cusp_a <= long_p < cusp_b
            if in_house:
                pos["house"] = i + 1
                break

    # Day and hour lords
    from datetime import datetime, timezone, timedelta
    dt_local = datetime(year, month, day, hour, minute, second)
    dt_utc = dt_local - timedelta(hours=tz_offset)
    day_lord = DAY_RULERS[dt_utc.weekday()]
    try:
        hour_lord = planetary_hour(jd, lat, lon, dt_utc.weekday())
    except Exception as e:
        hour_lord = f"<computation error: {e}>"

    # Build text report
    lines = []
    lines.append("=" * 64)
    lines.append("HORARY CHART")
    lines.append("=" * 64)
    if question:
        lines.append(f"Question: {question}")
    lines.append(f"Local time: {year}-{month:02d}-{day:02d} "
                 f"{hour:02d}:{minute:02d}:{second:02d} "
                 f"(UTC{tz_offset:+g})")
    lines.append(f"UTC time:   {dt_utc.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Location:   {location} ({lat:+.4f}°, {lon:+.4f}°)")
    lines.append(f"JD UT:      {jd:.6f}")
    lines.append(f"Day Lord:   {day_lord}")
    lines.append(f"Hour Lord:  {hour_lord}")
    lines.append("")

    lines.append("--- PLANETS ---")
    for name, pos in planets_data.items():
        retro = "R" if pos["retrograde"] else " "
        lines.append(f"  {name:8s}: {pos['degree']:2d}°{pos['minute']:02d}' "
                     f"{pos['sign']:12s} {retro}  in House {pos.get('house', '?')}"
                     f"   ({pos['speed']:+.3f}°/day)")

    lines.append("")
    lines.append(f"--- HOUSES ({house_system.decode()}) ---")
    asc_sign, asc_d, asc_m = deg_to_sign(asc)
    mc_sign, mc_d, mc_m = deg_to_sign(mc)
    lines.append(f"  Asc: {asc_d:2d}°{asc_m:02d}' {asc_sign}")
    lines.append(f"  MC:  {mc_d:2d}°{mc_m:02d}' {mc_sign}")
    lines.append("")
    for h in houses_data:
        lines.append(f"  House {h['house']:2d}: {h['degree']:2d}°{h['minute']:02d}' "
                     f"{h['sign']:12s}  ruled by {h['ruler']}")

    report = "\n".join(lines)

    return {
        "question": question,
        "location": location,
        "lat": lat,
        "lon": lon,
        "tz_offset": tz_offset,
        "datetime_local": dt_local.isoformat(),
        "datetime_utc": dt_utc.isoformat(),
        "jd": jd,
        "day_lord": day_lord,
        "hour_lord": hour_lord,
        "asc": {"longitude": asc, "sign": asc_sign,
                "degree": asc_d, "minute": asc_m},
        "mc": {"longitude": mc, "sign": mc_sign,
               "degree": mc_d, "minute": mc_m},
        "planets": planets_data,
        "houses": houses_data,
        "report": report,
    }


def main():
    parser = argparse.ArgumentParser(description="Cast a horary chart.")
    parser.add_argument("--datetime", required=True,
                        help="Local datetime in 'YYYY-MM-DD HH:MM:SS' format.")
    parser.add_argument("--tz", type=float, default=0.0,
                        help="Timezone offset in hours (e.g. -5 for New York EST).")
    parser.add_argument("--lat", type=float, required=True,
                        help="Latitude (positive north).")
    parser.add_argument("--lon", type=float, required=True,
                        help="Longitude (positive east, negative west).")
    parser.add_argument("--location", default="",
                        help="Human-readable location name.")
    parser.add_argument("--question", default="",
                        help="The horary question.")
    parser.add_argument("--house-system", default="R",
                        choices=["R", "P", "K", "C", "E"],
                        help="House system: R=Regiomontanus (default), "
                             "P=Placidus, K=Koch, C=Campanus, E=Equal.")
    args = parser.parse_args()

    from datetime import datetime
    dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M:%S")
    chart = cast(
        year=dt.year, month=dt.month, day=dt.day,
        hour=dt.hour, minute=dt.minute, second=dt.second,
        tz_offset=args.tz,
        lat=args.lat, lon=args.lon,
        location=args.location or "Unspecified",
        question=args.question,
        house_system=args.house_system.encode(),
    )
    print(chart["report"])


if __name__ == "__main__":
    main()
