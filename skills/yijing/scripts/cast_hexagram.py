#!/usr/bin/env python3
"""
Yijing Hexagram Generator

Generates I Ching hexagrams using multiple methods:
- Yarrow stalk simulation (traditional asymmetric probabilities)
- Three-coin method (symmetric probabilities)
- Seeded generation (reproducible from question)
- Random generation (true random)

Usage:
    python cast_hexagram.py                           # Random casting
    python cast_hexagram.py "My question"             # Seeded from question
    python cast_hexagram.py --method yarrow           # Use yarrow probabilities
    python cast_hexagram.py --method coins            # Use coin probabilities
    python cast_hexagram.py --seed 12345              # Explicit seed
    python cast_hexagram.py --json                    # JSON output
"""

import argparse
import hashlib
import json
import os
import random
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any

# Session management import
try:
    from session import (
        SessionManager,
        ConsultationSession,
        ReadingRecord,
        display_session_list,
        display_session_history,
        display_pattern_analysis,
    )
    SESSION_AVAILABLE = True
except ImportError:
    SESSION_AVAILABLE = False

# Hexagram relations import
try:
    from hexagram_relations import HexagramRelations
    RELATIONS_AVAILABLE = True
except ImportError:
    RELATIONS_AVAILABLE = False

# Na Jia / Wen Wang Gua import (六爻 chart: palace, stems/branches, Six Relatives, 世應)
try:
    from na_jia import build_chart, format_chart
    NAJIA_AVAILABLE = True
except ImportError:
    NAJIA_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════════════
# ORACLE REFUSAL (IMPORTUNITY DETECTION)
# ═══════════════════════════════════════════════════════════════════════════════

# Hexagram 4 teaches: "At the first oracle I inform. Repeated asking is
# importunity. If importunate, I give no information."

HISTORY_FILE = Path.home() / ".yijing_history.json"
IMPORTUNITY_WINDOW_HOURS = 24
SIMILARITY_THRESHOLD = 0.7


def get_question_history() -> Dict[str, Any]:
    """Load question history from file."""
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            return {"questions": []}
    return {"questions": []}


def save_question_history(history: Dict[str, Any]) -> None:
    """Save question history to file."""
    try:
        HISTORY_FILE.write_text(json.dumps(history, indent=2))
    except IOError:
        pass  # Fail silently if we can't write


def normalize_question(question: str) -> str:
    """Normalize question for similarity comparison."""
    # Lowercase, remove punctuation, collapse whitespace
    q = question.lower()
    q = re.sub(r'[^\w\s]', '', q)
    q = re.sub(r'\s+', ' ', q).strip()
    return q


def calculate_similarity(q1: str, q2: str) -> float:
    """Calculate simple word overlap similarity."""
    words1 = set(normalize_question(q1).split())
    words2 = set(normalize_question(q2).split())
    if not words1 or not words2:
        return 0.0
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union if union > 0 else 0.0


def detect_importunity(question: str) -> Optional[str]:
    """
    Detect if the question is importunate (repeated, trivial, or seeking confirmation).

    Returns None if question is acceptable, or a refusal message if importunate.
    """
    if not question:
        return None  # No question, no refusal

    normalized = normalize_question(question)

    # Check for trivial questions
    trivial_patterns = [
        r'^test$', r'^asdf', r'^hello$', r'^hi$', r'^[a-z]$',
        r'^what$', r'^why$', r'^how$', r'^[?]+$'
    ]
    for pattern in trivial_patterns:
        if re.match(pattern, normalized):
            return (
                "The oracle does not speak to empty vessels.\n"
                "蒙卦 (Méng) teaches: 'The young fool seeks me.'\n"
                "Bring a genuine question, one that lives in you."
            )

    # Check for confirmation-seeking
    confirmation_patterns = [
        r'right\s*[?]?\s*$', r'correct\s*[?]?\s*$', r'yes\s*[?]?\s*$',
        r'isn\'?t\s+it\s*[?]?\s*$', r'don\'?t\s+you\s+think\s*[?]?\s*$'
    ]
    for pattern in confirmation_patterns:
        if re.search(pattern, normalized):
            return (
                "The oracle does not confirm—it opens.\n"
                "You seek agreement; the Changes offer perspective.\n"
                "Reframe: 'What should I understand about this situation?'"
            )

    # Check for repeated questions within time window
    history = get_question_history()
    current_time = time.time()
    window_seconds = IMPORTUNITY_WINDOW_HOURS * 3600

    for entry in history.get("questions", []):
        age = current_time - entry.get("timestamp", 0)
        if age < window_seconds:
            similarity = calculate_similarity(question, entry.get("question", ""))
            if similarity > SIMILARITY_THRESHOLD:
                return (
                    "The oracle has already spoken to this question.\n"
                    "蒙卦 (Méng) warns: '初筮告，再三瀆，瀆則不告。'\n"
                    "'At the first oracle I inform. Repeated asking is importunity.\n"
                    "If importunate, I give no information.'\n\n"
                    "If the answer was unclear, contemplate it longer.\n"
                    "If the answer was unwelcome, that is your teaching.\n"
                    "Return when you have a new question—not a repeated demand."
                )

    return None


def record_question(question: str) -> None:
    """Record a question in history."""
    if not question:
        return

    history = get_question_history()
    current_time = time.time()

    # Clean old entries
    window_seconds = IMPORTUNITY_WINDOW_HOURS * 3600
    history["questions"] = [
        e for e in history.get("questions", [])
        if current_time - e.get("timestamp", 0) < window_seconds
    ]

    # Add new entry
    history["questions"].append({
        "question": question,
        "normalized": normalize_question(question),
        "timestamp": current_time
    })

    save_question_history(history)

# ═══════════════════════════════════════════════════════════════════════════════
# TRIGRAM DATA
# ═══════════════════════════════════════════════════════════════════════════════

TRIGRAMS = {
    (1, 1, 1): {"name": "Qián", "chinese": "乾", "symbol": "☰", "image": "Heaven", "element": "Metal"},
    (0, 0, 0): {"name": "Kūn", "chinese": "坤", "symbol": "☷", "image": "Earth", "element": "Earth"},
    # Trigram binaries are (line1, line2, line3) = BOTTOM-to-top (line1 = bottom).
    # Zhèn ☳ = single yang at the BOTTOM = (1,0,0); Gèn ☶ = single yang at the TOP = (0,0,1).
    # Xùn ☴ = single yin at the BOTTOM = (0,1,1); Duì ☱ = single yin at the TOP = (1,1,0).
    # (Corrected 2026-06-20: these four non-palindromic trigrams were previously stored as
    #  their vertical mirrors — a top-to-bottom convention clashing with bottom-to-top extraction.)
    (1, 0, 0): {"name": "Zhèn", "chinese": "震", "symbol": "☳", "image": "Thunder", "element": "Wood"},
    (0, 1, 1): {"name": "Xùn", "chinese": "巽", "symbol": "☴", "image": "Wind", "element": "Wood"},
    (0, 1, 0): {"name": "Kǎn", "chinese": "坎", "symbol": "☵", "image": "Water", "element": "Water"},
    (1, 0, 1): {"name": "Lí", "chinese": "離", "symbol": "☲", "image": "Fire", "element": "Fire"},
    (0, 0, 1): {"name": "Gèn", "chinese": "艮", "symbol": "☶", "image": "Mountain", "element": "Earth"},
    (1, 1, 0): {"name": "Duì", "chinese": "兌", "symbol": "☱", "image": "Lake", "element": "Metal"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# HEXAGRAM DATA (King Wen sequence)
# ═══════════════════════════════════════════════════════════════════════════════

# Lookup: (lower_trigram, upper_trigram) -> hexagram number
# Trigrams as (line1, line2, line3) where 1=yang, 0=yin
HEXAGRAM_LOOKUP = {
    ((1, 1, 1), (1, 1, 1)): 1,  # Qián
    ((0, 0, 0), (0, 0, 0)): 2,  # Kūn
    ((1, 0, 0), (0, 1, 0)): 3,  # Zhūn
    ((0, 1, 0), (0, 0, 1)): 4,  # Méng
    ((1, 1, 1), (0, 1, 0)): 5,  # Xū
    ((0, 1, 0), (1, 1, 1)): 6,  # Sòng
    ((0, 1, 0), (0, 0, 0)): 7,  # Shī
    ((0, 0, 0), (0, 1, 0)): 8,  # Bǐ
    ((1, 1, 1), (0, 1, 1)): 9,  # Xiǎo Xù
    ((1, 1, 0), (1, 1, 1)): 10,  # Lǚ
    ((1, 1, 1), (0, 0, 0)): 11,  # Tài
    ((0, 0, 0), (1, 1, 1)): 12,  # Pǐ
    ((1, 0, 1), (1, 1, 1)): 13,  # Tóng Rén
    ((1, 1, 1), (1, 0, 1)): 14,  # Dà Yǒu
    ((0, 0, 1), (0, 0, 0)): 15,  # Qiān
    ((0, 0, 0), (1, 0, 0)): 16,  # Yù
    ((1, 0, 0), (1, 1, 0)): 17,  # Suí
    ((0, 1, 1), (0, 0, 1)): 18,  # Gǔ
    ((1, 1, 0), (0, 0, 0)): 19,  # Lín
    ((0, 0, 0), (0, 1, 1)): 20,  # Guān
    ((1, 0, 0), (1, 0, 1)): 21,  # Shì Kè
    ((1, 0, 1), (0, 0, 1)): 22,  # Bì
    ((0, 0, 0), (0, 0, 1)): 23,  # Bō
    ((1, 0, 0), (0, 0, 0)): 24,  # Fù
    ((1, 0, 0), (1, 1, 1)): 25,  # Wú Wàng
    ((1, 1, 1), (0, 0, 1)): 26,  # Dà Xù
    ((1, 0, 0), (0, 0, 1)): 27,  # Yí
    ((0, 1, 1), (1, 1, 0)): 28,  # Dà Guò
    ((0, 1, 0), (0, 1, 0)): 29,  # Kǎn
    ((1, 0, 1), (1, 0, 1)): 30,  # Lí
    ((0, 0, 1), (1, 1, 0)): 31,  # Xián
    ((0, 1, 1), (1, 0, 0)): 32,  # Héng
    ((0, 0, 1), (1, 1, 1)): 33,  # Dùn
    ((1, 1, 1), (1, 0, 0)): 34,  # Dà Zhuàng
    ((0, 0, 0), (1, 0, 1)): 35,  # Jìn
    ((1, 0, 1), (0, 0, 0)): 36,  # Míng Yí
    ((1, 0, 1), (0, 1, 1)): 37,  # Jiā Rén
    ((1, 1, 0), (1, 0, 1)): 38,  # Kuí
    ((0, 0, 1), (0, 1, 0)): 39,  # Jiǎn
    ((0, 1, 0), (1, 0, 0)): 40,  # Xiè
    ((1, 1, 0), (0, 0, 1)): 41,  # Sǔn
    ((1, 0, 0), (0, 1, 1)): 42,  # Yì
    ((1, 1, 1), (1, 1, 0)): 43,  # Guài
    ((0, 1, 1), (1, 1, 1)): 44,  # Gòu
    ((0, 0, 0), (1, 1, 0)): 45,  # Cuì
    ((0, 1, 1), (0, 0, 0)): 46,  # Shēng
    ((0, 1, 0), (1, 1, 0)): 47,  # Kùn
    ((0, 1, 1), (0, 1, 0)): 48,  # Jǐng
    ((1, 0, 1), (1, 1, 0)): 49,  # Gé
    ((0, 1, 1), (1, 0, 1)): 50,  # Dǐng
    ((1, 0, 0), (1, 0, 0)): 51,  # Zhèn
    ((0, 0, 1), (0, 0, 1)): 52,  # Gèn
    ((0, 0, 1), (0, 1, 1)): 53,  # Jiàn
    ((1, 1, 0), (1, 0, 0)): 54,  # Guī Mèi
    ((1, 0, 1), (1, 0, 0)): 55,  # Fēng
    ((0, 0, 1), (1, 0, 1)): 56,  # Lǚ
    ((0, 1, 1), (0, 1, 1)): 57,  # Xùn
    ((1, 1, 0), (1, 1, 0)): 58,  # Duì
    ((0, 1, 0), (0, 1, 1)): 59,  # Huàn
    ((1, 1, 0), (0, 1, 0)): 60,  # Jié
    ((1, 1, 0), (0, 1, 1)): 61,  # Zhōng Fú
    ((0, 0, 1), (1, 0, 0)): 62,  # Xiǎo Guò (Thunder over Mountain)
    ((1, 0, 1), (0, 1, 0)): 63,  # Jì Jì
    ((0, 1, 0), (1, 0, 1)): 64,  # Wèi Jì
}

HEXAGRAM_NAMES = {
    1: ("乾", "Qián", "The Creative"),
    2: ("坤", "Kūn", "The Receptive"),
    3: ("屯", "Zhūn", "Difficulty at the Beginning"),
    4: ("蒙", "Méng", "Youthful Folly"),
    5: ("需", "Xū", "Waiting"),
    6: ("訟", "Sòng", "Conflict"),
    7: ("師", "Shī", "The Army"),
    8: ("比", "Bǐ", "Holding Together"),
    9: ("小畜", "Xiǎo Xù", "The Taming Power of the Small"),
    10: ("履", "Lǚ", "Treading"),
    11: ("泰", "Tài", "Peace"),
    12: ("否", "Pǐ", "Standstill"),
    13: ("同人", "Tóng Rén", "Fellowship"),
    14: ("大有", "Dà Yǒu", "Possession in Great Measure"),
    15: ("謙", "Qiān", "Modesty"),
    16: ("豫", "Yù", "Enthusiasm"),
    17: ("隨", "Suí", "Following"),
    18: ("蠱", "Gǔ", "Work on What Has Been Spoiled"),
    19: ("臨", "Lín", "Approach"),
    20: ("觀", "Guān", "Contemplation"),
    21: ("噬嗑", "Shì Kè", "Biting Through"),
    22: ("賁", "Bì", "Grace"),
    23: ("剝", "Bō", "Splitting Apart"),
    24: ("復", "Fù", "Return"),
    25: ("無妄", "Wú Wàng", "Innocence"),
    26: ("大畜", "Dà Xù", "The Taming Power of the Great"),
    27: ("頤", "Yí", "Nourishment"),
    28: ("大過", "Dà Guò", "Preponderance of the Great"),
    29: ("坎", "Kǎn", "The Abysmal"),
    30: ("離", "Lí", "The Clinging"),
    31: ("咸", "Xián", "Influence"),
    32: ("恆", "Héng", "Duration"),
    33: ("遯", "Dùn", "Retreat"),
    34: ("大壯", "Dà Zhuàng", "The Power of the Great"),
    35: ("晉", "Jìn", "Progress"),
    36: ("明夷", "Míng Yí", "Darkening of the Light"),
    37: ("家人", "Jiā Rén", "The Family"),
    38: ("睽", "Kuí", "Opposition"),
    39: ("蹇", "Jiǎn", "Obstruction"),
    40: ("解", "Xiè", "Deliverance"),
    41: ("損", "Sǔn", "Decrease"),
    42: ("益", "Yì", "Increase"),
    43: ("夬", "Guài", "Breakthrough"),
    44: ("姤", "Gòu", "Coming to Meet"),
    45: ("萃", "Cuì", "Gathering Together"),
    46: ("升", "Shēng", "Pushing Upward"),
    47: ("困", "Kùn", "Oppression"),
    48: ("井", "Jǐng", "The Well"),
    49: ("革", "Gé", "Revolution"),
    50: ("鼎", "Dǐng", "The Caldron"),
    51: ("震", "Zhèn", "The Arousing"),
    52: ("艮", "Gèn", "Keeping Still"),
    53: ("漸", "Jiàn", "Development"),
    54: ("歸妹", "Guī Mèi", "The Marrying Maiden"),
    55: ("豐", "Fēng", "Abundance"),
    56: ("旅", "Lǚ", "The Wanderer"),
    57: ("巽", "Xùn", "The Gentle"),
    58: ("兌", "Duì", "The Joyous"),
    59: ("渙", "Huàn", "Dispersion"),
    60: ("節", "Jié", "Limitation"),
    61: ("中孚", "Zhōng Fú", "Inner Truth"),
    62: ("小過", "Xiǎo Guò", "Preponderance of the Small"),
    63: ("既濟", "Jì Jì", "After Completion"),
    64: ("未濟", "Wèi Jì", "Before Completion"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Line:
    """A single line of a hexagram."""
    value: int  # 6, 7, 8, or 9
    position: int  # 1-6 from bottom

    @property
    def is_yang(self) -> bool:
        """Is this line yang (solid)?"""
        return self.value in (7, 9)

    @property
    def is_yin(self) -> bool:
        """Is this line yin (broken)?"""
        return self.value in (6, 8)

    @property
    def is_moving(self) -> bool:
        """Is this a moving/changing line?"""
        return self.value in (6, 9)

    @property
    def binary(self) -> int:
        """Return 1 for yang, 0 for yin."""
        return 1 if self.is_yang else 0

    @property
    def transformed_binary(self) -> int:
        """Return binary after transformation (if moving)."""
        if self.value == 6:  # Old yin -> yang
            return 1
        elif self.value == 9:  # Old yang -> yin
            return 0
        else:
            return self.binary

    def to_ascii(self) -> str:
        """Return ASCII representation."""
        if self.is_moving:
            if self.value == 9:
                return "▬▬●▬▬"  # Old yang
            else:  # value == 6
                return "▬▬✕▬▬"  # Old yin
        else:
            if self.is_yang:
                return "▬▬▬▬▬"  # Young yang
            else:
                return "▬▬ ▬▬"  # Young yin

    def to_dict(self) -> dict:
        return {
            "position": self.position,
            "value": self.value,
            "is_yang": self.is_yang,
            "is_moving": self.is_moving,
        }


@dataclass
class Hexagram:
    """A complete hexagram with six lines."""
    lines: List[Line]
    question: str = ""
    seed: Optional[int] = None
    method: str = "random"

    def __post_init__(self):
        if len(self.lines) != 6:
            raise ValueError("Hexagram must have exactly 6 lines")

    @property
    def lower_trigram(self) -> Tuple[int, int, int]:
        """Lower trigram as (line1, line2, line3) binary."""
        return (self.lines[0].binary, self.lines[1].binary, self.lines[2].binary)

    @property
    def upper_trigram(self) -> Tuple[int, int, int]:
        """Upper trigram as (line4, line5, line6) binary."""
        return (self.lines[3].binary, self.lines[4].binary, self.lines[5].binary)

    @property
    def number(self) -> int:
        """King Wen sequence number."""
        key = (self.lower_trigram, self.upper_trigram)
        return HEXAGRAM_LOOKUP.get(key, 0)

    @property
    def name(self) -> Tuple[str, str, str]:
        """(Chinese, Pinyin, English) name tuple."""
        return HEXAGRAM_NAMES.get(self.number, ("?", "?", "Unknown"))

    @property
    def moving_lines(self) -> List[int]:
        """Positions of moving lines (1-6)."""
        return [line.position for line in self.lines if line.is_moving]

    @property
    def has_moving_lines(self) -> bool:
        return len(self.moving_lines) > 0

    @property
    def nuclear_hexagram_lines(self) -> List[int]:
        """Extract nuclear hexagram line values (2-3-4 for lower, 3-4-5 for upper)."""
        # Nuclear lower: lines 2, 3, 4
        # Nuclear upper: lines 3, 4, 5
        nuclear = []
        for i in [1, 2, 3]:  # Lines 2, 3, 4 (0-indexed: 1, 2, 3)
            nuclear.append(7 if self.lines[i].is_yang else 8)
        for i in [2, 3, 4]:  # Lines 3, 4, 5 (0-indexed: 2, 3, 4)
            nuclear.append(7 if self.lines[i].is_yang else 8)
        return nuclear

    def get_relating_hexagram(self) -> Optional['Hexagram']:
        """Get the relating hexagram (after moving lines transform)."""
        if not self.has_moving_lines:
            return None

        new_lines = []
        for line in self.lines:
            if line.is_moving:
                # Transform: 6 -> 7 (yin to yang), 9 -> 8 (yang to yin)
                new_value = 7 if line.value == 6 else 8
            else:
                new_value = line.value
            new_lines.append(Line(value=new_value, position=line.position))

        return Hexagram(
            lines=new_lines,
            question=self.question,
            seed=self.seed,
            method=self.method
        )

    def get_nuclear_hexagram(self) -> 'Hexagram':
        """Extract the nuclear hexagram (lines 2-3-4 and 3-4-5)."""
        nuclear_lines = []
        # Lower nuclear: lines 2, 3, 4 become lines 1, 2, 3
        for i, pos in enumerate([1, 2, 3], start=1):  # 0-indexed
            val = 7 if self.lines[pos].is_yang else 8
            nuclear_lines.append(Line(value=val, position=i))
        # Upper nuclear: lines 3, 4, 5 become lines 4, 5, 6
        for i, pos in enumerate([2, 3, 4], start=4):
            val = 7 if self.lines[pos].is_yang else 8
            nuclear_lines.append(Line(value=val, position=i))

        return Hexagram(lines=nuclear_lines, question=self.question, method="nuclear")

    def to_ascii(self) -> str:
        """Generate ASCII art representation."""
        lines = []
        lines.append("╔════════════════════════════════════════════════════════════╗")

        # Header
        chinese, pinyin, english = self.name
        header = f"Hexagram {self.number}: {chinese} {pinyin} — {english}"
        lines.append(f"║{header.center(60)}║")

        if self.question:
            q = self.question[:56]
            lines.append(f"║  Question: {q.ljust(47)}║")

        lines.append("╠════════════════════════════════════════════════════════════╣")

        # Trigram info
        upper_info = TRIGRAMS.get(self.upper_trigram, {})
        lower_info = TRIGRAMS.get(self.lower_trigram, {})
        upper_name = f"{upper_info.get('symbol', '?')} {upper_info.get('name', '?')} ({upper_info.get('image', '?')})"
        lower_name = f"{lower_info.get('symbol', '?')} {lower_info.get('name', '?')} ({lower_info.get('image', '?')})"

        lines.append(f"║  Upper: {upper_name.ljust(50)}║")
        lines.append(f"║  Lower: {lower_name.ljust(50)}║")
        lines.append("╠════════════════════════════════════════════════════════════╣")

        # Lines (from top to bottom, so reverse order)
        for line in reversed(self.lines):
            marker = " *" if line.is_moving else "  "
            pos_label = f"Line {line.position}:"
            value_label = f"({line.value})"
            line_str = f"║  {pos_label:8} {line.to_ascii():^12} {value_label:5}{marker}           ║"
            lines.append(line_str)

        lines.append("╠════════════════════════════════════════════════════════════╣")

        # Moving lines summary
        if self.has_moving_lines:
            moving_str = ", ".join(str(p) for p in self.moving_lines)
            lines.append(f"║  Moving lines: {moving_str.ljust(43)}║")

            relating = self.get_relating_hexagram()
            if relating:
                r_chinese, r_pinyin, r_english = relating.name
                rel_str = f"→ Hexagram {relating.number}: {r_chinese} {r_pinyin}"
                lines.append(f"║  Relating hexagram: {rel_str.ljust(38)}║")
        else:
            lines.append(f"║  No moving lines — situation is stable              ║")

        # Nuclear hexagram
        nuclear = self.get_nuclear_hexagram()
        n_chinese, n_pinyin, n_english = nuclear.name
        nuc_str = f"Hexagram {nuclear.number}: {n_chinese} {n_pinyin}"
        lines.append(f"║  Nuclear hexagram: {nuc_str.ljust(39)}║")

        lines.append("╠════════════════════════════════════════════════════════════╣")

        # Method and seed
        lines.append(f"║  Method: {self.method.ljust(49)}║")
        if self.seed:
            lines.append(f"║  Seed: {str(self.seed)[:50].ljust(51)}║")

        # Probability histogram (cosmology visualization)
        lines.append("╠════════════════════════════════════════════════════════════╣")
        lines.append("║  COSMOLOGY INVOKED:                                        ║")
        if self.method in ("yarrow", "random"):
            lines.append("║  ┌──────────────────────────────────────────────────────┐   ║")
            lines.append("║  │ 6 █░░░░░░░  7 █████░░░  8 ███████░  9 ███░░░░░       │   ║")
            lines.append("║  │   6.25%      31.25%      43.75%      18.75%          │   ║")
            lines.append("║  └──────────────────────────────────────────────────────┘   ║")
            lines.append("║  Yarrow: Yang changes 3× more readily than yin              ║")
        else:  # coins
            lines.append("║  ┌──────────────────────────────────────────────────────┐   ║")
            lines.append("║  │ 6 ██░░░░░░  7 ██████░░  8 ██████░░  9 ██░░░░░░       │   ║")
            lines.append("║  │   12.5%       37.5%       37.5%       12.5%          │   ║")
            lines.append("║  └──────────────────────────────────────────────────────┘   ║")
            lines.append("║  Coins: Symmetric — all change equally probable             ║")

        lines.append("╚════════════════════════════════════════════════════════════╝")

        return "\n".join(lines)

    def to_dict(self) -> dict:
        chinese, pinyin, english = self.name
        result = {
            "number": self.number,
            "name": {"chinese": chinese, "pinyin": pinyin, "english": english},
            "lines": [line.to_dict() for line in self.lines],
            "lower_trigram": TRIGRAMS.get(self.lower_trigram, {}),
            "upper_trigram": TRIGRAMS.get(self.upper_trigram, {}),
            "moving_lines": self.moving_lines,
            "question": self.question,
            "seed": self.seed,
            "method": self.method,
        }

        if self.has_moving_lines:
            relating = self.get_relating_hexagram()
            if relating:
                r_chinese, r_pinyin, r_english = relating.name
                result["relating_hexagram"] = {
                    "number": relating.number,
                    "name": {"chinese": r_chinese, "pinyin": r_pinyin, "english": r_english}
                }

        nuclear = self.get_nuclear_hexagram()
        n_chinese, n_pinyin, n_english = nuclear.name
        result["nuclear_hexagram"] = {
            "number": nuclear.number,
            "name": {"chinese": n_chinese, "pinyin": n_pinyin, "english": n_english}
        }

        return result


# ═══════════════════════════════════════════════════════════════════════════════
# CASTING METHODS
# ═══════════════════════════════════════════════════════════════════════════════

def cast_line_yarrow(rng: random.Random) -> int:
    """
    Cast a single line using yarrow stalk probabilities.

    Probability distribution:
    - 6 (Old Yin):    1/16 = 6.25%
    - 7 (Young Yang): 5/16 = 31.25%
    - 8 (Young Yin):  7/16 = 43.75%
    - 9 (Old Yang):   3/16 = 18.75%
    """
    value = rng.random()

    if value < 1/16:        # 0.0625
        return 6
    elif value < 6/16:      # 0.375
        return 7
    elif value < 13/16:     # 0.8125
        return 8
    else:                   # remaining 3/16
        return 9


def cast_line_coins(rng: random.Random) -> int:
    """
    Cast a single line using three-coin probabilities.

    Probability distribution:
    - 6 (Old Yin):    1/8 = 12.5%
    - 7 (Young Yang): 3/8 = 37.5%
    - 8 (Young Yin):  3/8 = 37.5%
    - 9 (Old Yang):   1/8 = 12.5%
    """
    value = rng.random()

    if value < 1/8:         # Old Yin
        return 6
    elif value < 4/8:       # Young Yang
        return 7
    elif value < 7/8:       # Young Yin
        return 8
    else:                   # Old Yang
        return 9


def cast_hexagram(
    question: Optional[str] = None,
    method: str = "yarrow",
    seed: Optional[int] = None
) -> Hexagram:
    """
    Cast a complete hexagram.

    Args:
        question: Optional question to seed the casting
        method: "yarrow" (traditional), "coins" (three-coin), or "random"
        seed: Optional explicit seed for reproducibility

    Returns:
        A complete Hexagram object
    """
    # Determine seed
    if seed is None:
        if question:
            # Seed from the question ALONE so a given question yields a stable cast
            # (the documented contract; also the premise of the importunity guard).
            # Corrected 2026-06-20: mixing time.time() in made every call non-reproducible.
            hash_bytes = hashlib.sha256(question.encode()).digest()
            seed = int.from_bytes(hash_bytes[:8], 'big')
        else:
            seed = int(time.time() * 1000000)

    rng = random.Random(seed)

    # Select casting function
    if method == "coins":
        cast_fn = cast_line_coins
    else:  # yarrow or random (default to yarrow probabilities)
        cast_fn = cast_line_yarrow

    # Cast six lines
    lines = []
    for position in range(1, 7):
        value = cast_fn(rng)
        lines.append(Line(value=value, position=position))

    return Hexagram(
        lines=lines,
        question=question or "",
        seed=seed,
        method=method
    )


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Cast an I Ching hexagram",
        epilog="易，窮則變，變則通，通則久。"
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="Question to seed the casting (optional)"
    )
    parser.add_argument(
        "--method", "-m",
        choices=["yarrow", "coins", "random"],
        default="yarrow",
        help="Casting method (default: yarrow)"
    )
    parser.add_argument(
        "--seed", "-s",
        type=int,
        help="Explicit random seed for reproducibility"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output as JSON"
    )
    parser.add_argument(
        "--relations", "-r",
        action="store_true",
        help="Show hexagram relationships (cuogua, zonggua, jiaogua, hugua)"
    )
    parser.add_argument(
        "--najia", "-n",
        action="store_true",
        help="Show the Wen Wang Gua / 六爻 chart (palace, 納甲 stems/branches, Six Relatives, 世應)"
    )
    parser.add_argument(
        "--no-refusal",
        action="store_true",
        help="Bypass importunity detection (override Méng's teaching)"
    )
    parser.add_argument(
        "--clear-history",
        action="store_true",
        help="Clear question history and exit"
    )

    # Session management arguments
    session_group = parser.add_argument_group("session management")
    session_group.add_argument(
        "--new-session",
        metavar="NAME",
        help="Start a new consultation session with given name"
    )
    session_group.add_argument(
        "--session",
        metavar="ID",
        help="Use a specific session by ID"
    )
    session_group.add_argument(
        "--resume",
        action="store_true",
        help="Resume the active session (if any)"
    )
    session_group.add_argument(
        "--list-sessions",
        action="store_true",
        help="List all consultation sessions"
    )
    session_group.add_argument(
        "--history",
        nargs="?",
        const="active",
        metavar="ID",
        help="Show reading history for session (default: active session)"
    )
    session_group.add_argument(
        "--patterns",
        nargs="?",
        const="active",
        metavar="ID",
        help="Analyze patterns in session readings (default: active session)"
    )
    session_group.add_argument(
        "--archive-session",
        metavar="ID",
        help="Archive a session"
    )

    args = parser.parse_args()

    # Handle history clearing
    if args.clear_history:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
            print("Question history cleared.")
        else:
            print("No question history to clear.")
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # SESSION MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════════════

    session_manager = None
    active_session = None

    if SESSION_AVAILABLE:
        session_manager = SessionManager()

        # Handle --list-sessions
        if args.list_sessions:
            sessions = session_manager.list_sessions(include_archived=True)
            print(display_session_list(sessions, session_manager.active_session_id))
            return

        # Handle --history
        if args.history:
            session_id = args.history if args.history != "active" else session_manager.active_session_id
            if not session_id:
                print("No active session. Use --session ID or --new-session NAME.")
                return
            session = session_manager.get_session(session_id)
            if not session:
                print(f"Session not found: {session_id}")
                return
            print(display_session_history(session))
            return

        # Handle --patterns
        if args.patterns:
            session_id = args.patterns if args.patterns != "active" else session_manager.active_session_id
            if not session_id:
                print("No active session. Use --session ID or --new-session NAME.")
                return
            session = session_manager.get_session(session_id)
            if not session:
                print(f"Session not found: {session_id}")
                return
            patterns = session.get_patterns()
            print(display_pattern_analysis(patterns, session.name))
            return

        # Handle --archive-session
        if args.archive_session:
            if session_manager.archive_session(args.archive_session):
                print(f"Session archived: {args.archive_session}")
            else:
                print(f"Session not found: {args.archive_session}")
            return

        # Handle --new-session
        if args.new_session:
            active_session = session_manager.create_session(name=args.new_session)
            print(f"Created session: {active_session.id} ({active_session.name})")

        # Handle --session (use specific session)
        elif args.session:
            active_session = session_manager.get_session(args.session)
            if not active_session:
                print(f"Session not found: {args.session}")
                return
            session_manager.set_active_session(args.session)

        # Handle --resume (resume active session)
        elif args.resume:
            active_session = session_manager.get_active_session()
            if not active_session:
                print("No active session to resume. Use --new-session NAME to create one.")
                return
            print(f"Resuming session: {active_session.id} ({active_session.name})")

    elif any([args.new_session, args.session, args.resume, args.list_sessions,
              args.history, args.patterns, args.archive_session]):
        print("Session management not available (session.py not found).")
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # CASTING
    # ═══════════════════════════════════════════════════════════════════════════

    # Check for importunity (unless bypassed)
    if args.question and not args.no_refusal:
        refusal = detect_importunity(args.question)
        if refusal:
            print("╔════════════════════════════════════════════════════════════╗")
            print("║                  THE ORACLE DECLINES                       ║")
            print("╠════════════════════════════════════════════════════════════╣")
            for line in refusal.split('\n'):
                print(f"║  {line.ljust(56)}║")
            print("╠════════════════════════════════════════════════════════════╣")
            print("║  (Use --no-refusal to override, but consider: why?)        ║")
            print("╚════════════════════════════════════════════════════════════╝")
            sys.exit(1)

    # Cast the hexagram
    hexagram = cast_hexagram(
        question=args.question,
        method=args.method,
        seed=args.seed
    )

    # Record the question for future importunity detection
    if args.question and not args.no_refusal:
        record_question(args.question)

    # Record reading in session (if session active)
    if active_session and session_manager:
        reading = ReadingRecord.from_hexagram(hexagram, args.question or "")
        active_session.add_reading(reading)
        session_manager.save_session(active_session)

    # Output
    if args.json:
        output = hexagram.to_dict()
        if active_session:
            output["session"] = {
                "id": active_session.id,
                "name": active_session.name,
                "reading_count": len(active_session.readings)
            }
        if args.relations and RELATIONS_AVAILABLE:
            relations = HexagramRelations(primary=hexagram)
            output["relationships"] = relations.to_dict()["relationships"]
        if args.najia and NAJIA_AVAILABLE:
            output["najia"] = build_chart(hexagram, topic=args.question or None).to_dict()
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(hexagram.to_ascii())
        print()

        # Show relations if requested
        if args.relations:
            if RELATIONS_AVAILABLE:
                relations = HexagramRelations(primary=hexagram)
                print(relations.to_ascii())
                print()
            else:
                print("  (Relationships not available - hexagram_relations.py not found)")
                print()

        # Show the Wen Wang Gua / 六爻 chart if requested
        if args.najia:
            if NAJIA_AVAILABLE:
                print(format_chart(build_chart(hexagram, topic=args.question or None)))
                print()
            else:
                print("  (Na Jia chart not available - na_jia.py not found)")
                print()

        if active_session:
            print(f"  Session: {active_session.name} ({active_session.id})")
            print(f"  Reading #{len(active_session.readings)} in this session")
            print()
        print("To interpret this hexagram, consult the references in:")
        print("  .claude/skills/yijing/references/HEXAGRAMS.md")
        if hexagram.has_moving_lines:
            print("  .claude/skills/yijing/references/MOVING_LINES.md")
        print()


if __name__ == "__main__":
    main()
