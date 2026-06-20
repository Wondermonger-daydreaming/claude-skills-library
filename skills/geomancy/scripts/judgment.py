#!/usr/bin/env python3
"""
Geomantic chart JUDGMENT — perfection, aspects, and the Court verdict.

Ideas #7 + #8 made executable: ADVANCED_TECHNIQUES.md §0 *defines* the four
modes of perfection; this module *computes* them, plus astrological aspects
between significators and Christopher Cattan's Court-based yes/no.

NOTE (primary-source accuracy): the four-mode scheme below is the MODERN
(Greer/Skinner) systematization. The primary printed Latin (Fludd) attests a
TRIAD — occupatio/conjunctio/translatio — and there translatio is the
querent's figure "passing over" (kin to occupation), not the neutral
third-figure go-between coded here. This module implements the modern scheme
deliberately; see ADVANCED_TECHNIQUES.md §0 and PROVENANCE.md §7a / DISPUTED.md.

The 12 houses are populated by the first twelve figures of the shield, in order:
    House  1..4  = the four Mothers
    House  5..8  = the four Daughters
    House  9..12 = the four Nieces
(The Witnesses, Judge and Sentence are the "Court", read separately.)

Conventions (documented because traditions vary):
  - Adjacency for perfection = house n and n±1, no wrap (houses 1 and 12 are not
    adjacent). This is the common Agrippa-house reading.
  - Aspects use circular house-distance d = min(|h1-h2|, 12-|h1-h2|):
    0 conjunction · 2 sextile · 3 square · 4 trine · 6 opposition · else none.
  - Figure favorability (good/ill/neutral) is the common standard (Greer-ish);
    it is INTERPRETIVE, not locked like the dot-patterns — adjust to taste.

Usage:
    python judgment.py "my question"     # generate a chart and judge houses 1 & 7
    python judgment.py --seed 12345 --q 1 --quesited 10
"""

import argparse
import generate_shield as gs

# Interpretive (NOT locked) — common good/ill classification of the 16 figures.
FAVORABILITY = {
    "Fortuna Major": "good", "Fortuna Minor": "good", "Acquisitio": "good",
    "Laetitia": "good", "Caput Draconis": "good", "Conjunctio": "good",
    "Albus": "good", "Puella": "good",
    "Rubeus": "ill", "Cauda Draconis": "ill", "Tristitia": "ill",
    "Carcer": "ill", "Amissio": "ill", "Puer": "ill",
    "Populus": "neutral", "Via": "neutral",
}


def houses(chart) -> list:
    """Return the 12 house-figures (index 0 = House I ... index 11 = House XII)."""
    return list(chart.mothers) + list(chart.daughters) + list(chart.nieces)


def _adj(h: int) -> list:
    """Houses adjacent to house h (1-based), no wrap."""
    return [x for x in (h - 1, h + 1) if 1 <= x <= 12]


def perfection(chart, querent: int = 1, quesited: int = 7) -> dict:
    """Does the matter perfect? Return the strongest mode, or none.

    querent/quesited are 1-based house numbers (default I and VII).
    """
    H = houses(chart)
    fq, fu = H[querent - 1].name, H[quesited - 1].name

    if fq == fu:
        return {"perfects": True, "mode": "occupation",
                "detail": f"both significators are {fq} — perfects unconditionally"}

    # conjunction: one significator's figure sits adjacent to the other's house
    if any(H[a - 1].name == fq for a in _adj(quesited)):
        return {"perfects": True, "mode": "conjunction",
                "detail": f"querent's {fq} reaches the quesited's house — the querent moves to it"}
    if any(H[a - 1].name == fu for a in _adj(querent)):
        return {"perfects": True, "mode": "conjunction",
                "detail": f"quesited's {fu} reaches the querent's house — the quesited comes to the querent"}

    # mutation: the two significators sit in two adjacent houses, neither their own
    for h in range(1, 12):
        if {H[h - 1].name, H[h].name} == {fq, fu} and h not in (querent, quesited) and (h + 1) not in (querent, quesited):
            return {"perfects": True, "mode": "mutation",
                    "detail": f"{fq} and {fu} meet at houses {h}/{h + 1} — perfection by outside meeting"}

    # translation: a third (non-significator) figure is adjacent to BOTH houses
    near_q = {H[a - 1].name for a in _adj(querent)} - {fq, fu}
    near_u = {H[a - 1].name for a in _adj(quesited)} - {fq, fu}
    carriers = near_q & near_u
    if carriers:
        return {"perfects": True, "mode": "translation",
                "detail": f"{sorted(carriers)[0]} carries testimony between the two — perfection via go-between"}

    return {"perfects": False, "mode": None,
            "detail": "no occupation/conjunction/mutation/translation — the matter does not perfect"}


def aspect(h1: int, h2: int) -> str:
    """Astrological aspect between two houses by circular distance."""
    d = abs(h1 - h2)
    d = min(d, 12 - d)
    return {0: "conjunction", 2: "sextile", 3: "square", 4: "trine", 6: "opposition"}.get(d, "none")


def court_verdict(chart) -> dict:
    """Cattan's Court read: a fast yes/no from the Judge + the two Witnesses."""
    j = FAVORABILITY.get(chart.judge.name, "neutral")
    rw = FAVORABILITY.get(chart.right_witness.name, "neutral")
    lw = FAVORABILITY.get(chart.left_witness.name, "neutral")
    goods = [x for x in (rw, lw) if x == "good"]
    ills = [x for x in (rw, lw) if x == "ill"]
    if j == "good":
        v = "yes" if not ills else "yes, but with difficulty (a witness opposes)"
    elif j == "ill":
        v = "no" if not goods else "no, though a witness softens it"
    else:
        v = "open / qualified — the Judge is neutral; weigh the witnesses and the houses"
    return {"verdict": v, "judge": f"{chart.judge.name} ({j})",
            "right_witness": f"{chart.right_witness.name} ({rw})",
            "left_witness": f"{chart.left_witness.name} ({lw})"}


def _self_test() -> None:
    c = gs.generate_shield(seed=12345)
    assert len(houses(c)) == 12
    p = perfection(c, 1, 7)
    assert p["mode"] in (None, "occupation", "conjunction", "mutation", "translation")
    assert aspect(1, 7) == "opposition" and aspect(1, 1) == "conjunction" and aspect(1, 5) == "trine"
    assert "verdict" in court_verdict(c)


_self_test()


def main():
    ap = argparse.ArgumentParser(description="Judge a geomantic chart (perfection, aspect, Court)")
    ap.add_argument("question", nargs="?", help="question to seed the chart")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--q", type=int, default=1, help="querent house (default I)")
    ap.add_argument("--quesited", type=int, default=7, help="quesited house (default VII)")
    a = ap.parse_args()
    c = gs.generate_shield(question=a.question, seed=a.seed)
    H = houses(c)
    print(f"Querent  House {a.q}: {H[a.q - 1].name}")
    print(f"Quesited House {a.quesited}: {H[a.quesited - 1].name}")
    p = perfection(c, a.q, a.quesited)
    print(f"\nPERFECTION: {'YES' if p['perfects'] else 'NO'} — {p['mode'] or '—'}\n  {p['detail']}")
    print(f"ASPECT (House {a.q}↔{a.quesited}): {aspect(a.q, a.quesited)}")
    cv = court_verdict(c)
    print(f"\nCOURT VERDICT: {cv['verdict']}")
    print(f"  Judge {cv['judge']} · R.Witness {cv['right_witness']} · L.Witness {cv['left_witness']}")
    print(f"\n(Chart valid: {c.validate()} · seed {c.seed})")


if __name__ == "__main__":
    main()
