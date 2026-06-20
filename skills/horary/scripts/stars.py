#!/usr/bin/env python3
"""
stars.py — fixed stars, decans, and lunar mansions, made computable.

The three star-anchored layers of the tradition, each now a lookup:

  • FIXED STARS  — precessed tropical longitude for the chart date (Swiss
    Ephemeris, via dignities.fixstar_longitude; needs ephe/sefstars.txt, bundled).
  • DECANS (faces) — the 36 ten-degree thirds. Bounds are FIXED tropical (decans
    do NOT precess in this division). Planetary ruler = Chaldean face ruler
    (dignities.face_ruler). Rich multi-tradition attributes from
    references/decans-data.json (Liber Hermetis, Sacred Book of Hermes, the
    decan-gods, Testament of Solomon spirits, etc.).
  • LUNAR MANSIONS — the 28 manāzil. EQUAL-DIVISION bounds (360/28 = 12.857°
    from 0° Aries) are tropical & FIXED; the marking stars PRECESS. Arabic-rooted
    data from references/mansions-data.json, with Latin names and the
    Arabic↔Latin nature deltas kept visible.

USAGE
    python stars.py --decan 13.68          # what decan is 13.68° (= 13°41' Aries)?
    python stars.py --mansion 130          # what lunar mansion is 130° (=10° Leo)?
    python stars.py --star Regulus 2461212.43   # precessed longitude for a JD
    python stars.py --test

Pure Python except --star (needs pyswisseph + the bundled sefstars.txt).
"""
from __future__ import annotations
import argparse
import json
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
_REF = os.path.join(_DIR, "..", "references")
SIGNS = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra",
         "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
MANSION_WIDTH = 360 / 28  # 12.857142...°

def _load(name):
    with open(os.path.join(_REF, name), encoding="utf-8") as f:
        return json.load(f)

_DECANS = _load("decans-data.json")["decans"]
_MANSIONS = _load("mansions-data.json")["mansions"]

# Chaldean face cycle (mirrors dignities.FACE_CYCLE; kept here so stars.py is
# usable standalone, but cross-checked against dignities in --test).
FACE_CYCLE = ["Mars", "Sun", "Venus", "Mercury", "Moon", "Saturn", "Jupiter"]

def _norm(lon):
    return lon % 360

def sign_and_deg(lon):
    lon = _norm(lon)
    return SIGNS[int(lon // 30)], lon % 30

# ---------------------------------------------------------------------------

def decan(lon: float) -> dict:
    """Full decan entry for a longitude: bounds, Chaldean ruler, all attributes."""
    sign, deg = sign_and_deg(lon)
    third = int(deg // 10) + 1
    key = f"{sign} {third}"
    entry = dict(_DECANS[key])
    face_no = SIGNS.index(sign) * 3 + (third - 1)
    entry["ruler_chaldean_face"] = FACE_CYCLE[face_no % 7]
    entry["_key"] = key
    return entry

def lunar_mansion(lon: float) -> dict:
    """Equal-division lunar mansion for a longitude (tropical, non-precessing)."""
    lon = _norm(lon)
    n = int(lon // MANSION_WIDTH) + 1
    if n > 28:
        n = 28
    return dict(_MANSIONS[str(n)])

def fixed_star(name: str, jd_ut: float):
    """Precessed tropical longitude (+ sign/deg) of a fixed star for a date."""
    import dignities as dg  # local import: only --star needs swisseph
    lon = dg.fixstar_longitude(name, jd_ut)
    if lon is None:
        return None
    sign, deg = sign_and_deg(lon)
    return {"star": name, "longitude": round(lon, 4),
            "position": f"{deg:.2f}° {sign}"}

# ---------------------------------------------------------------------------

def run_tests() -> int:
    import sys
    sys.path.insert(0, _DIR)
    fails = []
    def chk(d, got, want):
        if got != want:
            fails.append(f"  FAIL {d}: got {got!r} want {want!r}")

    # Decans
    d = decan(5)            # 5° Aries
    chk("decan 5° -> Aries 1", d["_key"], "Aries 1")
    chk("decan 5° ruler Mars (Chaldean face)", d["ruler_chaldean_face"], "Mars")
    chk("decan 5° has Liber Hermetis Name", "Liber Hermetis Name" in d, True)
    chk("decan 13.68° (13°41' Aries) third 2", decan(13.68)["third"], 2)
    chk("decan 128.67° -> Leo 1", decan(128.67)["_key"], "Leo 1")
    chk("36 decans loaded", len(_DECANS), 36)

    # Decan ruler must agree with dignities.face_ruler for all 36
    import dignities as dg
    for s in SIGNS:
        for third in range(3):
            lon = SIGNS.index(s) * 30 + third * 10 + 5
            chk(f"decan ruler == dignities.face_ruler @ {s}{third+1}",
                decan(lon)["ruler_chaldean_face"], dg.face_ruler(s, third * 10 + 5))

    # Mansions
    m = lunar_mansion(0)
    chk("mansion 0° -> #1", m["number"], 1)
    chk("mansion 0° -> al-Sharaṭayn", m["arabic"].startswith("al-Shara"), True)
    chk("mansion 130° (10° Leo) -> #11 al-Zubra", lunar_mansion(130)["number"], 11)
    chk("mansion 130° arabic al-Zubra", lunar_mansion(130)["arabic"], "al-Zubra")
    chk("mansion 359° -> #28", lunar_mansion(359)["number"], 28)
    chk("28 mansions loaded", len(_MANSIONS), 28)

    if fails:
        print(f"SELF-TEST FAILED ({len(fails)}):"); print("\n".join(fails)); return 1
    print("SELF-TEST PASSED — 36 decans + 28 mansions loaded; decan rulers match")
    print("dignities.face_ruler for all 36; mansion equal-division bounds correct.")
    # Bonus: live star check (non-fatal)
    fs = fixed_star("Regulus", 2461212.43)
    if fs:
        print(f"  (live fixed star OK: Regulus -> {fs['position']})")
    else:
        print("  (fixed-star compute unavailable — pyswisseph/sefstars.txt missing)")
    return 0

# ---------------------------------------------------------------------------

def _print_decan(d):
    print(f"DECAN: {d['_key']}  ({d['start_deg']}–{d['end_deg']}°, "
          f"Liber Hermetis #{d.get('decan_number_LiberHermetis')})")
    print(f"  Chaldean face ruler: {d['ruler_chaldean_face']}")
    for k, v in d.items():
        if k in ("sign", "third", "start_deg", "end_deg", "_key",
                 "ruler_chaldean_face", "decan_number_LiberHermetis"):
            continue
        v = v if len(str(v)) < 160 else str(v)[:157] + "…"
        print(f"  {k}: {v}")

def _print_mansion(m):
    print(f"MANSION {m['number']}: {m['arabic']} ({m['meaning']})  [Latin: {m['latin']}]")
    print(f"  Equal-division start: {m['eq_div_start']} ({m['eq_div_start_deg']}°) — fixed/tropical")
    print(f"  Marking star (precesses): {m['marking_star_precesses']}")
    print(f"  Nature (Latin, Picatrix/Agrippa): {m['nature_latin_picatrix_agrippa']}")
    print(f"  Nature (Arabic, Abenragel):       {m['nature_arabic_abenragel']}")
    print(f"  Arabic↔Latin delta: {m['arabic_latin_delta']}")

def main():
    ap = argparse.ArgumentParser(description="Fixed stars, decans, lunar mansions.")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--decan", type=float)
    ap.add_argument("--mansion", type=float)
    ap.add_argument("--star", nargs=2, metavar=("NAME", "JD"))
    args = ap.parse_args()
    if args.test:
        raise SystemExit(run_tests())
    if args.decan is not None:
        _print_decan(decan(args.decan))
    if args.mansion is not None:
        _print_mansion(lunar_mansion(args.mansion))
    if args.star:
        import sys
        sys.path.insert(0, _DIR)
        fs = fixed_star(args.star[0], float(args.star[1]))
        print(fs if fs else f"{args.star[0]}: (pyswisseph/sefstars.txt unavailable)")
    if not (args.decan is not None or args.mansion is not None or args.star):
        ap.print_help()

if __name__ == "__main__":
    main()
