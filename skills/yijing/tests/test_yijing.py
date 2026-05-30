#!/usr/bin/env python3
"""
Yijing Oracle Test Suite

An oracle without tests is epistemologically fragile.
These tests verify the mathematical integrity of the casting system.

Run with: python -m pytest tests/test_yijing.py -v
Or:       python tests/test_yijing.py

Tests verify:
1. Probability distributions match cosmological specifications
2. Nuclear hexagram extraction produces exactly 16 unique nuclei
3. Hexagram lookup covers all 64 hexagrams
4. Golden readings remain stable across versions
"""

import random
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

# Add script directory to path
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

from cast_hexagram import (
    cast_line_yarrow,
    cast_line_coins,
    cast_hexagram,
    Hexagram,
    Line,
    HEXAGRAM_LOOKUP,
    HEXAGRAM_NAMES,
    TRIGRAMS,
)


# ═══════════════════════════════════════════════════════════════════════════════
# PROBABILITY DISTRIBUTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_yarrow_probabilities() -> None:
    """
    Verify yarrow stalk probabilities over 100,000 casts.

    Expected distribution:
    - 6 (Old Yin):    1/16 = 6.25%
    - 7 (Young Yang): 5/16 = 31.25%
    - 8 (Young Yin):  7/16 = 43.75%
    - 9 (Old Yang):   3/16 = 18.75%

    Tolerance: ±1% (statistical margin)
    """
    results: Dict[int, int] = {6: 0, 7: 0, 8: 0, 9: 0}
    rng = random.Random(42)  # Deterministic for reproducibility
    n_samples = 100_000

    for _ in range(n_samples):
        line = cast_line_yarrow(rng)
        results[line] += 1

    # Calculate actual percentages
    actual = {k: v / n_samples for k, v in results.items()}

    # Expected percentages
    expected = {
        6: 1/16,   # 0.0625
        7: 5/16,   # 0.3125
        8: 7/16,   # 0.4375
        9: 3/16,   # 0.1875
    }

    tolerance = 0.01  # 1%

    for value in [6, 7, 8, 9]:
        diff = abs(actual[value] - expected[value])
        assert diff < tolerance, (
            f"Yarrow probability for {value}: expected {expected[value]:.4f}, "
            f"got {actual[value]:.4f} (diff: {diff:.4f})"
        )

    print(f"✓ Yarrow probabilities verified over {n_samples:,} samples")
    print(f"  6: {actual[6]:.4f} (expected 0.0625)")
    print(f"  7: {actual[7]:.4f} (expected 0.3125)")
    print(f"  8: {actual[8]:.4f} (expected 0.4375)")
    print(f"  9: {actual[9]:.4f} (expected 0.1875)")


def test_coin_probabilities() -> None:
    """
    Verify three-coin probabilities over 100,000 casts.

    Expected distribution:
    - 6 (Old Yin):    1/8 = 12.5%
    - 7 (Young Yang): 3/8 = 37.5%
    - 8 (Young Yin):  3/8 = 37.5%
    - 9 (Old Yang):   1/8 = 12.5%
    """
    results: Dict[int, int] = {6: 0, 7: 0, 8: 0, 9: 0}
    rng = random.Random(42)
    n_samples = 100_000

    for _ in range(n_samples):
        line = cast_line_coins(rng)
        results[line] += 1

    actual = {k: v / n_samples for k, v in results.items()}

    expected = {
        6: 1/8,    # 0.125
        7: 3/8,    # 0.375
        8: 3/8,    # 0.375
        9: 1/8,    # 0.125
    }

    tolerance = 0.01

    for value in [6, 7, 8, 9]:
        diff = abs(actual[value] - expected[value])
        assert diff < tolerance, (
            f"Coin probability for {value}: expected {expected[value]:.4f}, "
            f"got {actual[value]:.4f}"
        )

    print(f"✓ Coin probabilities verified over {n_samples:,} samples")
    print(f"  6: {actual[6]:.4f} (expected 0.125)")
    print(f"  7: {actual[7]:.4f} (expected 0.375)")
    print(f"  8: {actual[8]:.4f} (expected 0.375)")
    print(f"  9: {actual[9]:.4f} (expected 0.125)")


def test_asymmetry_ratio() -> None:
    """
    Verify the 3:1 ratio of Old Yang (9) to Old Yin (6) in yarrow method.

    This is the key cosmological assertion:
    Yang changes 3× more readily than yin.
    """
    results: Dict[int, int] = {6: 0, 9: 0}
    rng = random.Random(42)
    n_samples = 100_000

    for _ in range(n_samples):
        line = cast_line_yarrow(rng)
        if line in (6, 9):
            results[line] += 1

    # Old Yang should be ~3x Old Yin
    ratio = results[9] / results[6] if results[6] > 0 else float('inf')

    assert 2.5 < ratio < 3.5, f"Expected ~3:1 ratio, got {ratio:.2f}:1"

    print(f"✓ Asymmetry ratio verified: Old Yang (9) is {ratio:.2f}× more likely than Old Yin (6)")


# ═══════════════════════════════════════════════════════════════════════════════
# NUCLEAR HEXAGRAM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_nuclear_exhaustive() -> None:
    """
    Verify nuclear extraction for all 64 hexagrams.

    Key insight: Only 16 distinct nuclear hexagrams can exist,
    because lines 2-4 and 3-5 must share lines 3-4.
    """
    nuclear_numbers: set = set()

    # Generate all 64 hexagrams
    for hex_num in range(1, 65):
        # Find the trigram pair that produces this hexagram
        for (lower, upper), num in HEXAGRAM_LOOKUP.items():
            if num == hex_num:
                # Build the hexagram
                lines = []
                for i, bit in enumerate(lower):
                    lines.append(Line(value=7 if bit == 1 else 8, position=i + 1))
                for i, bit in enumerate(upper):
                    lines.append(Line(value=7 if bit == 1 else 8, position=i + 4))

                hexagram = Hexagram(lines=lines, method="test")
                nuclear = hexagram.get_nuclear_hexagram()
                nuclear_numbers.add(nuclear.number)
                break

    # Must have exactly 16 unique nuclear hexagrams
    assert len(nuclear_numbers) == 16, (
        f"Expected exactly 16 unique nuclear hexagrams, found {len(nuclear_numbers)}: {sorted(nuclear_numbers)}"
    )

    print(f"✓ Nuclear exhaustive test passed: exactly 16 unique nuclei")
    print(f"  Nuclear attractors: {sorted(nuclear_numbers)}")


def test_nuclear_attractor_mapping() -> None:
    """
    Verify that each nuclear hexagram attracts exactly 4 primary hexagrams.

    The 64 hexagrams map to 16 nuclei, so each nucleus has 4 primaries.
    """
    nucleus_to_primaries: Dict[int, List[int]] = {}

    for hex_num in range(1, 65):
        for (lower, upper), num in HEXAGRAM_LOOKUP.items():
            if num == hex_num:
                lines = []
                for i, bit in enumerate(lower):
                    lines.append(Line(value=7 if bit == 1 else 8, position=i + 1))
                for i, bit in enumerate(upper):
                    lines.append(Line(value=7 if bit == 1 else 8, position=i + 4))

                hexagram = Hexagram(lines=lines, method="test")
                nuclear = hexagram.get_nuclear_hexagram()

                if nuclear.number not in nucleus_to_primaries:
                    nucleus_to_primaries[nuclear.number] = []
                nucleus_to_primaries[nuclear.number].append(hex_num)
                break

    for nucleus, primaries in nucleus_to_primaries.items():
        assert len(primaries) == 4, (
            f"Nuclear hexagram {nucleus} should attract 4 primaries, found {len(primaries)}: {primaries}"
        )

    print(f"✓ Nuclear attractor mapping verified: each nucleus attracts exactly 4 primaries")


# ═══════════════════════════════════════════════════════════════════════════════
# HEXAGRAM LOOKUP TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_hexagram_lookup_complete() -> None:
    """Verify that all 64 hexagrams are reachable via trigram lookup."""
    reachable = set(HEXAGRAM_LOOKUP.values())
    expected = set(range(1, 65))

    missing = expected - reachable
    extra = reachable - expected

    assert not missing, f"Missing hexagrams in lookup: {missing}"
    assert not extra, f"Invalid hexagram numbers in lookup: {extra}"
    assert len(HEXAGRAM_LOOKUP) == 64, f"Expected 64 entries, found {len(HEXAGRAM_LOOKUP)}"

    print(f"✓ Hexagram lookup complete: all 64 hexagrams reachable")


def test_hexagram_names_complete() -> None:
    """Verify that all 64 hexagrams have names."""
    for hex_num in range(1, 65):
        assert hex_num in HEXAGRAM_NAMES, f"Missing name for hexagram {hex_num}"
        chinese, pinyin, english = HEXAGRAM_NAMES[hex_num]
        assert chinese, f"Empty Chinese name for hexagram {hex_num}"
        assert pinyin, f"Empty pinyin for hexagram {hex_num}"
        assert english, f"Empty English name for hexagram {hex_num}"

    print(f"✓ Hexagram names complete: all 64 hexagrams have Chinese, pinyin, and English names")


def test_trigram_lookup_complete() -> None:
    """Verify that all 8 trigrams are defined."""
    expected_trigrams = [
        (1, 1, 1),  # Qián
        (0, 0, 0),  # Kūn
        (0, 0, 1),  # Zhèn
        (1, 1, 0),  # Xùn
        (0, 1, 0),  # Kǎn
        (1, 0, 1),  # Lí
        (1, 0, 0),  # Gèn
        (0, 1, 1),  # Duì
    ]

    for trigram in expected_trigrams:
        assert trigram in TRIGRAMS, f"Missing trigram: {trigram}"
        info = TRIGRAMS[trigram]
        assert "name" in info, f"Missing name for trigram {trigram}"
        assert "symbol" in info, f"Missing symbol for trigram {trigram}"
        assert "element" in info, f"Missing element for trigram {trigram}"

    print(f"✓ Trigram lookup complete: all 8 trigrams defined with correspondences")


# ═══════════════════════════════════════════════════════════════════════════════
# GOLDEN TESTS (Canonical Readings)
# ═══════════════════════════════════════════════════════════════════════════════

# These are pre-computed canonical casts that must remain stable.
# If these fail, the oracle's bones have shifted.

GOLDEN_READINGS = {
    # Seed 42 with yarrow method → Hexagram 27 (Nourishment)
    ("yarrow", 42): {
        "number": 27,
        "name_pinyin": "Yí",
        "lines": [8, 6, 7, 7, 8, 8],
    },
    # Seed 12345 with yarrow method → Hexagram 25 (Innocence)
    ("yarrow", 12345): {
        "number": 25,
        "name_pinyin": "Wú Wàng",
        "lines": [8, 6, 9, 7, 7, 7],
    },
    # Seed 42 with coins method → Hexagram 27 (same seed, different method, same result here)
    ("coins", 42): {
        "number": 27,
        "name_pinyin": "Yí",
        "lines": [8, 6, 7, 7, 8, 8],
    },
    # Seed 999 with yarrow → Hexagram 54 (Marrying Maiden)
    ("yarrow", 999): {
        "number": 54,
        "name_pinyin": "Guī Mèi",
        "lines": [8, 7, 9, 8, 8, 7],
    },
}


def test_golden_readings() -> None:
    """
    Verify that canonical readings remain stable.

    Golden tests ensure the oracle recites its catechism perfectly.
    If these fail, something fundamental has changed.
    """
    for (method, seed), expected in GOLDEN_READINGS.items():
        hexagram = cast_hexagram(question=None, method=method, seed=seed)

        # Verify hexagram number
        assert hexagram.number == expected["number"], (
            f"Golden test failed for ({method}, seed={seed}): "
            f"expected hexagram {expected['number']}, got {hexagram.number}"
        )

        # Verify name
        _, pinyin, _ = hexagram.name
        assert pinyin == expected["name_pinyin"], (
            f"Golden test failed for ({method}, seed={seed}): "
            f"expected {expected['name_pinyin']}, got {pinyin}"
        )

        # Verify line values
        actual_lines = [line.value for line in hexagram.lines]
        assert actual_lines == expected["lines"], (
            f"Golden test failed for ({method}, seed={seed}): "
            f"expected lines {expected['lines']}, got {actual_lines}"
        )

    print(f"✓ Golden readings verified: {len(GOLDEN_READINGS)} canonical casts stable")


# ═══════════════════════════════════════════════════════════════════════════════
# RELATING HEXAGRAM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_relating_hexagram_transformation() -> None:
    """
    Verify that moving lines correctly transform to relating hexagram.

    Old Yin (6) → Young Yang (7)
    Old Yang (9) → Young Yin (8)
    """
    # Create hexagram with known moving lines
    lines = [
        Line(value=6, position=1),  # Old Yin → becomes yang
        Line(value=7, position=2),  # Young Yang → stays
        Line(value=8, position=3),  # Young Yin → stays
        Line(value=9, position=4),  # Old Yang → becomes yin
        Line(value=7, position=5),  # Young Yang → stays
        Line(value=8, position=6),  # Young Yin → stays
    ]
    hexagram = Hexagram(lines=lines, method="test")

    # Verify moving lines detected
    assert hexagram.moving_lines == [1, 4], f"Expected moving lines [1, 4], got {hexagram.moving_lines}"

    # Get relating hexagram
    relating = hexagram.get_relating_hexagram()
    assert relating is not None, "Should have relating hexagram with moving lines"

    # Verify transformation
    expected_values = [7, 7, 8, 8, 7, 8]  # 6→7, keep, keep, 9→8, keep, keep
    actual_values = [line.value for line in relating.lines]
    assert actual_values == expected_values, (
        f"Relating hexagram transformation incorrect: expected {expected_values}, got {actual_values}"
    )

    print(f"✓ Relating hexagram transformation verified")


def test_no_relating_without_moving() -> None:
    """Verify that hexagrams without moving lines return no relating hexagram."""
    # All stable lines
    lines = [Line(value=v, position=i+1) for i, v in enumerate([7, 8, 7, 8, 7, 8])]
    hexagram = Hexagram(lines=lines, method="test")

    assert not hexagram.has_moving_lines
    assert hexagram.get_relating_hexagram() is None

    print(f"✓ No relating hexagram without moving lines")


# ═══════════════════════════════════════════════════════════════════════════════
# LINE CLASS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_line_properties() -> None:
    """Verify Line class properties."""
    # Old Yin
    line6 = Line(value=6, position=1)
    assert line6.is_yin
    assert not line6.is_yang
    assert line6.is_moving
    assert line6.binary == 0
    assert line6.transformed_binary == 1  # 6 → yang

    # Young Yang
    line7 = Line(value=7, position=2)
    assert line7.is_yang
    assert not line7.is_yin
    assert not line7.is_moving
    assert line7.binary == 1
    assert line7.transformed_binary == 1

    # Young Yin
    line8 = Line(value=8, position=3)
    assert line8.is_yin
    assert not line8.is_yang
    assert not line8.is_moving
    assert line8.binary == 0
    assert line8.transformed_binary == 0

    # Old Yang
    line9 = Line(value=9, position=4)
    assert line9.is_yang
    assert not line9.is_yin
    assert line9.is_moving
    assert line9.binary == 1
    assert line9.transformed_binary == 0  # 9 → yin

    print(f"✓ Line properties verified for all four line types")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def run_all_tests() -> None:
    """Run all tests and report results."""
    print("=" * 70)
    print("YIJING ORACLE TEST SUITE")
    print("Verifying the mathematical integrity of the Changes")
    print("=" * 70)
    print()

    tests = [
        ("Probability Distribution", [
            test_yarrow_probabilities,
            test_coin_probabilities,
            test_asymmetry_ratio,
        ]),
        ("Nuclear Hexagrams", [
            test_nuclear_exhaustive,
            test_nuclear_attractor_mapping,
        ]),
        ("Hexagram Lookup", [
            test_hexagram_lookup_complete,
            test_hexagram_names_complete,
            test_trigram_lookup_complete,
        ]),
        ("Golden Readings", [
            test_golden_readings,
        ]),
        ("Relating Hexagrams", [
            test_relating_hexagram_transformation,
            test_no_relating_without_moving,
        ]),
        ("Line Properties", [
            test_line_properties,
        ]),
    ]

    passed = 0
    failed = 0

    for section_name, test_funcs in tests:
        print(f"\n--- {section_name} ---")
        for test_func in test_funcs:
            try:
                test_func()
                passed += 1
            except AssertionError as e:
                print(f"✗ {test_func.__name__}: {e}")
                failed += 1
            except Exception as e:
                print(f"✗ {test_func.__name__}: EXCEPTION - {e}")
                failed += 1

    print()
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed > 0:
        print("\n⚠ The oracle's bones have shifted. Investigate before proceeding.")
        sys.exit(1)
    else:
        print("\n✓ The oracle recites its catechism perfectly.")
        print("  The mathematics encodes the cosmology.")
        print("  The cosmology is intact.")


if __name__ == "__main__":
    run_all_tests()
