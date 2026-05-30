#!/usr/bin/env python3
"""
Hexagram Relationships Algebra

Implements the four classical hexagram transformations:
- Cuogua (錯卦): Binary complement (opposite) - all lines inverted
- Zonggua (綜卦): Inverted/overturned - hexagram flipped upside-down
- Jiaogua (交卦): Exchanged - upper and lower trigrams swapped
- Hugua (互卦): Nuclear - lines 2-3-4 and 3-4-5 extracted

These transformations reveal the hidden relationships between hexagrams
and illuminate the deep structure of the Changes.
"""

from dataclasses import dataclass
from functools import cached_property
from typing import Optional, Dict, Any, List, Tuple

# Lazy imports to avoid circular dependency
# These will be populated on first use
_Hexagram = None
_Line = None
_HEXAGRAM_LOOKUP = None
_HEXAGRAM_NAMES = None


def _ensure_imports():
    """Lazy import from cast_hexagram to avoid circular dependency."""
    global _Hexagram, _Line, _HEXAGRAM_LOOKUP, _HEXAGRAM_NAMES
    if _Hexagram is None:
        from cast_hexagram import Hexagram, Line, HEXAGRAM_LOOKUP, HEXAGRAM_NAMES
        _Hexagram = Hexagram
        _Line = Line
        _HEXAGRAM_LOOKUP = HEXAGRAM_LOOKUP
        _HEXAGRAM_NAMES = HEXAGRAM_NAMES


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════════

# The 8 symmetric hexagrams (zonggua = self)
# These are paired by cuogua in the King Wen sequence
SYMMETRIC_HEXAGRAMS = {1, 2, 27, 28, 29, 30, 61, 62}

# The 8 doubled-trigram hexagrams (jiaogua = self)
# Upper and lower trigrams are identical
DOUBLED_TRIGRAM_HEXAGRAMS = {1, 2, 29, 30, 51, 52, 57, 58}


# ═══════════════════════════════════════════════════════════════════════════════
# BINARY OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def hexagram_to_binary(hexagram: 'Hexagram') -> int:
    """
    Convert hexagram to 6-bit binary representation.

    Line 1 (bottom) = bit 0 (LSB)
    Line 6 (top) = bit 5 (MSB)
    Yang (1) = 1, Yin (0) = 0
    """
    result = 0
    for i, line in enumerate(hexagram.lines):
        if line.is_yang:
            result |= (1 << i)
    return result


def binary_to_hexagram(binary: int, method: str = "derived"):
    """
    Convert 6-bit binary back to a Hexagram object.

    Creates stable lines (7 for yang, 8 for yin) - no moving lines.
    """
    _ensure_imports()
    lines = []
    for position in range(1, 7):
        bit = (binary >> (position - 1)) & 1
        value = 7 if bit == 1 else 8  # Stable lines
        lines.append(_Line(value=value, position=position))
    return _Hexagram(lines=lines, method=method)


def reverse_bits(binary: int) -> int:
    """
    Reverse the 6 bits (line 1↔6, 2↔5, 3↔4).

    This is the zonggua transformation at the binary level.
    """
    result = 0
    for i in range(6):
        if binary & (1 << i):
            result |= (1 << (5 - i))
    return result


def swap_trigrams(binary: int) -> int:
    """
    Swap upper 3 bits with lower 3 bits.

    This is the jiaogua transformation at the binary level.
    """
    lower = binary & 0b000111
    upper = (binary >> 3) & 0b000111
    return (lower << 3) | upper


def complement_bits(binary: int) -> int:
    """
    XOR with all 1s (binary complement).

    This is the cuogua transformation at the binary level.
    """
    return binary ^ 0b111111


# ═══════════════════════════════════════════════════════════════════════════════
# HEXAGRAM RELATIONS CLASS
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class HexagramRelations:
    """
    Computes all traditional hexagram relationships.

    Given a primary hexagram, computes:
    - Cuogua (錯卦): Binary complement (opposite)
    - Zonggua (綜卦): Vertical reversal (overturned)
    - Jiaogua (交卦): Trigram exchange (swapped)
    - Hugua (互卦): Nuclear extraction
    - King Wen pair (the sequence partner)

    Also provides:
    - Binary representation
    - Symmetry detection
    - Transformation distance calculations
    """

    primary: 'Hexagram'

    @property
    def binary(self) -> int:
        """6-bit binary representation of the hexagram."""
        return hexagram_to_binary(self.primary)

    @property
    def binary_str(self) -> str:
        """Binary as 6-character string (line 1 first)."""
        return format(self.binary, '06b')[::-1]  # Reverse for line 1 first

    @property
    def is_symmetric(self) -> bool:
        """True if hexagram is identical when inverted (zonggua = self)."""
        return self.primary.number in SYMMETRIC_HEXAGRAMS

    @property
    def is_doubled(self) -> bool:
        """True if upper and lower trigrams are identical (jiaogua = self)."""
        return self.primary.number in DOUBLED_TRIGRAM_HEXAGRAMS

    @cached_property
    def cuogua(self) -> 'Hexagram':
        """
        錯卦 - Complementary/Opposite hexagram.

        Every yin becomes yang, every yang becomes yin.
        Binary: XOR with 0b111111
        """
        complemented = complement_bits(self.binary)
        return binary_to_hexagram(complemented, method="cuogua")

    @cached_property
    def zonggua(self) -> 'Hexagram':
        """
        綜卦 - Inverted/Overturned hexagram.

        Flip the hexagram upside down (reverse line order).
        Returns same hexagram for the 8 symmetric hexagrams.
        """
        reversed_binary = reverse_bits(self.binary)
        return binary_to_hexagram(reversed_binary, method="zonggua")

    @cached_property
    def jiaogua(self) -> 'Hexagram':
        """
        交卦 - Exchanged hexagram.

        Swap upper and lower trigrams.
        Returns same hexagram for the 8 doubled-trigram hexagrams.
        """
        swapped = swap_trigrams(self.binary)
        return binary_to_hexagram(swapped, method="jiaogua")

    @property
    def hugua(self) -> 'Hexagram':
        """
        互卦 - Nuclear hexagram.

        Extract lines 2-3-4 and 3-4-5.
        Delegates to existing Hexagram.get_nuclear_hexagram().
        """
        return self.primary.get_nuclear_hexagram()

    @property
    def king_wen_pair(self) -> 'Hexagram':
        """
        The King Wen sequence partner.

        For 56 hexagrams: the zonggua (paired by inversion)
        For 8 symmetric hexagrams: the cuogua (paired by complementation)
        """
        if self.is_symmetric:
            return self.cuogua
        return self.zonggua

    @property
    def relating(self) -> Optional['Hexagram']:
        """
        The relating hexagram (if moving lines exist).

        Delegates to existing Hexagram.get_relating_hexagram().
        """
        return self.primary.get_relating_hexagram()

    def line_distance_to(self, other: 'HexagramRelations') -> int:
        """
        Count how many lines differ between two hexagrams.

        Returns the Hamming distance (number of bit flips needed).
        """
        return bin(self.binary ^ other.binary).count('1')

    def transformation_path(self, other: 'HexagramRelations') -> Dict[str, bool]:
        """
        Check which single transformations reach the target hexagram.

        Returns dict with transformation name -> True/False.
        """
        target = other.binary
        return {
            'cuogua': complement_bits(self.binary) == target,
            'zonggua': reverse_bits(self.binary) == target,
            'jiaogua': swap_trigrams(self.binary) == target,
            'hugua': self.hugua.number == other.primary.number,
            'same': self.binary == target,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize all relationships as a dictionary."""
        _ensure_imports()
        cuogua_name = _HEXAGRAM_NAMES.get(self.cuogua.number, ("?", "?", "?"))
        zonggua_name = _HEXAGRAM_NAMES.get(self.zonggua.number, ("?", "?", "?"))
        jiaogua_name = _HEXAGRAM_NAMES.get(self.jiaogua.number, ("?", "?", "?"))
        hugua_name = _HEXAGRAM_NAMES.get(self.hugua.number, ("?", "?", "?"))
        pair_name = _HEXAGRAM_NAMES.get(self.king_wen_pair.number, ("?", "?", "?"))

        return {
            'primary': {
                'number': self.primary.number,
                'binary': self.binary_str,
            },
            'is_symmetric': self.is_symmetric,
            'is_doubled': self.is_doubled,
            'relationships': {
                'cuogua': {
                    'number': self.cuogua.number,
                    'name': {'chinese': cuogua_name[0], 'pinyin': cuogua_name[1], 'english': cuogua_name[2]},
                    'description': 'Complementary (all lines inverted)',
                },
                'zonggua': {
                    'number': self.zonggua.number,
                    'name': {'chinese': zonggua_name[0], 'pinyin': zonggua_name[1], 'english': zonggua_name[2]},
                    'is_self': self.is_symmetric,
                    'description': 'Overturned (upside-down)',
                },
                'jiaogua': {
                    'number': self.jiaogua.number,
                    'name': {'chinese': jiaogua_name[0], 'pinyin': jiaogua_name[1], 'english': jiaogua_name[2]},
                    'is_self': self.is_doubled,
                    'description': 'Exchanged (trigrams swapped)',
                },
                'hugua': {
                    'number': self.hugua.number,
                    'name': {'chinese': hugua_name[0], 'pinyin': hugua_name[1], 'english': hugua_name[2]},
                    'description': 'Nuclear (lines 2-3-4 + 3-4-5)',
                },
                'king_wen_pair': {
                    'number': self.king_wen_pair.number,
                    'name': {'chinese': pair_name[0], 'pinyin': pair_name[1], 'english': pair_name[2]},
                    'pairing_type': 'cuogua' if self.is_symmetric else 'zonggua',
                },
            },
        }

    def to_ascii(self) -> str:
        """Generate ASCII visualization of all relationships."""
        _ensure_imports()
        lines = []

        # Header
        primary_name = _HEXAGRAM_NAMES.get(self.primary.number, ("?", "?", "?"))
        header = f"Hexagram {self.primary.number}: {primary_name[0]} {primary_name[1]}"
        lines.append("╔════════════════════════════════════════════════════════════════════════╗")
        lines.append(f"║                     HEXAGRAM RELATIONSHIPS                            ║")
        lines.append(f"║  {header.ljust(68)}  ║")
        lines.append("╠════════════════════════════════════════════════════════════════════════╣")

        # Binary representation
        lines.append(f"║  Binary: {self.binary_str} (line 1→6)".ljust(73) + "║")
        if self.is_symmetric:
            lines.append(f"║  [SYMMETRIC: zonggua = self]".ljust(73) + "║")
        if self.is_doubled:
            lines.append(f"║  [DOUBLED: jiaogua = self]".ljust(73) + "║")

        lines.append("╠════════════════════════════════════════════════════════════════════════╣")

        # Each relationship
        for label, hexagram, chinese, is_self in [
            ("CUOGUA (錯卦) Complement", self.cuogua, "錯", False),
            ("ZONGGUA (綜卦) Overturn", self.zonggua, "綜", self.is_symmetric),
            ("JIAOGUA (交卦) Exchange", self.jiaogua, "交", self.is_doubled),
            ("HUGUA (互卦) Nuclear", self.hugua, "互", False),
        ]:
            name = _HEXAGRAM_NAMES.get(hexagram.number, ("?", "?", "?"))
            suffix = " [self]" if is_self else ""
            hex_info = f"#{hexagram.number} {name[0]} {name[1]}{suffix}"
            lines.append(f"║  {label}:".ljust(35) + f"{hex_info.ljust(35)}  ║")

        lines.append("╠════════════════════════════════════════════════════════════════════════╣")

        # King Wen pair
        pair_name = _HEXAGRAM_NAMES.get(self.king_wen_pair.number, ("?", "?", "?"))
        pair_type = "cuogua" if self.is_symmetric else "zonggua"
        pair_info = f"#{self.king_wen_pair.number} {pair_name[0]} {pair_name[1]} (via {pair_type})"
        lines.append(f"║  KING WEN PAIR:".ljust(35) + f"{pair_info.ljust(35)}  ║")

        lines.append("╚════════════════════════════════════════════════════════════════════════╝")

        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def make_hexagram_by_number(number: int):
    """
    Create a Hexagram from its King Wen number.

    Useful for testing and exploration.
    """
    _ensure_imports()
    for (lower, upper), num in _HEXAGRAM_LOOKUP.items():
        if num == number:
            lines = []
            for i, bit in enumerate(lower):
                lines.append(_Line(value=7 if bit == 1 else 8, position=i + 1))
            for i, bit in enumerate(upper):
                lines.append(_Line(value=7 if bit == 1 else 8, position=i + 4))
            return _Hexagram(lines=lines, method="lookup")
    return None


def get_all_relations(number: int) -> Optional[HexagramRelations]:
    """
    Get HexagramRelations for a hexagram by King Wen number.
    """
    hexagram = make_hexagram_by_number(number)
    if hexagram:
        return HexagramRelations(primary=hexagram)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN (for testing)
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys

    # Test with a hexagram number
    test_num = int(sys.argv[1]) if len(sys.argv) > 1 else 11

    print(f"Testing relationships for Hexagram {test_num}:")
    print()

    relations = get_all_relations(test_num)
    if relations:
        print(relations.to_ascii())
    else:
        print(f"Hexagram {test_num} not found.")
