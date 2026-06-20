#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
na_jia.py — 納甲筮法 / 文王卦 / 六爻 engine.

Enacts the Wen Wang Gua (King Wen) divination apparatus that
``references/NA_JIA.md`` documents: the four steps of 裝卦 (sì bù zhuāng guà).

    1. 裝宮 / 定宮   find the palace + palace-position; palace element = head-trigram element
    2. 納甲          assign Heavenly Stem + Earthly Branch to each of the six lines
    3. 定五行        read each line's Five-Element value off its branch
    4. 定六親、安世應  assign the Six Relatives against the PALACE element; place 世/應

Design note — *second genesis, not transcription*.
NA_JIA.md is honest that its tables are "secondary-triangulated, not a direct read
of the 京氏易傳 primary text." Re-typing those tables here would only copy the doc's
uncertainty (and any error) one level down. So this module instead *derives* every
table from a minimal set of sourced primitives:

    - the eight palace-head trigrams + the generating (flip) rule        -> the 8×8 palace grid
    - per-trigram branch-START + the 陽順陰逆 (+2 / −2) rule              -> all branch tables
    - the 生 (generating) and 克 (controlling) element cycles            -> the Six Relatives
    - the World-line walk 6→1→2→3→4→5→4→3, Response = World+3 (mod 6)    -> 世/應

The derivations are then cross-checked, in tests, against (a) NA_JIA.md's own worked
examples (乾, 坤, 屯), (b) the requirement that the generated palace grid partitions all
64 King-Wen hexagrams exactly once, and (c) canonical external Liu Yao charts. When an
independent derivation agrees with the transcribed table AND with an outside source,
that convergence-across-ancestry is the evidence the result is not a self-consistent
mirror. (One doc error was caught this way — see CAVEAT on 归魂 in ``palace_member_lines``.)

Importable (``from na_jia import build_chart``) and runnable
(``python3 na_jia.py 3`` casts the Wen Wang Gua chart for King-Wen hexagram #3).
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

# ── sibling module (cast_hexagram.py) ───────────────────────────────────────────
try:
    from cast_hexagram import (
        TRIGRAMS,
        HEXAGRAM_LOOKUP,
        HEXAGRAM_NAMES,
        Hexagram,
        Line,
    )
except ImportError:  # pragma: no cover — allow standalone import from any cwd
    import os

    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from cast_hexagram import (  # noqa: E402
        TRIGRAMS,
        HEXAGRAM_LOOKUP,
        HEXAGRAM_NAMES,
        Hexagram,
        Line,
    )

# ════════════════════════════════════════════════════════════════════════════════
# SOURCED PRIMITIVES  (everything else is derived from these)
# ════════════════════════════════════════════════════════════════════════════════

# The twelve Earthly Branches (地支), in cycle order. Index 0 = 子.
EARTHLY_BRANCHES: List[str] = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_PINYIN: Dict[str, str] = {
    "子": "zǐ", "丑": "chǒu", "寅": "yín", "卯": "mǎo", "辰": "chén", "巳": "sì",
    "午": "wǔ", "未": "wèi", "申": "shēn", "酉": "yǒu", "戌": "xū", "亥": "hài",
}

# Branch -> Five-Element (NA_JIA.md §3; standard 子平/六爻 correspondence).
# 寅卯木 · 巳午火 · 申酉金 · 亥子水 · 辰戌丑未土
BRANCH_ELEMENT: Dict[str, str] = {
    "子": "Water", "丑": "Earth", "寅": "Wood", "卯": "Wood", "辰": "Earth", "巳": "Fire",
    "午": "Fire", "未": "Earth", "申": "Metal", "酉": "Metal", "戌": "Earth", "亥": "Water",
}

# 六冲 (liù chōng, "six clashes") and 六合 (liù hé, "six harmonies") — the branch pairs.
# Each is an unordered pair of branches; used for 六冲卦/六合卦 detection (§5.5) and 回頭沖.
SIX_CLASH_PAIRS = frozenset(frozenset(p) for p in
    [("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")])
SIX_HARMONY_PAIRS = frozenset(frozenset(p) for p in
    [("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")])

# Per-trigram Na Jia primitives (NA_JIA.md §2). Keyed by trigram binary
# (line1, line2, line3) bottom-to-top — the SAME convention as cast_hexagram.TRIGRAMS.
#   start  : index in EARTHLY_BRANCHES of the branch on the trigram's INNER line 1
#            (the OUTER line-4 start is always start+6, mod 12 — verified for all 8)
#   stems  : (inner_stem, outer_stem); the six children repeat one stem, Qián/Kūn take two
#   yang   : True -> branches run forward (順, +2/line); False -> backward (逆, −2/line)
# Sourced from the classical 納甲 mnemonic
#   「乾金甲子外壬午，坎水戊寅外戊申，艮土丙辰外丙戌，震木庚子外庚午，
#     巽木辛丑外辛未，離火己卯外己酉，坤土乙未外癸丑，兌金丁巳外丁亥」
TRIGRAM_NAJIA: Dict[Tuple[int, int, int], Dict] = {
    (1, 1, 1): {"start": 0,  "stems": ("甲", "壬"), "yang": True},   # 乾 Qián  子 / 午
    (0, 1, 0): {"start": 2,  "stems": ("戊", "戊"), "yang": True},   # 坎 Kǎn   寅 / 申
    (0, 0, 1): {"start": 4,  "stems": ("丙", "丙"), "yang": True},   # 艮 Gèn   辰 / 戌
    (1, 0, 0): {"start": 0,  "stems": ("庚", "庚"), "yang": True},   # 震 Zhèn  子 / 午
    (0, 1, 1): {"start": 1,  "stems": ("辛", "辛"), "yang": False},  # 巽 Xùn   丑 / 未
    (1, 0, 1): {"start": 3,  "stems": ("己", "己"), "yang": False},  # 離 Lí    卯 / 酉
    (0, 0, 0): {"start": 7,  "stems": ("乙", "癸"), "yang": False},  # 坤 Kūn   未 / 丑
    (1, 1, 0): {"start": 5,  "stems": ("丁", "丁"), "yang": False},  # 兌 Duì   巳 / 亥
}

# The eight palace heads (NA_JIA.md §1.1), in divinatory order:
# four yang houses (father→sons) then four yin houses (mother→daughters).
# Palace element = element of the palace-head trigram (the Six Relatives' fulcrum).
PALACE_HEADS: List[Tuple[int, int, int]] = [
    (1, 1, 1),  # 1 乾 Qián  — Metal
    (0, 1, 0),  # 2 坎 Kǎn   — Water
    (0, 0, 1),  # 3 艮 Gèn   — Earth
    (1, 0, 0),  # 4 震 Zhèn  — Wood
    (0, 1, 1),  # 5 巽 Xùn   — Wood
    (1, 0, 1),  # 6 離 Lí    — Fire
    (0, 0, 0),  # 7 坤 Kūn   — Earth
    (1, 1, 0),  # 8 兌 Duì   — Metal
]

# The two element cycles (NA_JIA.md §4). Each list: every element generates / controls
# the NEXT one in the list (wrapping). Elements use cast_hexagram's English names.
GENERATING_CYCLE: List[str] = ["Metal", "Water", "Wood", "Fire", "Earth"]  # 金生水生木生火生土生金
CONTROLLING_CYCLE: List[str] = ["Metal", "Wood", "Earth", "Water", "Fire"]  # 金克木克土克水克火克金

# The Six Relatives (六親), named relative to the palace element ("me", 我).
SIX_RELATIVES = {
    "父母": {"pinyin": "fù mǔ", "en": "Parents", "rule": "生我 (generates me)"},
    "兄弟": {"pinyin": "xiōng dì", "en": "Siblings", "rule": "同我 (same as me)"},
    "子孫": {"pinyin": "zǐ sūn", "en": "Offspring", "rule": "我生 (I generate)"},
    "妻財": {"pinyin": "qī cái", "en": "Wealth/Wife", "rule": "我克 (I control)"},
    "官鬼": {"pinyin": "guān guǐ", "en": "Officials/Ghosts", "rule": "克我 (controls me)"},
}

# 用神 (yòng shén) — which relative represents the matter asked (NA_JIA.md §5.2).
YONG_SHEN_BY_TOPIC: Dict[str, str] = {
    "wealth": "妻財", "money": "妻財", "wife": "妻財", "business": "妻財", "property": "妻財",
    "career": "官鬼", "husband": "官鬼", "illness": "官鬼", "lawsuit": "官鬼",
    "threat": "官鬼", "ghost": "官鬼", "job": "官鬼", "sickness": "官鬼",
    "documents": "父母", "parents": "父母", "house": "父母", "study": "父母",
    "vehicle": "父母", "exam": "父母", "school": "父母",
    "children": "子孫", "child": "子孫", "blessing": "子孫", "medicine": "子孫",
    "peace": "子孫", "health": "子孫",
    "siblings": "兄弟", "peers": "兄弟", "partners": "兄弟", "competition": "兄弟",
    "friends": "兄弟", "rival": "兄弟",
}

# Palace-position names (1-based), NA_JIA.md §1.2.
POSITION_NAMES = ["本宮", "一世", "二世", "三世", "四世", "五世", "游魂", "归魂"]
POSITION_PINYIN = ["běn gōng", "yī shì", "èr shì", "sān shì", "sì shì", "wǔ shì", "yóu hún", "guī hún"]

# Which line indices (0-based, bottom→top) are flipped from the pure hexagram to reach
# each palace position (NA_JIA.md §1.2). Derived, not transcribed; see palace_member_lines.
_POSITION_FLIPS: Dict[int, frozenset] = {
    1: frozenset(),                  # 本宮  doubled trigram
    2: frozenset({0}),               # 一世  flip line 1
    3: frozenset({0, 1}),            # 二世  + line 2
    4: frozenset({0, 1, 2}),         # 三世  + line 3
    5: frozenset({0, 1, 2, 3}),      # 四世  + line 4
    6: frozenset({0, 1, 2, 3, 4}),   # 五世  + line 5
    7: frozenset({0, 1, 2, 4}),      # 游魂  from 五世, line 4 reverts
    8: frozenset({4}),               # 归魂  from 游魂, inner trigram (1,2,3) restored
}


# ════════════════════════════════════════════════════════════════════════════════
# STEP 1 — 裝宮 : palace + position  (derived 8×8 grid)
# ════════════════════════════════════════════════════════════════════════════════

def palace_member_lines(palace_trigram: Tuple[int, int, int], position: int) -> Tuple[int, ...]:
    """Six lines (bottom→top, 1=yang) of the `position`-th member of a palace.

    Built from the pure (doubled) palace trigram by flipping a cumulative set of
    lines per NA_JIA.md §1.2.  position ∈ 1..8 (本宮 … 归魂).

    CAVEAT (a doc error caught by this derivation): NA_JIA.md §1.2's prose gloss
    claims the 归魂 outer trigram "is the opposite of the palace trigram." It is
    not. For 乾宮, 归魂 = 火天大有 (☲/☰): the outer trigram is ☲ Lí, NOT ☷ Kūn
    (the opposite of ☰). The *mechanical* rule (restore the inner trigram from
    游魂) is correct and is what is implemented; the "opposite" gloss is wrong.
    The generated grid is validated to partition all 64 King-Wen hexagrams, which
    the buggy gloss would fail — so the structure, not the prose, is trusted.
    """
    if position not in _POSITION_FLIPS:
        raise ValueError(f"palace position must be 1..8, got {position}")
    p1, p2, p3 = palace_trigram
    base = [p1, p2, p3, p1, p2, p3]  # the pure hexagram (doubled trigram)
    flips = _POSITION_FLIPS[position]
    return tuple(1 - base[i] if i in flips else base[i] for i in range(6))


def _build_palace_grid() -> Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], Tuple[int, int]]:
    """Generate the full 8×8 palace grid by derivation.

    Returns a map: (lower_trigram, upper_trigram) -> (palace_index 1-8, position 1-8).
    Validated at import time to partition all 64 King-Wen hexagrams exactly once.
    """
    grid: Dict[Tuple[Tuple[int, int, int], Tuple[int, int, int]], Tuple[int, int]] = {}
    seen_kw = set()
    for pi, head in enumerate(PALACE_HEADS, start=1):
        for pos in range(1, 9):
            lines = palace_member_lines(head, pos)
            lower = lines[0:3]
            upper = lines[3:6]
            kw = HEXAGRAM_LOOKUP.get((lower, upper))
            if kw is None:  # pragma: no cover — would indicate a trigram-table mismatch
                raise RuntimeError(f"derived hexagram {lines} not in HEXAGRAM_LOOKUP")
            grid[(lower, upper)] = (pi, pos)
            seen_kw.add(kw)
    # Self-check (load-bearing): the eight palaces must partition all 64 hexagrams.
    if len(grid) != 64 or len(seen_kw) != 64:  # pragma: no cover
        raise RuntimeError(
            f"palace grid is not a clean partition: {len(grid)} cells, {len(seen_kw)} King-Wen numbers"
        )
    return grid


PALACE_GRID = _build_palace_grid()


# ════════════════════════════════════════════════════════════════════════════════
# STEP 2 — 納甲 : stems + branches on the six lines  (derived)
# ════════════════════════════════════════════════════════════════════════════════

def trigram_branches(trigram: Tuple[int, int, int], *, outer: bool) -> List[str]:
    """The three branches a trigram carries when it sits inner (lines 1-3) or
    outer (lines 4-6), bottom→top.

    Derived from the trigram's inner START branch + the 陽順陰逆 rule:
    yang trigrams run forward (+2/line), yin backward (−2/line); the outer start
    is always inner_start + 6 (mod 12), continuing the same direction.
    """
    nj = TRIGRAM_NAJIA[trigram]
    step = 2 if nj["yang"] else -2
    start = (nj["start"] + 6) % 12 if outer else nj["start"]
    return [EARTHLY_BRANCHES[(start + step * i) % 12] for i in range(3)]


def line_stems_branches(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> List[Tuple[str, str]]:
    """(stem, branch) for the six lines, bottom→top.

    Inner trigram supplies lines 1-3 (its inner column + inner stem); outer
    trigram supplies lines 4-6 (its outer column + outer stem).
    """
    inner_branches = trigram_branches(lower, outer=False)
    outer_branches = trigram_branches(upper, outer=True)
    inner_stem = TRIGRAM_NAJIA[lower]["stems"][0]
    outer_stem = TRIGRAM_NAJIA[upper]["stems"][1]
    out: List[Tuple[str, str]] = []
    for b in inner_branches:
        out.append((inner_stem, b))
    for b in outer_branches:
        out.append((outer_stem, b))
    return out


# ════════════════════════════════════════════════════════════════════════════════
# STEP 4 — 六親 : the Six Relatives  (derived from the 生/克 cycles)
# ════════════════════════════════════════════════════════════════════════════════

def _generates(a: str, b: str) -> bool:
    """Does element a generate element b? (生)"""
    i = GENERATING_CYCLE.index(a)
    return GENERATING_CYCLE[(i + 1) % 5] == b


def _controls(a: str, b: str) -> bool:
    """Does element a control element b? (克)"""
    i = CONTROLLING_CYCLE.index(a)
    return CONTROLLING_CYCLE[(i + 1) % 5] == b


def six_relative(palace_element: str, line_element: str) -> str:
    """The Six-Relative character for a line, judged against the PALACE element.

    生我者=父母 · 同我者=兄弟 · 我生者=子孫 · 我克者=妻財 · 克我者=官鬼.
    (The most common beginner error is judging against the hexagram's own lower
    trigram; it is ALWAYS the palace element. NA_JIA.md §4.)
    """
    if line_element == palace_element:
        return "兄弟"                                  # 同我
    if _generates(line_element, palace_element):
        return "父母"                                  # 生我
    if _generates(palace_element, line_element):
        return "子孫"                                  # 我生
    if _controls(palace_element, line_element):
        return "妻財"                                  # 我克
    if _controls(line_element, palace_element):
        return "官鬼"                                  # 克我
    raise RuntimeError(  # pragma: no cover — five cases are exhaustive over 5 elements
        f"no Six-Relative relation between palace {palace_element} and line {line_element}"
    )


# The 生/克 cycles expressed directly on the Six Relatives (induced by the element cycles
# when each relative is read relative to the palace). Each relative generates / controls
# the NEXT one in its list (wrapping). Derived, not transcribed; see four_spirits.
RELATIVE_SHENG: List[str] = ["父母", "兄弟", "子孫", "妻財", "官鬼"]  # 父母生兄弟生子孫生妻財生官鬼生父母
RELATIVE_KE: List[str] = ["父母", "子孫", "官鬼", "兄弟", "妻財"]      # 父母克子孫克官鬼克兄弟克妻財克父母


def four_spirits(yong_shen: str) -> Dict[str, str]:
    """The 四神 relative to a chosen 用神 (yòng shén), as Six-Relative names.

    Purely structural (no calendar): derived from the relative-level 生/克 cycles.
      元神 yuán shén — generates the 用神 (生用神; the support/source)
      忌神 jì shén   — controls the 用神 (克用神; the attacker)
      仇神 chóu shén — generates the 忌神 (生忌神 == 克元神; the attacker's source)
    The strength-judgment of these spirits (旺相休囚/空亡/日月生扶) is a downstream
    interpretation layer that needs calendar timing — deliberately out of scope here.
    """
    if yong_shen not in RELATIVE_SHENG:
        raise ValueError(f"用神 must be one of the Six Relatives, got {yong_shen!r}")

    def pred(cycle: List[str], x: str) -> str:
        return cycle[(cycle.index(x) - 1) % 5]

    yuan = pred(RELATIVE_SHENG, yong_shen)
    ji = pred(RELATIVE_KE, yong_shen)
    chou = pred(RELATIVE_SHENG, ji)
    return {"用神": yong_shen, "元神": yuan, "忌神": ji, "仇神": chou}


# ════════════════════════════════════════════════════════════════════════════════
# STEP 4 — 世應 : World and Response lines  (derived)
# ════════════════════════════════════════════════════════════════════════════════

# World line by palace position (1-based index into this list), NA_JIA.md §5.1.
# The walk: 6 → 1 → 2 → 3 → 4 → 5, then 游魂 shares 四世's line 4, 归魂 shares 三世's line 3.
_WORLD_LINE_BY_POSITION = [6, 1, 2, 3, 4, 5, 4, 3]


def world_response(position: int) -> Tuple[int, int]:
    """(world_line, response_line), each 1-6. Response is always World+3 (mod 6).

    Primary-confirmed: 《增删卜易·世应章》 — 「隔世爻兩位即是應爻」 (the Response sits
    three positions from the World), and its 乾宮 table lists 世 at 6,1,2,3,4,5,4,3,
    matching _WORLD_LINE_BY_POSITION exactly (web-fetched, zh.wikisource.org).
    """
    world = _WORLD_LINE_BY_POSITION[position - 1]
    response = ((world - 1 + 3) % 6) + 1
    return world, response


# ════════════════════════════════════════════════════════════════════════════════
# 六冲卦 / 六合卦 — hexagram-level clash / harmony  (§5.5)
# ════════════════════════════════════════════════════════════════════════════════
#
# A 六冲卦 is a hexagram in which every line and its counterpart three positions away
# (line i ↔ line i+3, the 世/應 axis) form a 六冲 pair; a 六合卦, a 六合 pair throughout.
# Derived structurally from the Na Jia branches; the derivation yields exactly the
# canonical sets — 六冲卦 = the 10 (八純卦 + 无妄 + 大壮); 六合卦 = the 8 (泰否豫賁復困旅節).
#
# Meaning (primary): 《增删卜易·六冲章》 — 「沖者散也，凡占凶事宜於沖散、占吉事而不宜」.
# 六冲卦 portends scattering / volatility / fast-but-impermanent outcomes (近病·官非·生育
# 遇之反吉 — the bad scatters; 久病·谋事遇之 則散而不成). 六合卦 is its dual: gathering,
# union, slow-holding. (六冲卦 meaning web-fetched from zh.wikisource.org 增删卜易; the
# 六合卦 *list* is structural — no verbatim primary list was reachable — but matches the
# canonical set via the engine's own derivation.)
LIUCHONG_GLOSS = "沖者散也 — the whole hexagram scatters: volatile, quick, impermanent (《增删卜易·六冲章》)"
LIUHE_GLOSS = "合者聚也 — things gather and hold: union, slow to resolve (六冲卦's dual)"


def _hexagram_branches(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> List[str]:
    """The six Na Jia branches of a hexagram, bottom→top."""
    return [b for (_s, b) in line_stems_branches(lower, upper)]


def _axis_all_in(lower, upper, pairset: frozenset) -> bool:
    """True if every 世/應-axis pair (line i ↔ line i+3) is in `pairset`."""
    br = _hexagram_branches(lower, upper)
    return all(frozenset((br[i], br[i + 3])) in pairset for i in range(3))


def is_liuchong(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> bool:
    """六冲卦 — every i↔i+3 line pair clashes (the classical 10)."""
    return _axis_all_in(lower, upper, SIX_CLASH_PAIRS)


def is_liuhe(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> bool:
    """六合卦 — every i↔i+3 line pair harmonizes (the classical 8)."""
    return _axis_all_in(lower, upper, SIX_HARMONY_PAIRS)


# ════════════════════════════════════════════════════════════════════════════════
# STEP 5 — 飛伏 : the flying and hidden spirits  (derived)
# ════════════════════════════════════════════════════════════════════════════════
#
# 飛神 (fēi shén, "flying spirit")  = the VISIBLE line of the cast hexagram at a position.
# 伏神 (fú shén, "hidden spirit")   = the line "hidden behind" it, taken from the
#                                     本宮首卦 (the pure palace / 八純卦 hexagram) at the
#                                     SAME position.
#
# Rule (dominant 增删卜易 / 京房 納甲 convention; cross-checked against the primary
# texts and independent re-derivation, 2026-06-20):
#   - 伏神 is ALWAYS taken from the pure palace hexagram at the same line position.
#     There is no mainstream 對宮卦 / 錯卦 source. (A pure hexagram carries all five
#     relatives, so any relative missing from a derived hexagram can be found in it.)
#   - A 伏神 is only "live" (worth consulting, 才有戲) when the relative it carries is
#     ABSENT from the visible hexagram (不上卦). In full practice the absence is judged
#     against BOTH the main hexagram and the 變卦 (changed hexagram); this engine flags
#     absence from the MAIN hexagram (the diviner overlays the 變卦 check).
#
ALL_RELATIVES: List[str] = ["父母", "兄弟", "子孫", "妻財", "官鬼"]


def _line_relatives(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> List[Tuple[str, str, str, str]]:
    """Per-line (stem, branch, element, relative) bottom→top, judged vs the PALACE element.

    A standalone helper used by both the chart builder and 飛伏, so neither recurses
    through the other.
    """
    pi, _pos = PALACE_GRID[(lower, upper)]
    palace_element = _trigram_meta(PALACE_HEADS[pi - 1])["element"]
    out: List[Tuple[str, str, str, str]] = []
    for stem, branch in line_stems_branches(lower, upper):
        elem = BRANCH_ELEMENT[branch]
        out.append((stem, branch, elem, six_relative(palace_element, elem)))
    return out


def missing_relatives(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> List[str]:
    """The Six Relatives ABSENT from the visible hexagram (不上卦), in canonical order.

    These are exactly the relatives whose 伏神 a diviner would go looking for.
    """
    present = {r for (_s, _b, _e, r) in _line_relatives(lower, upper)}
    return [r for r in ALL_RELATIVES if r not in present]


def flying_hidden(lower: Tuple[int, int, int], upper: Tuple[int, int, int]) -> List["HiddenSpirit"]:
    """The 飛/伏 pair at every line position (bottom→top), 伏神 from the pure palace hexagram.

    Each HiddenSpirit is marked ``surfaced=True`` when its 伏神 carries a relative absent
    from the visible hexagram — i.e. a genuinely hidden relative the diviner consults.
    """
    pi, _pos = PALACE_GRID[(lower, upper)]
    head = PALACE_HEADS[pi - 1]
    current = _line_relatives(lower, upper)
    pure = _line_relatives(head, head)  # 本宮首卦 — the source of all 伏神
    present = {r for (_s, _b, _e, r) in current}
    out: List[HiddenSpirit] = []
    for i in range(6):
        _cs, cb, _ce, cr = current[i]
        ps, pb, _pe, pr = pure[i]
        out.append(
            HiddenSpirit(
                position=i + 1,
                fei_relative=cr,
                fei_branch=cb,
                fu_relative=pr,
                fu_branch=pb,
                fu_stem=ps,
                surfaced=(pr not in present),
            )
        )
    return out


# ════════════════════════════════════════════════════════════════════════════════
# ASSEMBLY — build the full chart
# ════════════════════════════════════════════════════════════════════════════════

@dataclass
class NaJiaLine:
    """One line of a Wen Wang Gua chart, with its full装卦 annotation."""
    position: int          # 1-6 from bottom
    stem: str              # 天干
    branch: str            # 地支
    branch_pinyin: str
    element: str           # 五行 (English: Metal/Water/Wood/Fire/Earth)
    relative: str          # 六親 (Chinese)
    relative_en: str
    is_world: bool         # 世爻
    is_response: bool      # 應爻
    is_moving: bool = False  # 動爻 (only meaningful when built from a cast Hexagram)
    is_yang: bool = True


@dataclass
class HiddenSpirit:
    """A 飛/伏 pair at one line position: the visible 飛神 and the 伏神 behind it."""
    position: int          # 1-6 from bottom
    fei_relative: str      # 飛神 — the visible line's Six-Relative
    fei_branch: str
    fu_relative: str       # 伏神 — the hidden relative, from the pure palace hexagram
    fu_branch: str
    fu_stem: str
    surfaced: bool         # True when 伏神 carries a relative absent from the visible hexagram


@dataclass
class MovingLine:
    """A 動爻 (moving line) and its 變爻 (transform), with the 回頭 feedback relation."""
    position: int
    relative: str             # 本爻 the moving line's Six-Relative
    branch: str
    element: str
    transformed_stem: str     # 變爻 (transformed line, from the relating hexagram)
    transformed_branch: str
    transformed_element: str
    transformed_relative: str  # 變爻 六親, judged vs the ORIGINAL palace element
    feedback: str             # 回頭生 / 回頭克 / 比和 / 泄氣 / 耗 (/ 化進神 / 化退神)
    feedback_en: str
    is_clash: bool = False    # 回頭沖: 動爻 branch and 變爻 branch form a 六冲 pair (地支層)


@dataclass
class NaJiaChart:
    """A complete Wen Wang Gua / Liu Yao chart for one hexagram."""
    kw_number: int
    name_zh: str
    name_pinyin: str
    name_en: str
    palace_zh: str
    palace_pinyin: str
    palace_element: str
    position_index: int    # 1-8
    position_zh: str
    position_pinyin: str
    world_line: int
    response_line: int
    lines: List[NaJiaLine]               # bottom→top (index 0 = line 1)
    yong_shen: Optional[str] = None      # suggested 用神 relative, if a topic was given
    hidden: Optional[List[HiddenSpirit]] = None   # 飛伏 pairs, one per line (bottom→top)
    missing: Optional[List[str]] = None  # relatives 不上卦 (absent from the visible hexagram)
    spirits: Optional[Dict[str, dict]] = None  # 四神 (用神/元神/忌神/仇神) when a 用神 is set
    moving_dynamics: Optional[List[MovingLine]] = None  # 動爻→變爻 回頭 feedback (casts only)
    is_liuchong: bool = False           # 六冲卦 (every 世/應-axis pair clashes)
    is_liuhe: bool = False              # 六合卦 (every 世/應-axis pair harmonizes)
    world_relative: Optional[str] = None      # 持世 — the Six-Relative on the 世爻
    response_relative: Optional[str] = None   # the Six-Relative on the 應爻
    doubled_relatives: Optional[List[str]] = None  # 兩現 — relatives appearing on ≥2 lines

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def _trigram_meta(trigram: Tuple[int, int, int]) -> dict:
    return TRIGRAMS[trigram]


def build_chart_from_trigrams(
    lower: Tuple[int, int, int],
    upper: Tuple[int, int, int],
    *,
    moving: Optional[List[int]] = None,
    topic: Optional[str] = None,
) -> NaJiaChart:
    """Build the Wen Wang Gua chart from a (lower, upper) trigram pair.

    `moving`  : 1-based positions of moving lines (動爻), optional.
    `topic`   : a keyword to suggest the 用神 relative, optional.
    """
    moving = moving or []
    pi, position = PALACE_GRID[(lower, upper)]
    palace_head = PALACE_HEADS[pi - 1]
    palace_meta = _trigram_meta(palace_head)
    palace_element = palace_meta["element"]

    sb = line_stems_branches(lower, upper)
    world, response = world_response(position)

    all_lines_binary = list(lower) + list(upper)
    lines: List[NaJiaLine] = []
    for idx, (stem, branch) in enumerate(sb):
        pos = idx + 1
        element = BRANCH_ELEMENT[branch]
        rel = six_relative(palace_element, element)
        lines.append(
            NaJiaLine(
                position=pos,
                stem=stem,
                branch=branch,
                branch_pinyin=BRANCH_PINYIN[branch],
                element=element,
                relative=rel,
                relative_en=SIX_RELATIVES[rel]["en"],
                is_world=(pos == world),
                is_response=(pos == response),
                is_moving=(pos in moving),
                is_yang=bool(all_lines_binary[idx]),
            )
        )

    kw = HEXAGRAM_LOOKUP[(lower, upper)]
    name_zh, name_py, name_en = HEXAGRAM_NAMES.get(kw, ("?", "?", "Unknown"))

    yong = _suggest_yong_shen(topic) if topic else None
    hidden = flying_hidden(lower, upper)
    missing = missing_relatives(lower, upper)

    # Relative→lines map (used for 兩現, 持世/應, and the 四神 line lookup).
    rel_to_lines: Dict[str, List[int]] = {}
    for nl in lines:
        rel_to_lines.setdefault(nl.relative, []).append(nl.position)
    doubled = [r for r in ALL_RELATIVES if len(rel_to_lines.get(r, [])) >= 2]  # 兩現
    world_rel = next(nl.relative for nl in lines if nl.position == world)       # 持世
    response_rel = next(nl.relative for nl in lines if nl.position == response)

    spirits = None
    if yong:
        present = {nl.relative for nl in lines}
        role_gloss = {
            "用神": "the matter asked",
            "元神": "generates 用神 (support)",
            "忌神": "controls 用神 (attacker)",
            "仇神": "generates 忌神 (attacker's source)",
        }
        spirits = {}
        for role, rel in four_spirits(yong).items():
            spirits[role] = {
                "relative": rel,
                "lines": rel_to_lines.get(rel, []),
                "absent": rel not in present,  # 不上卦 → see its 伏神 in `hidden`
                "gloss": role_gloss[role],
            }

    return NaJiaChart(
        kw_number=kw,
        name_zh=name_zh,
        name_pinyin=name_py,
        name_en=name_en,
        palace_zh=palace_meta["chinese"],
        palace_pinyin=palace_meta["name"],
        palace_element=palace_element,
        position_index=position,
        position_zh=POSITION_NAMES[position - 1],
        position_pinyin=POSITION_PINYIN[position - 1],
        world_line=world,
        response_line=response,
        lines=lines,
        yong_shen=yong,
        hidden=hidden,
        missing=missing,
        spirits=spirits,
        is_liuchong=is_liuchong(lower, upper),
        is_liuhe=is_liuhe(lower, upper),
        world_relative=world_rel,
        response_relative=response_rel,
        doubled_relatives=doubled,
    )


def _feedback(dong_el: str, bian_el: str) -> Tuple[str, str]:
    """The 回頭 relation of a 變爻 (transformed) element back onto its 動爻 (moving) element."""
    if bian_el == dong_el:
        return "比和", "same element"
    if _generates(bian_el, dong_el):
        return "回頭生", "transformed generates moving (favorable feedback)"
    if _controls(bian_el, dong_el):
        return "回頭克", "transformed controls moving (harmful feedback)"
    if _generates(dong_el, bian_el):
        return "泄氣", "moving generates transformed (drained)"
    return "耗", "moving controls transformed (expended)"  # _controls(dong_el, bian_el)


# 化進神 / 化退神: within a SAME-element transform, advancing strengthens (進), retreating
# weakens (退). TWO rules, by element type:
#
#   Non-Earth (金木水火): the 生(長生)→旺 pair. 進 = 生→旺 (亥→子, 寅→卯, 巳→午, 申→酉);
#                          退 = 旺→生 (reverse).
#   Earth (辰戌丑未):       the four-season cycle 丑→辰→未→戌→丑 (季冬→季春→季夏→季秋).
#                          進 = one step forward, 退 = one step back. (Earth has no 長生→旺
#                          pair among 辰戌丑未 — its 長生/帝旺 fall on non-Earth branches — so
#                          the 生→旺 rule structurally cannot serve Earth; the texts use the
#                          season cycle instead.)
#
# Sources (2026-06-20). The Earth rule is CLASSICAL, not a minority school:
# 《增删卜易》 and 《卜筮正宗》 both give exactly this four-season ordering, in agreement
# (verified by web-fetched primary quotes). A check of the primary texts corrected an initial
# misreading: the four-season rule had appeared to be a modern minority view, but 《增删卜易》
# and 《卜筮正宗》 both give it — a reminder that a fetched primary source outranks plausible
# reconstruction.
#
# Why it is applied UNCONDITIONALLY (no opt-in): across all 64 hexagrams × 6 lines, the ONLY
# Earth→Earth transforms that ever occur in 动变 are the four ADJACENT-step pairs 丑↔辰 and
# 未↔戌 (each 8×). The pairs the later texts dispute (辰→未, 戌→丑) and the opposite pairs
# (辰↔戌, 丑↔未) never occur at all. On every occurring case, ALL schools (增删卜易, 卜筮正宗,
# 易隐, modern primers) agree — so the dispute is empty in practice and needs no flag.
# (Default is ON, per the primary sources.)
_SHENG_BRANCH = {"亥", "寅", "巳", "申"}  # 四長生 (birth) branches — one per non-Earth element
_WANG_BRANCH = {"子", "卯", "午", "酉"}   # 四旺 (peak) branches — one per non-Earth element
_EARTH_ADVANCE_CYCLE = ["辰", "未", "戌", "丑"]  # 進 = one forward step (= 增删卜易 丑→辰→未→戌→丑)


def _earth_jin_tui(dong_branch: str, bian_branch: str) -> Optional[Tuple[str, str]]:
    """Earth-only 化進神/化退神 by the classical four-season cycle (增删卜易 / 卜筮正宗).

    進 = one step forward in _EARTH_ADVANCE_CYCLE (丑→辰, 辰→未, 未→戌, 戌→丑).
    退 = one step backward.
    Opposite branches (辰↔戌, 未↔丑) are two steps apart (and are 冲, never adjacent), so
    return None. Non-Earth branches return None too (handled by the 生→旺 rule upstream).
    """
    if dong_branch == bian_branch:
        return None
    try:
        i = _EARTH_ADVANCE_CYCLE.index(dong_branch)
        j = _EARTH_ADVANCE_CYCLE.index(bian_branch)
    except ValueError:
        return None  # not both Earth
    delta = (j - i) % 4
    if delta == 1:
        return "化進神", "Earth advances one seasonal step (strengthening)"
    if delta == 3:
        return "化退神", "Earth retreats one seasonal step (weakening)"
    return None  # delta == 2: opposite Earth branches (冲) — never occur in 动变 anyway


def _jin_tui(dong_branch: str, bian_branch: str) -> Optional[Tuple[str, str]]:
    """Classify a same-element transform as 化進神 / 化退神, or None if undecidable.

    Only call when the 動爻 and 變爻 are the SAME element (a 比和 transform). Non-Earth uses
    the 生→旺 pair; Earth uses the four-season cycle. Both rules are classical and unanimous
    on every transform that actually occurs in 动变.
    """
    if dong_branch in _SHENG_BRANCH and bian_branch in _WANG_BRANCH:
        return "化進神", "advances toward the element's peak (strengthening)"
    if dong_branch in _WANG_BRANCH and bian_branch in _SHENG_BRANCH:
        return "化退神", "retreats from the element's peak (weakening)"
    return _earth_jin_tui(dong_branch, bian_branch)  # Earth four-season; None if non-adjacent


def moving_line_dynamics(hexagram: "Hexagram") -> List["MovingLine"]:
    """For each 動爻 (moving line) of a cast, its 變爻 (transform) and the 回頭 feedback.

    Purely structural (no calendar). The 變爻's 六親 is judged against the ORIGINAL
    hexagram's palace element (本宮五行) — the standard rule: the 變卦 lines are not
    re-assigned to the changed hexagram's palace. Same-element transforms are further
    classified 化進神/化退神 (non-Earth by 生→旺, Earth by the classical four-season cycle).
    """
    if not hexagram.has_moving_lines:
        return []
    lower, upper = hexagram.lower_trigram, hexagram.upper_trigram
    pi, _pos = PALACE_GRID[(lower, upper)]
    palace_element = _trigram_meta(PALACE_HEADS[pi - 1])["element"]
    original = _line_relatives(lower, upper)
    relating = hexagram.get_relating_hexagram()
    trans = line_stems_branches(relating.lower_trigram, relating.upper_trigram)
    out: List[MovingLine] = []
    for pos in hexagram.moving_lines:
        i = pos - 1
        _s, branch, element, relative = original[i]
        t_stem, t_branch = trans[i]
        t_element = BRANCH_ELEMENT[t_branch]
        t_relative = six_relative(palace_element, t_element)
        fb, fb_en = _feedback(element, t_element)
        if fb == "比和":  # refine a same-element transform into 化進神/化退神 where defined
            jt = _jin_tui(branch, t_branch)
            if jt is not None:
                fb, fb_en = jt
        clash = frozenset((branch, t_branch)) in SIX_CLASH_PAIRS  # 回頭沖 (地支層)
        out.append(
            MovingLine(
                position=pos,
                relative=relative,
                branch=branch,
                element=element,
                transformed_stem=t_stem,
                transformed_branch=t_branch,
                transformed_element=t_element,
                transformed_relative=t_relative,
                feedback=fb,
                feedback_en=fb_en,
                is_clash=clash,
            )
        )
    return out


def build_chart(hexagram: "Hexagram", *, topic: Optional[str] = None) -> NaJiaChart:
    """Build the Wen Wang Gua chart for a cast :class:`Hexagram` (carries moving lines)."""
    chart = build_chart_from_trigrams(
        hexagram.lower_trigram,
        hexagram.upper_trigram,
        moving=hexagram.moving_lines,
        topic=topic,
    )
    chart.moving_dynamics = moving_line_dynamics(hexagram)
    return chart


def build_chart_by_number(kw_number: int, *, topic: Optional[str] = None) -> NaJiaChart:
    """Build the chart for a King-Wen hexagram number (1-64), no moving lines."""
    for (lower, upper), kw in HEXAGRAM_LOOKUP.items():
        if kw == kw_number:
            return build_chart_from_trigrams(lower, upper, topic=topic)
    raise ValueError(f"King-Wen number must be 1..64, got {kw_number}")


def _suggest_yong_shen(topic: str) -> Optional[str]:
    t = topic.lower()
    for keyword, relative in YONG_SHEN_BY_TOPIC.items():
        if keyword in t:
            return relative
    return None


# ════════════════════════════════════════════════════════════════════════════════
# RENDERING
# ════════════════════════════════════════════════════════════════════════════════

def format_chart(chart: NaJiaChart) -> str:
    """Render a chart as an aligned text table (bottom line last, as drawn 自下而上)."""
    lines_out: List[str] = []
    lines_out.append(
        f"{chart.name_zh} {chart.name_pinyin} — {chart.name_en}  (King-Wen #{chart.kw_number})"
    )
    lines_out.append(
        f"宮 Palace: {chart.palace_zh}宮 {chart.palace_pinyin} "
        f"({chart.palace_element}) · {chart.position_zh} {chart.position_pinyin}"
    )
    lines_out.append(
        f"世 World: line {chart.world_line} ({chart.world_relative})   "
        f"應 Response: line {chart.response_line} ({chart.response_relative})"
        + (f"   用神 Yòng Shén: {chart.yong_shen}" if chart.yong_shen else "")
    )
    if chart.is_liuchong:
        lines_out.append(f"卦象: 六冲卦 (Six-Clash) — {LIUCHONG_GLOSS}")
    elif chart.is_liuhe:
        lines_out.append(f"卦象: 六合卦 (Six-Harmony) — {LIUHE_GLOSS}")
    if chart.doubled_relatives:
        dbl = "·".join(f"{r} {SIX_RELATIVES[r]['en']}" for r in chart.doubled_relatives)
        lines_out.append(f"兩現 (relatives on ≥2 lines): {dbl}  (operative one chosen by 臨世應/動/旺/月日 — partly calendar)")
    lines_out.append("")
    header = f"{'Line':>4}  {'爻':<6}  {'干支':<5} {'五行':<6} {'六親':<10} {'世/應':<5} {'動'}"
    lines_out.append(header)
    lines_out.append("─" * 52)
    for nl in reversed(chart.lines):  # top line first, visually 自上而下
        glyph = "▬▬▬▬▬" if nl.is_yang else "▬▬ ▬▬"
        gz = f"{nl.stem}{nl.branch}"
        wy = "世" if nl.is_world else ("應" if nl.is_response else "")
        mv = "○" if nl.is_moving else ""
        rel = f"{nl.relative} {nl.relative_en}"
        lines_out.append(
            f"{nl.position:>4}  {glyph:<6}  {gz:<5} {nl.element:<6} {rel:<14} {wy:<5} {mv}"
        )

    # 飛伏 — show only the live (surfaced) hidden spirits; the diviner consults these.
    surfaced = [h for h in (chart.hidden or []) if h.surfaced]
    lines_out.append("")
    if not chart.missing:
        lines_out.append("伏神 Hidden spirits: none — all five relatives appear (六親俱全).")
    else:
        miss = "·".join(f"{m} {SIX_RELATIVES[m]['en']}" for m in chart.missing)
        lines_out.append(f"伏神 Hidden spirits (不上卦: {miss}):")
        for h in surfaced:
            fu_el = BRANCH_ELEMENT[h.fu_branch]
            lines_out.append(
                f"   line {h.position}: {h.fu_relative} {h.fu_stem}{h.fu_branch}({fu_el}) "
                f"伏 behind 飛神 {h.fei_relative} {h.fei_branch}"
            )

    # 四神 — only when a 用神 was selected (via topic).
    if chart.spirits:
        lines_out.append("")
        lines_out.append(f"四神 Four spirits (用神 = {chart.spirits['用神']['relative']}):")
        for role in ("用神", "元神", "忌神", "仇神"):
            s = chart.spirits[role]
            where = ("lines " + ",".join(map(str, s["lines"]))) if s["lines"] else "不上卦 (hidden — see 伏神)"
            lines_out.append(f"   {role} {s['relative']:<2} — {s['gloss']:<32} {where}")

    # 動爻 → 變爻 dynamics (only present on a cast with moving lines).
    if chart.moving_dynamics:
        lines_out.append("")
        lines_out.append("動爻 → 變爻 (moving-line transforms):")
        for m in chart.moving_dynamics:
            be = BRANCH_ELEMENT[m.transformed_branch]
            clash = "  回頭沖 (地支相沖)" if m.is_clash else ""
            lines_out.append(
                f"   line {m.position}: {m.relative} {m.branch}({m.element}) → "
                f"{m.transformed_relative} {m.transformed_stem}{m.transformed_branch}({be})  "
                f"{m.feedback} ({m.feedback_en}){clash}"
            )
    return "\n".join(lines_out)


# ════════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════════

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="納甲 / 文王卦 / 六爻 — build the Wen Wang Gua chart for a hexagram."
    )
    parser.add_argument(
        "hexagram", type=int, nargs="?",
        help="King-Wen hexagram number (1-64). Omit to print all 64 palace assignments.",
    )
    parser.add_argument("--topic", "-t", default=None, help="topic keyword to suggest the 用神")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = parser.parse_args(argv)

    if args.hexagram is None:
        # Print the derived palace map for all 64 — a quick visual partition check.
        rows = []
        for (lower, upper), (pi, pos) in PALACE_GRID.items():
            kw = HEXAGRAM_LOOKUP[(lower, upper)]
            head = TRIGRAMS[PALACE_HEADS[pi - 1]]["chinese"]
            rows.append((kw, head, POSITION_NAMES[pos - 1]))
        rows.sort()
        for kw, head, posname in rows:
            zh, py, en = HEXAGRAM_NAMES[kw]
            print(f"#{kw:>2} {zh:<4} {py:<10} — {head}宮 {posname}")
        return 0

    if not (1 <= args.hexagram <= 64):
        parser.error("hexagram must be 1..64")

    chart = build_chart_by_number(args.hexagram, topic=args.topic)
    if args.json:
        import json
        print(json.dumps(chart.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(format_chart(chart))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
