#!/usr/bin/env python3
"""
judge.py — the horary JUDGMENT ENGINE.

Integrates the chart-caster (cast_chart.py) and the dignity calculators
(dignities.py) into the end-to-end pipeline a reading needs: sect ->
significators -> dignities -> the perfection search (direct / translation /
collection / reception, WITH applying-vs-separating computed from real
ephemeris speeds) -> impediments (prohibition / refranation / combustion) ->
the Moon's next application -> the Part of Fortune.

It builds the SKELETON of a reading. It does NOT render the judgment — that
synthesis stays with the astrologer. The script casts and bookkeeps; the
astrologer weighs and speaks. (See SKILL.md: "the script casts; the astrologer
judges.")

USAGE
    # Judge a cast chart for a quesited house (5 = creations/works):
    python judge.py --datetime "2024-01-01 12:00:00" --tz 0 \
        --lat 51.4779 --lon -0.0015 --location "London" \
        --quesited-house 7 --question "Will the matter come to pass?"

    # Or by question type (maps to the house):
    python judge.py --datetime "..." --tz -3 --lat .. --lon .. --topic marriage

    # Self-test / demo (runs a deterministic fixture, checks the engine):
    python judge.py --test

DEPENDENCIES
    pyswisseph (for casting). All judgment logic is pure Python over the cast.
"""
from __future__ import annotations
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dignities as dg  # noqa: E402

# Question topic -> primary quesited house (Lilly's house significations).
TOPIC_HOUSES = {
    "self": 1, "money": 2, "possessions": 2, "siblings": 3, "communication": 3,
    "travel-short": 3, "father": 4, "home": 4, "property": 4, "land": 4,
    "children": 5, "creation": 5, "work": 5, "creativity": 5, "pregnancy": 5,
    "pleasure": 5, "illness": 6, "servants": 6, "employees": 6, "pets": 6,
    "marriage": 7, "partner": 7, "relationship": 7, "spouse": 7, "enemy": 7,
    "lawsuit": 7, "death": 8, "inheritance": 8, "others-money": 8,
    "religion": 9, "higher-learning": 9, "travel-long": 9, "dreams": 9,
    "career": 10, "reputation": 10, "honor": 10, "mother": 10, "boss": 10,
    "friends": 11, "hopes": 11, "wishes": 11, "patrons": 11,
    "hidden-enemies": 12, "imprisonment": 12, "sorrow": 12,
}

ASPECT_NAMES = {0: "conjunction", 60: "sextile", 90: "square",
                120: "trine", 180: "opposition"}
ASPECT_GLYPH = {0: "☌", 60: "⚹", 90: "□", 120: "△", 180: "☍"}

# Average daily motion (deg/day) — for "faster/slower" ORDERING only.
# Aligned to DIGNITIES.md §IX (Moon 13°10' = 13.167, etc.).
MEAN_SPEED = {"Moon": 13.167, "Mercury": 1.383, "Venus": 1.2, "Sun": 0.983,
              "Mars": 0.517, "Jupiter": 0.083, "Saturn": 0.033}

# Swift/slow accidental-dignity thresholds (deg/day) from DIGNITIES.md §IX.
# (swift_if_above, slow_if_below) — between them is the NEUTRAL band (no points).
# The Sun has no swift/slow. The Moon's divider is its mean (no neutral band).
SPEED_THRESHOLDS = {
    "Moon": (13.167, 13.167), "Mercury": (1.5, 1.0), "Venus": (1.25, 0.983),
    "Mars": (0.667, 0.417), "Jupiter": (0.133, 0.05), "Saturn": (0.05, 0.0167),
}

def speed_class(planet: str, speed: float):
    """'swift' / 'slow' / None per DIGNITIES.md §IX (None = neutral band or Sun)."""
    if planet == "Sun" or planet not in SPEED_THRESHOLDS:
        return None
    sp = abs(speed)
    hi, lo = SPEED_THRESHOLDS[planet]
    if sp > hi:
        return "swift"
    if sp < lo:
        return "slow"
    return None

# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def ang_sep(a: float, b: float) -> float:
    """Angular separation 0..180."""
    d = abs((a - b) % 360)
    return d if d <= 180 else 360 - d

def aspect_status(lon1, s1, lon2, s2, p1, p2):
    """
    Find the tightest Ptolemaic aspect (within moiety orb) between two bodies
    and decide applying vs separating from real speeds (numeric derivative).
    Returns dict or None.
    """
    allowed = dg.moiety(p1) + dg.moiety(p2)
    sep = ang_sep(lon1, lon2)
    best = None
    for angle in ASPECT_NAMES:
        orb = abs(sep - angle)
        if orb <= allowed and (best is None or orb < best["orb"]):
            dt = 0.02
            orb_next = abs(ang_sep(lon1 + s1 * dt, lon2 + s2 * dt) - angle)
            applying = orb_next < orb
            rate = abs(orb - orb_next) / dt  # deg/day the orb closes
            days = (orb / rate) if (applying and rate > 1e-9) else None
            best = {"angle": angle, "name": ASPECT_NAMES[angle],
                    "glyph": ASPECT_GLYPH[angle], "orb": round(orb, 2),
                    "allowed": round(allowed, 2), "applying": applying,
                    "deg_to_perfect": round(orb, 2) if applying else None,
                    "days_approx": round(days, 1) if days else None}
    return best

# ---------------------------------------------------------------------------
# Chart accessors
# ---------------------------------------------------------------------------

def sect_of(chart) -> str:
    """Night if the Sun is below the horizon (houses 1-6), else day."""
    return "night" if chart["planets"]["Sun"]["house"] in (1, 2, 3, 4, 5, 6) else "day"

def lord_of_house(chart, n: int) -> str:
    return chart["houses"][n - 1]["ruler"]

def lon_of(chart, planet: str) -> float:
    return chart["planets"][planet]["longitude"]

def speed_of(chart, planet: str) -> float:
    return chart["planets"][planet]["speed"]

def pos_str(chart, planet: str) -> str:
    p = chart["planets"][planet]
    r = " R" if p["retrograde"] else ""
    return f"{p['degree']}°{p['minute']:02d}' {p['sign']}{r} (h{p['house']})"

def reception(chart, a: str, b: str) -> list:
    """Receptions between two planets by domicile/exaltation (which receives which)."""
    out = []
    sa, sb = chart["planets"][a]["sign"], chart["planets"][b]["sign"]
    if dg.DOMICILE[sa] == b:
        out.append(f"{b} receives {a} by domicile")
    if dg.DOMICILE[sb] == a:
        out.append(f"{a} receives {b} by domicile")
    if a in dg.EXALTATION and dg.EXALTATION[a][0] == sb:
        out.append(f"{b} receives {a} by exaltation")
    if b in dg.EXALTATION and dg.EXALTATION[b][0] == sa:
        out.append(f"{a} receives {b} by exaltation")
    mutual = any("receives" in x for x in out) and len(
        {x.split()[0] for x in out}) >= 2
    return out

# ---------------------------------------------------------------------------
# The perfection search
# ---------------------------------------------------------------------------

PLANETS = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]

def perfection_search(chart, sigA: str, sigB: str) -> dict:
    """Direct aspect / translation / collection / mutual reception between sigs."""
    result = {"direct": None, "translation": [], "collection": [],
              "reception": []}

    # Direct aspect
    direct = aspect_status(lon_of(chart, sigA), speed_of(chart, sigA),
                           lon_of(chart, sigB), speed_of(chart, sigB),
                           sigA, sigB)
    if direct:
        result["direct"] = direct

    # Reception
    result["reception"] = reception(chart, sigA, sigB)

    others = [p for p in PLANETS if p not in (sigA, sigB)]
    for c in others:
        asp_a = aspect_status(lon_of(chart, c), speed_of(chart, c),
                              lon_of(chart, sigA), speed_of(chart, sigA), c, sigA)
        asp_b = aspect_status(lon_of(chart, c), speed_of(chart, c),
                              lon_of(chart, sigB), speed_of(chart, sigB), c, sigB)
        if not asp_a or not asp_b:
            continue
        c_faster = MEAN_SPEED[c] > MEAN_SPEED[sigA] and MEAN_SPEED[c] > MEAN_SPEED[sigB]
        c_slower = MEAN_SPEED[c] < MEAN_SPEED[sigA] and MEAN_SPEED[c] < MEAN_SPEED[sigB]
        # Translation: a faster C separating from one, applying to the other
        if c_faster and (asp_a["applying"] != asp_b["applying"]):
            result["translation"].append(
                {"by": c, "to_A": asp_a, "to_B": asp_b})
        # Collection: a slower C that BOTH significators apply to
        if c_slower and asp_a["applying"] and asp_b["applying"]:
            result["collection"].append(
                {"by": c, "from_A": asp_a, "from_B": asp_b})
    return result

# ---------------------------------------------------------------------------
# Impediments
# ---------------------------------------------------------------------------

def combustion(chart, planet: str) -> str | None:
    if planet == "Sun":
        return None
    d = ang_sep(lon_of(chart, planet), lon_of(chart, "Sun"))
    if d <= 17 / 60:
        return "cazimi (strengthened, in the Sun's heart)"
    if d <= 8.5:
        return f"combust ({d:.1f}° from Sun — burnt, hidden)"
    if d <= 17:
        return f"under the beams ({d:.1f}° from Sun — weakened)"
    return None

def refranation(chart, planet: str) -> str | None:
    """A significator about to station retrograde cannot complete an aspect."""
    sp = speed_of(chart, planet)
    if chart["planets"][planet]["retrograde"]:
        return f"{planet} is retrograde (light may withdraw / a matter reverses or returns)"
    if 0 < sp < 0.05 and planet not in ("Jupiter", "Saturn"):
        return f"{planet} is nearly stationary (slow to act; risk of refranation)"
    return None

def prohibition(chart, sigA, sigB, direct) -> list:
    """A third planet that perfects with a significator sooner than A-B perfect."""
    if not direct or not direct["applying"] or direct["deg_to_perfect"] is None:
        return []
    out = []
    for c in [p for p in PLANETS if p not in (sigA, sigB)]:
        for sig in (sigA, sigB):
            a = aspect_status(lon_of(chart, c), speed_of(chart, c),
                              lon_of(chart, sig), speed_of(chart, sig), c, sig)
            if a and a["applying"] and a["deg_to_perfect"] is not None \
                    and a["deg_to_perfect"] < direct["deg_to_perfect"]:
                out.append(f"{c} {a['glyph']} {sig} perfects first "
                           f"({a['deg_to_perfect']}° vs {direct['deg_to_perfect']}°) "
                           f"— possible prohibition")
    return out

# ---------------------------------------------------------------------------
# Moon's next application / void of course
# ---------------------------------------------------------------------------

def moon_next_application(chart) -> dict:
    moon_lon = lon_of(chart, "Moon")
    moon_deg_in_sign = chart["planets"]["Moon"]["degree"] + chart["planets"]["Moon"]["minute"] / 60
    deg_to_sign_end = 30 - moon_deg_in_sign
    apps = []
    for c in [p for p in PLANETS if p != "Moon"]:
        a = aspect_status(moon_lon, speed_of(chart, "Moon"),
                          lon_of(chart, c), speed_of(chart, c), "Moon", c)
        if a and a["applying"] and a["deg_to_perfect"] is not None:
            apps.append((a["deg_to_perfect"], c, a))
    apps.sort()
    if not apps:
        return {"void_of_course": True,
                "note": "Moon makes no applying Ptolemaic aspect — 'nothing will come of the matter' (check Lilly's VOC exceptions in Taurus/Cancer/Sagittarius/Pisces)"}
    deg, c, a = apps[0]
    before_sign_change = deg <= deg_to_sign_end
    return {"void_of_course": not before_sign_change,
            "next": f"Moon {a['glyph']} {c} in {deg}° ({a['name']}, {'applying' if a['applying'] else ''})",
            "perfects_before_leaving_sign": before_sign_change,
            "all_applications": [f"{c} {a['glyph']} ({deg}°)" for deg, c, a in apps]}

# ---------------------------------------------------------------------------
# The full judgment skeleton
# ---------------------------------------------------------------------------

def judge(chart, quesited_house: int, question: str = "") -> dict:
    sect = sect_of(chart)
    l1 = lord_of_house(chart, 1)
    quesited = lord_of_house(chart, quesited_house)

    def dignity(planet):
        p = chart["planets"][planet]
        deg = p["degree"] + p["minute"] / 60
        ess = dg.essential_dignity(planet, p["sign"], deg, sect)
        motion = "retrograde" if p["retrograde"] else "direct"
        speed = speed_class(planet, p["speed"])
        acc = dg.accidental_dignity(p["house"], motion, speed)
        return {"planet": planet, "position": pos_str(chart, planet),
                "essential": ess["essential_score"],
                "accidental": acc["accidental_score"],
                "total": ess["essential_score"] + acc["accidental_score"],
                "detail": ess["dignities"] + ess["debilities"] + acc["factors"]}

    same = (quesited == l1)
    perf = None if same else perfection_search(chart, l1, quesited)
    direct = perf["direct"] if perf else None

    asc = chart["asc"]
    pof = dg.part_of_fortune(asc["longitude"], lon_of(chart, "Sun"),
                             lon_of(chart, "Moon"), sect)
    pof_house = house_of_longitude(chart, pof["longitude"])

    return {
        "question": question, "sect": sect,
        "querent": {"sig": l1, "dignity": dignity(l1),
                    "moon": dignity("Moon")},
        "quesited": {"house": quesited_house, "sig": quesited,
                     "dignity": dignity(quesited),
                     "note": "quesited ruler == querent ruler (same planet signifies both)" if same else None},
        "perfection": perf,
        "impediments": {
            "combust_querent": combustion(chart, l1),
            "combust_quesited": None if same else combustion(chart, quesited),
            "refranation_querent": refranation(chart, l1),
            "refranation_quesited": None if same else refranation(chart, quesited),
            "prohibition": prohibition(chart, l1, quesited, direct) if not same else [],
        },
        "moon": moon_next_application(chart),
        "part_of_fortune": {**pof, "house": pof_house},
    }

def house_of_longitude(chart, lon: float) -> int:
    cusps = [(h["house"], h["longitude"]) for h in chart["houses"]]
    for i in range(12):
        a = cusps[i][1]
        b = cusps[(i + 1) % 12][1]
        inside = (a <= lon < b) if b > a else (lon >= a or lon < b)
        if inside:
            return cusps[i][0]
    return 0

# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render(j) -> str:
    L = []
    L.append("=" * 66)
    L.append("HORARY JUDGMENT SKELETON  (the engine bookkeeps; the astrologer reads)")
    L.append("=" * 66)
    if j["question"]:
        L.append(f"Q: {j['question']}")
    L.append(f"Sect: {j['sect']} chart")
    L.append("")
    q = j["querent"]
    L.append(f"QUERENT  = {q['sig']} (Lord 1)  +  Moon (always)")
    L.append(f"  {q['sig']:8s} {q['dignity']['position']:24s}  "
             f"ess {q['dignity']['essential']:+d} / acc {q['dignity']['accidental']:+d} = "
             f"{q['dignity']['total']:+d}")
    L.append(f"    [{', '.join(q['dignity']['detail']) or 'none'}]")
    L.append(f"  {'Moon':8s} {q['moon']['position']:24s}  "
             f"ess {q['moon']['essential']:+d} / acc {q['moon']['accidental']:+d} = "
             f"{q['moon']['total']:+d}")
    L.append(f"    [{', '.join(q['moon']['detail']) or 'none'}]")
    L.append("")
    qd = j["quesited"]
    L.append(f"QUESITED = {qd['sig']} (Lord {qd['house']})")
    if qd["note"]:
        L.append(f"  ! {qd['note']}")
    L.append(f"  {qd['sig']:8s} {qd['dignity']['position']:24s}  "
             f"ess {qd['dignity']['essential']:+d} / acc {qd['dignity']['accidental']:+d} = "
             f"{qd['dignity']['total']:+d}")
    L.append(f"    [{', '.join(qd['dignity']['detail']) or 'none'}]")
    L.append("")
    L.append("PERFECTION — does the light reach?")
    p = j["perfection"]
    if p is None:
        L.append("  (querent and quesited share one significator — read its condition directly)")
    else:
        d = p["direct"]
        if d:
            status = "APPLYING" if d["applying"] else "separating (past)"
            extra = f", perfects in ~{d['deg_to_perfect']}° (~{d['days_approx']}d)" if d["applying"] else ""
            L.append(f"  Direct: {q['sig']} {d['glyph']} {qd['sig']} "
                     f"({d['name']}, orb {d['orb']}/{d['allowed']}°, {status}{extra})")
        else:
            L.append(f"  Direct: none in orb between {q['sig']} and {qd['sig']}")
        for t in p["translation"]:
            L.append(f"  Translation of light by {t['by']} "
                     f"(to {q['sig']}: {'appl' if t['to_A']['applying'] else 'sep'} {t['to_A']['glyph']}; "
                     f"to {qd['sig']}: {'appl' if t['to_B']['applying'] else 'sep'} {t['to_B']['glyph']})")
        for c in p["collection"]:
            L.append(f"  Collection of light by {c['by']} (both significators apply to it)")
        for r in p["reception"]:
            L.append(f"  Reception: {r}")
        if not (p["direct"] or p["translation"] or p["collection"] or p["reception"]):
            L.append("  No perfection found — the matter may not come to pass without effort.")
    L.append("")
    L.append("IMPEDIMENTS")
    imp = j["impediments"]
    any_imp = False
    for k in ("combust_querent", "combust_quesited", "refranation_querent", "refranation_quesited"):
        if imp[k]:
            L.append(f"  {k}: {imp[k]}"); any_imp = True
    for pr in imp["prohibition"]:
        L.append(f"  {pr}"); any_imp = True
    if not any_imp:
        L.append("  none detected (light not burnt, withdrawn, or cut off)")
    L.append("")
    m = j["moon"]
    L.append("MOON")
    if m["void_of_course"]:
        L.append(f"  VOID OF COURSE — {m.get('note', m.get('next',''))}")
    else:
        L.append(f"  Next application: {m['next']}  "
                 f"(perfects before sign change: {m['perfects_before_leaving_sign']})")
        L.append(f"  Sequence: {', '.join(m['all_applications'])}")
    L.append("")
    pf = j["part_of_fortune"]
    L.append(f"PART OF FORTUNE: {pf['degree']}° {pf['sign']} in house {pf['house']}  "
             f"[{pf['formula']}]")
    L.append("")
    L.append("-> The skeleton is built. Weigh the testimonies and render judgment.")
    return "\n".join(L)

# ---------------------------------------------------------------------------
# Self-test / demo
# ---------------------------------------------------------------------------

def run_demo_and_test() -> int:
    try:
        from cast_chart import cast
    except Exception as e:
        print(f"Cannot import cast_chart ({e}); is pyswisseph installed?")
        return 2
    # Deterministic regression fixture: Greenwich, 2024-01-01 12:00:00 UTC.
    # Chosen because it exercises the whole engine — collection of light,
    # combustion, and a void-of-course Moon — not just a direct aspect.
    chart = cast(year=2024, month=1, day=1, hour=12, minute=0, second=0,
                 tz_offset=0, lat=51.4779, lon=-0.0015,
                 location="Greenwich",
                 question="Will the matter come to pass?")
    j = judge(chart, quesited_house=7,
              question="Will the matter come to pass?")
    print(render(j))
    print("\n" + "=" * 66)
    print("SELF-TEST (deterministic fixture — Greenwich 2024-01-01 12:00 UTC):")
    fails = []
    def chk(desc, got, want):
        if got != want:
            fails.append(f"  FAIL {desc}: got {got!r} want {want!r}")
    chk("sect (day chart)", j["sect"], "day")
    chk("querent L1 = Mars", j["querent"]["sig"], "Mars")
    # Mars: term +2, h9 +2, direct +4, swift +2 => total +10.
    chk("Mars total +10", j["querent"]["dignity"]["total"], 10)
    # Moon: peregrine (no essential dignity), h6 -2, direct +4, slow -2 => 0.
    chk("Moon total 0 (peregrine)", j["querent"]["moon"]["total"], 0)
    chk("Moon flagged peregrine", "peregrine" in j["querent"]["moon"]["detail"], True)
    chk("quesited L7 = Venus", j["quesited"]["sig"], "Venus")
    chk("Venus total +8", j["quesited"]["dignity"]["total"], 8)
    # No direct aspect Mars-Venus; light is gathered by a heavier planet (Saturn).
    chk("no direct perfection", j["perfection"]["direct"], None)
    chk("collection of light detected", len(j["perfection"]["collection"]) >= 1, True)
    chk("collector is Saturn", j["perfection"]["collection"][0]["by"], "Saturn")
    # Impediment: Mars (L1) is under the Sun's beams.
    chk("querent impeded by the Sun's beams",
        j["impediments"]["combust_querent"] is not None, True)
    # Moon makes no applying Ptolemaic aspect before leaving its sign.
    chk("Moon void of course", j["moon"]["void_of_course"], True)
    chk("Part of Fortune in 8th house", j["part_of_fortune"]["house"], 8)
    if fails:
        print(f"FAILED ({len(fails)}):"); print("\n".join(fails)); return 1
    print("PASSED — engine reproduces the fixture: day sect, Mars/Venus significators,")
    print("collection of light by Saturn, querent under the beams, void Moon, ⊕ in the 8th.")
    return 0

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Horary judgment engine.")
    ap.add_argument("--test", action="store_true")
    ap.add_argument("--datetime"); ap.add_argument("--tz", type=float, default=0.0)
    ap.add_argument("--lat", type=float); ap.add_argument("--lon", type=float)
    ap.add_argument("--location", default="Unspecified")
    ap.add_argument("--question", default="")
    ap.add_argument("--quesited-house", type=int)
    ap.add_argument("--topic", help="question topic -> house (e.g. marriage, career, money)")
    ap.add_argument("--house-system", default="R")
    args = ap.parse_args()

    if args.test:
        raise SystemExit(run_demo_and_test())

    if not (args.datetime and args.lat is not None and args.lon is not None):
        raise SystemExit("need --datetime --lat --lon (or --test)")
    qh = args.quesited_house or TOPIC_HOUSES.get((args.topic or "").lower())
    if not qh:
        raise SystemExit("need --quesited-house N or a known --topic")

    from cast_chart import cast
    from datetime import datetime
    dt = datetime.strptime(args.datetime, "%Y-%m-%d %H:%M:%S")
    chart = cast(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour,
                 minute=dt.minute, second=dt.second, tz_offset=args.tz,
                 lat=args.lat, lon=args.lon, location=args.location,
                 question=args.question, house_system=args.house_system.encode())
    print(chart["report"])
    print()
    print(render(judge(chart, qh, args.question)))


if __name__ == "__main__":
    main()
