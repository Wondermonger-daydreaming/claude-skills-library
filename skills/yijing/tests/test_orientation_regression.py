"""
Regression tests for the trigram-orientation bug (fixed 2026-06-20).

These supply the EXTERNAL ORACLE the original suite lacked: an independent,
first-principles King Wen mapping derived from the trigram line-figures (no
hand-typed 6-bit hexagram patterns — the very thing that fooled the first audit
pass into undercounting 28 instead of 48).

Before the fix, the engine returned the VERTICAL MIRROR of the true hexagram for
all 48 hexagrams containing a non-palindromic trigram (Zhèn/Gèn/Xùn/Duì).
After the fix, all 64 map to their canonical King Wen number.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from cast_hexagram import Hexagram, Line, TRIGRAMS, cast_hexagram  # noqa: E402

# Trigram binaries BOTTOM->top, from the line-figures (no hand-typed hexagram patterns):
_TRI = {"Qian": (1, 1, 1), "Kun": (0, 0, 0), "Zhen": (1, 0, 0), "Gen": (0, 0, 1),
        "Kan": (0, 1, 0), "Li": (1, 0, 1), "Xun": (0, 1, 1), "Dui": (1, 1, 0)}
# Standard (lower, upper) -> King Wen number pairing:
_PAIR = {
    ("Qian", "Qian"): 1, ("Kun", "Kun"): 2, ("Zhen", "Kan"): 3, ("Kan", "Gen"): 4,
    ("Qian", "Kan"): 5, ("Kan", "Qian"): 6, ("Kan", "Kun"): 7, ("Kun", "Kan"): 8,
    ("Qian", "Xun"): 9, ("Dui", "Qian"): 10, ("Qian", "Kun"): 11, ("Kun", "Qian"): 12,
    ("Li", "Qian"): 13, ("Qian", "Li"): 14, ("Gen", "Kun"): 15, ("Kun", "Zhen"): 16,
    ("Zhen", "Dui"): 17, ("Xun", "Gen"): 18, ("Dui", "Kun"): 19, ("Kun", "Xun"): 20,
    ("Zhen", "Li"): 21, ("Li", "Gen"): 22, ("Kun", "Gen"): 23, ("Zhen", "Kun"): 24,
    ("Zhen", "Qian"): 25, ("Qian", "Gen"): 26, ("Zhen", "Gen"): 27, ("Xun", "Dui"): 28,
    ("Kan", "Kan"): 29, ("Li", "Li"): 30, ("Gen", "Dui"): 31, ("Xun", "Zhen"): 32,
    ("Gen", "Qian"): 33, ("Qian", "Zhen"): 34, ("Kun", "Li"): 35, ("Li", "Kun"): 36,
    ("Li", "Xun"): 37, ("Dui", "Li"): 38, ("Gen", "Kan"): 39, ("Kan", "Zhen"): 40,
    ("Dui", "Gen"): 41, ("Zhen", "Xun"): 42, ("Qian", "Dui"): 43, ("Xun", "Qian"): 44,
    ("Kun", "Dui"): 45, ("Xun", "Kun"): 46, ("Kan", "Dui"): 47, ("Xun", "Kan"): 48,
    ("Li", "Dui"): 49, ("Xun", "Li"): 50, ("Zhen", "Zhen"): 51, ("Gen", "Gen"): 52,
    ("Gen", "Xun"): 53, ("Dui", "Zhen"): 54, ("Li", "Zhen"): 55, ("Gen", "Li"): 56,
    ("Xun", "Xun"): 57, ("Dui", "Dui"): 58, ("Kan", "Xun"): 59, ("Dui", "Kan"): 60,
    ("Dui", "Xun"): 61, ("Gen", "Zhen"): 62, ("Li", "Kan"): 63, ("Kan", "Li"): 64,
}
_CANON = {(_TRI[lo] + _TRI[up]): n for (lo, up), n in _PAIR.items()}


def test_canonical_pairing_is_bijective():
    """Sanity on the oracle itself: 64 unique patterns -> exactly 1..64."""
    assert len(_CANON) == 64
    assert sorted(_CANON.values()) == list(range(1, 65))


def test_all_64_hexagram_numbers_canonical():
    """Every line-pattern must map to its true King Wen number."""
    wrong = []
    for p in range(64):
        b2t = tuple((p >> i) & 1 for i in range(6))
        lines = [Line(value=(7 if b else 8), position=i + 1) for i, b in enumerate(b2t)]
        got = Hexagram(lines=lines).number
        want = _CANON[b2t]
        if got != want:
            wrong.append((b2t, got, want))
    assert not wrong, f"{len(wrong)}/64 hexagrams misidentified: {wrong[:5]}..."


def test_nonpalindromic_trigrams_named_correctly():
    assert TRIGRAMS[(1, 0, 0)]["name"].startswith("Zh"), "(1,0,0) bottom->top must be Zhèn (Thunder)"
    assert TRIGRAMS[(0, 0, 1)]["name"].startswith("G"), "(0,0,1) bottom->top must be Gèn (Mountain)"
    assert TRIGRAMS[(0, 1, 1)]["name"].startswith("X"), "(0,1,1) bottom->top must be Xùn (Wind)"
    assert TRIGRAMS[(1, 1, 0)]["name"].startswith("D"), "(1,1,0) bottom->top must be Duì (Lake)"


def test_known_hexagrams_by_name():
    """Spot-check the famously-confused mirror pairs land right."""
    def num(b2t):
        lines = [Line(value=(7 if b else 8), position=i + 1) for i, b in enumerate(b2t)]
        return Hexagram(lines=lines).number
    assert num((1, 1, 1, 1, 1, 0)) == 43   # five yang, yin on top = Guài (was misread as 9)
    assert num((1, 1, 1, 0, 1, 1)) == 9    # Xiǎo Xù: Xùn (upper) over Qián (lower)
    assert num((0, 1, 1, 1, 1, 1)) == 44   # Gòu: Qián (upper) over Xùn (lower) — the mirror of 9
    assert num((1, 0, 0, 1, 0, 0)) == 51   # doubled Zhèn (was misread as 52)
    assert num((0, 0, 1, 0, 0, 1)) == 52   # doubled Gèn


def test_question_seed_is_reproducible():
    """Same question must yield the same cast (the documented contract)."""
    a = cast_hexagram(question="Will the harvest be good?", method="yarrow")
    b = cast_hexagram(question="Will the harvest be good?", method="yarrow")
    assert a.seed == b.seed, "same question must produce the same seed"
    assert [l.value for l in a.lines] == [l.value for l in b.lines], \
        "same question must produce the same cast"
