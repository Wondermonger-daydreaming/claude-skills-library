#!/usr/bin/env python3
"""
Hexagram Relations Test Suite

Tests verify the mathematical integrity of the hexagram transformation algebra:
- Cuogua (錯卦): Binary complement — XOR with 0b111111
- Zonggua (綜卦): Vertical flip — reverse line order
- Jiaogua (交卦): Trigram exchange — swap upper/lower trigrams
- Hugua (互卦): Nuclear extraction — lines 2-3-4 and 3-4-5

Run with: python -m pytest .claude/skills/yijing/tests/test_relations.py -v
Or:       python .claude/skills/yijing/tests/test_relations.py
"""

import sys
from pathlib import Path

# Add script directory to path
script_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(script_dir))

from hexagram_relations import (
    HexagramRelations,
    make_hexagram_by_number,
    get_all_relations,
    hexagram_to_binary,
    binary_to_hexagram,
    reverse_bits,
    swap_trigrams,
    complement_bits,
    SYMMETRIC_HEXAGRAMS,
    DOUBLED_TRIGRAM_HEXAGRAMS,
)


# ═══════════════════════════════════════════════════════════════════════════════
# BINARY OPERATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_complement_involution() -> None:
    """
    Verify cuogua is an involution: complement(complement(x)) == x.

    This is fundamental group theory: cuogua is its own inverse.
    """
    for binary in range(64):  # All 6-bit values
        doubled = complement_bits(complement_bits(binary))
        assert doubled == binary, f"Double complement failed: {binary:06b} → {complement_bits(binary):06b} → {doubled:06b}"

    print("✓ Cuogua involution verified: complement(complement(x)) = x for all 64 hexagrams")


def test_reverse_involution() -> None:
    """
    Verify zonggua is an involution: reverse(reverse(x)) == x.

    Flipping upside-down twice returns to original.
    """
    for binary in range(64):
        doubled = reverse_bits(reverse_bits(binary))
        assert doubled == binary, f"Double reverse failed: {binary:06b}"

    print("✓ Zonggua involution verified: reverse(reverse(x)) = x for all 64 hexagrams")


def test_swap_involution() -> None:
    """
    Verify jiaogua is an involution: swap(swap(x)) == x.

    Swapping trigrams twice returns to original.
    """
    for binary in range(64):
        doubled = swap_trigrams(swap_trigrams(binary))
        assert doubled == binary, f"Double swap failed: {binary:06b}"

    print("✓ Jiaogua involution verified: swap(swap(x)) = x for all 64 hexagrams")


# ═══════════════════════════════════════════════════════════════════════════════
# SYMMETRIC HEXAGRAM TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_symmetric_hexagrams() -> None:
    """
    Verify the 8 symmetric hexagrams where zonggua = self.

    These are hexagrams whose binary pattern reads the same forwards and backwards:
    1 (乾): 111111, 2 (坤): 000000, 27 (頤): 001100, 28 (大過): 110011
    29 (坎): 010010, 30 (離): 101101, 61 (中孚): 110110, 62 (小過): 001001
    """
    expected_symmetric = {1, 2, 27, 28, 29, 30, 61, 62}

    actual_symmetric = set()
    for num in range(1, 65):
        hexagram = make_hexagram_by_number(num)
        if hexagram:
            binary = hexagram_to_binary(hexagram)
            reversed_binary = reverse_bits(binary)
            if binary == reversed_binary:
                actual_symmetric.add(num)

    assert actual_symmetric == expected_symmetric, (
        f"Symmetric hexagrams mismatch!\n"
        f"Expected: {expected_symmetric}\n"
        f"Actual: {actual_symmetric}\n"
        f"Missing: {expected_symmetric - actual_symmetric}\n"
        f"Extra: {actual_symmetric - expected_symmetric}"
    )

    # Also verify the constant matches
    assert SYMMETRIC_HEXAGRAMS == expected_symmetric

    print(f"✓ 8 symmetric hexagrams verified: {sorted(expected_symmetric)}")


def test_doubled_trigram_hexagrams() -> None:
    """
    Verify the 8 doubled-trigram hexagrams where jiaogua = self.

    These have identical upper and lower trigrams:
    1 (乾 over 乾), 2 (坤 over 坤), 29 (坎 over 坎), 30 (離 over 離)
    51 (震 over 震), 52 (艮 over 艮), 57 (巽 over 巽), 58 (兌 over 兌)
    """
    expected_doubled = {1, 2, 29, 30, 51, 52, 57, 58}

    actual_doubled = set()
    for num in range(1, 65):
        hexagram = make_hexagram_by_number(num)
        if hexagram:
            binary = hexagram_to_binary(hexagram)
            swapped = swap_trigrams(binary)
            if binary == swapped:
                actual_doubled.add(num)

    assert actual_doubled == expected_doubled, (
        f"Doubled-trigram hexagrams mismatch!\n"
        f"Expected: {expected_doubled}\n"
        f"Actual: {actual_doubled}"
    )

    assert DOUBLED_TRIGRAM_HEXAGRAMS == expected_doubled

    print(f"✓ 8 doubled-trigram hexagrams verified: {sorted(expected_doubled)}")


# ═══════════════════════════════════════════════════════════════════════════════
# HEXAGRAM RELATIONS CLASS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_all_64_produce_valid_relations() -> None:
    """
    Every hexagram should produce valid relations.
    """
    for num in range(1, 65):
        relations = get_all_relations(num)
        assert relations is not None, f"Failed to create relations for hexagram {num}"

        # All derived hexagrams should have valid King Wen numbers
        assert 1 <= relations.cuogua.number <= 64, f"Invalid cuogua for {num}"
        assert 1 <= relations.zonggua.number <= 64, f"Invalid zonggua for {num}"
        assert 1 <= relations.jiaogua.number <= 64, f"Invalid jiaogua for {num}"
        assert 1 <= relations.hugua.number <= 64, f"Invalid hugua for {num}"
        assert 1 <= relations.king_wen_pair.number <= 64, f"Invalid pair for {num}"

    print("✓ All 64 hexagrams produce valid relations")


def test_cuogua_specific_cases() -> None:
    """
    Verify specific cuogua (complement) relationships.

    - Hexagram 1 (all yang) ↔ Hexagram 2 (all yin)
    - Hexagram 11 (泰 Peace) ↔ Hexagram 12 (否 Stagnation)
    - Hexagram 27 (頤) ↔ Hexagram 28 (大過)
    """
    test_cases = [
        (1, 2),    # Qian ↔ Kun
        (11, 12),  # Tai ↔ Pi
        (27, 28),  # Yi ↔ Da Guo
        (29, 30),  # Kan ↔ Li
        (63, 64),  # Ji Ji ↔ Wei Ji
    ]

    for a, b in test_cases:
        rel_a = get_all_relations(a)
        rel_b = get_all_relations(b)

        assert rel_a.cuogua.number == b, f"cuogua({a}) should be {b}, got {rel_a.cuogua.number}"
        assert rel_b.cuogua.number == a, f"cuogua({b}) should be {a}, got {rel_b.cuogua.number}"

    print("✓ Cuogua specific cases verified (1↔2, 11↔12, 27↔28, 29↔30, 63↔64)")


def test_zonggua_symmetric() -> None:
    """
    Symmetric hexagrams should have zonggua = self.
    """
    for num in SYMMETRIC_HEXAGRAMS:
        relations = get_all_relations(num)
        assert relations.zonggua.number == num, (
            f"Symmetric hexagram {num} should have zonggua=self, got {relations.zonggua.number}"
        )
        assert relations.is_symmetric == True

    print(f"✓ All 8 symmetric hexagrams have zonggua = self")


def test_jiaogua_doubled() -> None:
    """
    Doubled-trigram hexagrams should have jiaogua = self.
    """
    for num in DOUBLED_TRIGRAM_HEXAGRAMS:
        relations = get_all_relations(num)
        assert relations.jiaogua.number == num, (
            f"Doubled hexagram {num} should have jiaogua=self, got {relations.jiaogua.number}"
        )
        assert relations.is_doubled == True

    print(f"✓ All 8 doubled-trigram hexagrams have jiaogua = self")


def test_king_wen_pairing() -> None:
    """
    King Wen pairs:
    - For symmetric hexagrams: pair is cuogua
    - For non-symmetric hexagrams: pair is zonggua
    """
    for num in range(1, 65):
        relations = get_all_relations(num)

        if num in SYMMETRIC_HEXAGRAMS:
            assert relations.king_wen_pair.number == relations.cuogua.number, (
                f"Symmetric {num} should pair via cuogua"
            )
        else:
            assert relations.king_wen_pair.number == relations.zonggua.number, (
                f"Non-symmetric {num} should pair via zonggua"
            )

    print("✓ King Wen pairing logic verified for all 64 hexagrams")


def test_binary_representation() -> None:
    """
    Verify binary conversion is consistent.

    Binary encoding: Line 1 = bit 0 (LSB), Line 6 = bit 5 (MSB)
    Lower trigram (lines 1-2-3) occupies lower 3 bits.
    Upper trigram (lines 4-5-6) occupies upper 3 bits.

    Hexagram 1 (Qian): 111111 — all yang
    Hexagram 2 (Kun):  000000 — all yin
    Hexagram 11 (Tai): 000111 — Heaven below (111), Earth above (000)
    Hexagram 12 (Pi):  111000 — Earth below (000), Heaven above (111)
    """
    test_cases = [
        (1, 0b111111),   # Qian: all yang
        (2, 0b000000),   # Kun: all yin
        (11, 0b000111),  # Tai: yang lower (111), yin upper (000) — Heaven BELOW Earth
        (12, 0b111000),  # Pi: yin lower (000), yang upper (111) — Earth BELOW Heaven
    ]

    for num, expected_binary in test_cases:
        hexagram = make_hexagram_by_number(num)
        actual = hexagram_to_binary(hexagram)
        assert actual == expected_binary, (
            f"Hexagram {num}: expected {expected_binary:06b}, got {actual:06b}"
        )

    print("✓ Binary representation verified for golden cases")


def test_line_distance() -> None:
    """
    Test Hamming distance between hexagrams.

    - Hexagram 1 to 2: 6 lines different (complete opposite)
    - Any hexagram to itself: 0
    - Symmetric hexagram to its cuogua: 6 (they're opposites)
    """
    rel_1 = get_all_relations(1)
    rel_2 = get_all_relations(2)

    # Complete opposites
    assert rel_1.line_distance_to(rel_2) == 6

    # Self distance
    assert rel_1.line_distance_to(rel_1) == 0

    # Hexagram 11 to 12: complement, so 6 lines different
    rel_11 = get_all_relations(11)
    rel_12 = get_all_relations(12)
    assert rel_11.line_distance_to(rel_12) == 6

    print("✓ Line distance (Hamming distance) calculations verified")


def test_transformation_path() -> None:
    """
    Test the transformation_path method that identifies which single transformation reaches target.
    """
    rel_1 = get_all_relations(1)
    rel_2 = get_all_relations(2)

    path = rel_1.transformation_path(rel_2)
    assert path['cuogua'] == True, "1 → 2 should be via cuogua"
    assert path['zonggua'] == False, "1 → 2 is not via zonggua (1 is symmetric)"
    assert path['same'] == False

    # Hexagram 1 is symmetric: zonggua leads to self
    path_self = rel_1.transformation_path(rel_1)
    assert path_self['zonggua'] == True  # Because 1 is symmetric
    assert path_self['same'] == True

    print("✓ Transformation path detection verified")


# ═══════════════════════════════════════════════════════════════════════════════
# TO_DICT AND TO_ASCII TESTS
# ═══════════════════════════════════════════════════════════════════════════════

def test_to_dict_structure() -> None:
    """
    Verify to_dict() produces expected structure.
    """
    relations = get_all_relations(27)  # Yi - Nourishment (symmetric)
    data = relations.to_dict()

    # Check top-level structure
    assert 'primary' in data
    assert 'is_symmetric' in data
    assert 'is_doubled' in data
    assert 'relationships' in data

    # Check relationships
    for rel_type in ['cuogua', 'zonggua', 'jiaogua', 'hugua', 'king_wen_pair']:
        assert rel_type in data['relationships']
        rel = data['relationships'][rel_type]
        assert 'number' in rel
        assert 'name' in rel

    # Hexagram 27 should be symmetric but not doubled
    assert data['is_symmetric'] == True
    assert data['is_doubled'] == False

    print("✓ to_dict() structure verified")


def test_to_ascii_output() -> None:
    """
    Verify to_ascii() produces non-empty string with expected markers.
    """
    relations = get_all_relations(11)
    ascii_output = relations.to_ascii()

    assert len(ascii_output) > 0
    assert "HEXAGRAM RELATIONSHIPS" in ascii_output
    assert "CUOGUA" in ascii_output
    assert "ZONGGUA" in ascii_output
    assert "JIAOGUA" in ascii_output
    assert "HUGUA" in ascii_output
    assert "KING WEN PAIR" in ascii_output

    print("✓ to_ascii() output structure verified")


# ═══════════════════════════════════════════════════════════════════════════════
# GOLDEN TEST: FIXED HEXAGRAM
# ═══════════════════════════════════════════════════════════════════════════════

def test_hexagram_11_golden() -> None:
    """
    Golden test for Hexagram 11 (泰 Tai - Peace).

    Binary: 000111 (Heaven/Qian below = 111, Earth/Kun above = 000)
    Line 1 = bit 0 (LSB), so lower trigram occupies lower 3 bits.

    Expected relations:
    - Cuogua: 12 (否 Pi - Stagnation) — complement: 111000
    - Zonggua: 12 (否 Pi) — flipped: 111000 (same as cuogua for this pair!)
    - Jiaogua: 12 (否 Pi) — swapped trigrams (also 12! swapping Heaven↔Earth = 11↔12)
    - Hugua: 54 (歸妹 Guī Mèi) — nuclear: lines 2-3-4 = ☱ Duì, lines 3-4-5 = ☳ Zhèn

    Remarkable: Hexagrams 11 and 12 are related by cuogua, zonggua, AND jiaogua!
    They are the archetypal pair: Peace and Stagnation, Heaven-Earth exchanged.
    """
    relations = get_all_relations(11)

    # Verify binary: Heaven (111) below, Earth (000) above
    assert relations.binary == 0b000111, f"Binary should be 000111, got {relations.binary:06b}"

    # Verify transformations — 11 and 12 are related by ALL three primary transformations!
    assert relations.cuogua.number == 12, f"Cuogua should be 12, got {relations.cuogua.number}"
    assert relations.zonggua.number == 12, f"Zonggua should be 12, got {relations.zonggua.number}"
    assert relations.jiaogua.number == 12, f"Jiaogua should be 12, got {relations.jiaogua.number}"
    assert relations.hugua.number == 54, f"Hugua should be 54, got {relations.hugua.number}"

    # Hexagram 11 is not symmetric (111000 reversed is 000111, different)
    assert relations.is_symmetric == False

    # King Wen pair should be zonggua for non-symmetric
    assert relations.king_wen_pair.number == 12

    print("✓ Hexagram 11 (泰 Tai) golden test passed")
    print("  Binary: 000111 (Heaven below, Earth above)")
    print("  Cuogua: 12 (否)")
    print("  Zonggua: 12 (否)")
    print("  Jiaogua: 12 (否) — all three transformations lead to the same place!")
    print("  Hugua: 54 (歸妹)")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("HEXAGRAM RELATIONS TEST SUITE")
    print("=" * 70)
    print()

    # Binary operation tests
    print("Binary Operations:")
    test_complement_involution()
    test_reverse_involution()
    test_swap_involution()
    print()

    # Symmetric/doubled hexagram tests
    print("Special Hexagram Sets:")
    test_symmetric_hexagrams()
    test_doubled_trigram_hexagrams()
    print()

    # HexagramRelations class tests
    print("HexagramRelations Class:")
    test_all_64_produce_valid_relations()
    test_cuogua_specific_cases()
    test_zonggua_symmetric()
    test_jiaogua_doubled()
    test_king_wen_pairing()
    test_binary_representation()
    test_line_distance()
    test_transformation_path()
    print()

    # Serialization tests
    print("Serialization:")
    test_to_dict_structure()
    test_to_ascii_output()
    print()

    # Golden tests
    print("Golden Tests:")
    test_hexagram_11_golden()
    print()

    print("=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
