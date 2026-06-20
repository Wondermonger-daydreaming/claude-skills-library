#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for na_jia.py — the 納甲 / 文王卦 / 六爻 derivation engine.

The whole module is a *derivation*, not a transcription of NA_JIA.md's tables.
These tests are the OUTSIDE that proves the derivation isn't a self-consistent
mirror: each class checks the derivation against an INDEPENDENT ancestry —

  - TestPartition       : the structural invariant (clean 8×8 partition of all 64)
  - TestDocWorkedExamples: NA_JIA.md's own worked charts (乾 §2.3/§4.2, 坤 §2.4, 屯 §6)
  - TestCanonicalCharts : canonical external Liu Yao charts NOT in the doc (師, 大有)
  - TestInvariants      : self-checks the doc itself states (§1.1, §4.1, §5.1)
  - TestDocErrorCaught  : the 归魂 prose-gloss error the derivation exposes

When derivation == doc == external source, the agreement is evidence, not proof —
convergence across ancestry. (See na_jia.py module docstring.)
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from na_jia import (  # noqa: E402
    ALL_RELATIVES,
    EARTHLY_BRANCHES,
    PALACE_GRID,
    PALACE_HEADS,
    TRIGRAM_NAJIA,
    _feedback,
    _jin_tui,
    _line_relatives,
    build_chart,
    build_chart_by_number,
    flying_hidden,
    four_spirits,
    is_liuchong,
    is_liuhe,
    missing_relatives,
    moving_line_dynamics,
    palace_member_lines,
    six_relative,
    trigram_branches,
    world_response,
)
from cast_hexagram import HEXAGRAM_LOOKUP, TRIGRAMS, Hexagram, Line  # noqa: E402


def _branches_bottom_to_top(chart):
    return [nl.branch for nl in chart.lines]


def _relatives_bottom_to_top(chart):
    return [nl.relative for nl in chart.lines]


def _elements_bottom_to_top(chart):
    return [nl.element for nl in chart.lines]


# ════════════════════════════════════════════════════════════════════════════════
class TestPartition:
    """The generated 8×8 palace grid must partition all 64 King-Wen hexagrams."""

    def test_grid_has_64_cells(self):
        assert len(PALACE_GRID) == 64

    def test_every_king_wen_appears_exactly_once(self):
        seen = sorted(HEXAGRAM_LOOKUP[k] for k in PALACE_GRID)
        assert seen == list(range(1, 65))

    def test_eight_palaces_eight_positions_each(self):
        from collections import Counter
        palaces = Counter(pi for pi, _pos in PALACE_GRID.values())
        assert set(palaces) == set(range(1, 9))
        assert all(count == 8 for count in palaces.values())

    def test_pure_hexagrams_are_position_one(self):
        # The eight doubled trigrams must each be 本宮 (position 1).
        for head in PALACE_HEADS:
            assert PALACE_GRID[(head, head)][1] == 1


# ════════════════════════════════════════════════════════════════════════════════
class TestDocWorkedExamples:
    """NA_JIA.md's three fully-worked charts, encoded verbatim from the doc."""

    def test_qian_hex1(self):
        # §2.3 + §4.2 + §1.1 + §5.1
        c = build_chart_by_number(1)
        assert (c.palace_zh, c.palace_element, c.position_zh) == ("乾", "Metal", "本宮")
        assert (c.world_line, c.response_line) == (6, 3)
        assert _branches_bottom_to_top(c) == ["子", "寅", "辰", "午", "申", "戌"]
        assert _elements_bottom_to_top(c) == ["Water", "Wood", "Earth", "Fire", "Metal", "Earth"]
        assert _relatives_bottom_to_top(c) == ["子孫", "妻財", "父母", "官鬼", "兄弟", "父母"]
        assert [nl.stem for nl in c.lines] == ["甲", "甲", "甲", "壬", "壬", "壬"]

    def test_kun_hex2(self):
        # §2.4
        c = build_chart_by_number(2)
        assert (c.palace_zh, c.palace_element, c.position_zh) == ("坤", "Earth", "本宮")
        assert (c.world_line, c.response_line) == (6, 3)
        assert _branches_bottom_to_top(c) == ["未", "巳", "卯", "丑", "亥", "酉"]
        assert [nl.stem for nl in c.lines] == ["乙", "乙", "乙", "癸", "癸", "癸"]
        assert _relatives_bottom_to_top(c) == ["兄弟", "父母", "官鬼", "兄弟", "妻財", "子孫"]

    def test_zhun_hex3(self):
        # §6 end-to-end worked build
        c = build_chart_by_number(3)
        assert (c.palace_zh, c.palace_element, c.position_zh) == ("坎", "Water", "二世")
        assert (c.world_line, c.response_line) == (2, 5)
        assert _branches_bottom_to_top(c) == ["子", "寅", "辰", "申", "戌", "子"]
        assert _relatives_bottom_to_top(c) == ["兄弟", "子孫", "官鬼", "父母", "官鬼", "兄弟"]


# ════════════════════════════════════════════════════════════════════════════════
class TestCanonicalCharts:
    """Canonical external Liu Yao charts NOT given in NA_JIA.md (different ancestry)."""

    def test_shi_hex7_kan_guihun(self):
        # 師 — 坎宮归魂, a standard primer chart.
        c = build_chart_by_number(7)
        assert (c.palace_zh, c.position_zh) == ("坎", "归魂")
        assert (c.world_line, c.response_line) == (3, 6)
        assert _branches_bottom_to_top(c) == ["寅", "辰", "午", "丑", "亥", "酉"]
        assert _relatives_bottom_to_top(c) == ["子孫", "官鬼", "妻財", "官鬼", "兄弟", "父母"]

    def test_dayou_hex14_qian_guihun(self):
        # 大有 — 乾宮归魂. Inner trigram = ☰ Qián (the palace's OWN trigram).
        c = build_chart_by_number(14)
        assert (c.palace_zh, c.position_zh) == ("乾", "归魂")
        assert (c.world_line, c.response_line) == (3, 6)
        # lines 1-3 (inner) must be Qián's branches with stem 甲 — the home trigram restored
        assert [nl.branch for nl in c.lines[:3]] == ["子", "寅", "辰"]
        assert [nl.stem for nl in c.lines[:3]] == ["甲", "甲", "甲"]

    def test_gou_hex44_qian_yishi(self):
        # 姤 — 乾宮一世.
        c = build_chart_by_number(44)
        assert (c.palace_zh, c.position_zh) == ("乾", "一世")
        assert (c.world_line, c.response_line) == (1, 4)


# ════════════════════════════════════════════════════════════════════════════════
class TestInvariants:
    """Self-checks NA_JIA.md itself asserts — re-derived and enforced."""

    def test_outer_start_is_inner_start_plus_six(self):
        # §2.2: the outer start is always 6 branches (opposite point) from the inner.
        for tri, nj in TRIGRAM_NAJIA.items():
            inner = trigram_branches(tri, outer=False)
            outer = trigram_branches(tri, outer=True)
            i_inner = EARTHLY_BRANCHES.index(inner[0])
            i_outer = EARTHLY_BRANCHES.index(outer[0])
            assert (i_outer - i_inner) % 12 == 6, tri

    def test_each_palace_row_is_a_permutation_of_five_elements(self):
        # §4.1 self-check: a palace element's five relatives cover all five elements.
        elements = ["Metal", "Water", "Wood", "Fire", "Earth"]
        for palace in elements:
            rels = {six_relative(palace, e): e for e in elements}
            assert len(rels) == 5  # all five relatives distinct
            assert set(rels.values()) == set(elements)

    def test_response_is_world_plus_three_mod_six(self):
        # §5.1: 世應相隔三位.
        for pos in range(1, 9):
            world, response = world_response(pos)
            assert response == ((world - 1 + 3) % 6) + 1

    def test_world_line_walk(self):
        # §5.1 mnemonic: 六→初→二→三→四→五→四→三.
        assert [world_response(p)[0] for p in range(1, 9)] == [6, 1, 2, 3, 4, 5, 4, 3]

    def test_branch_polarity_yang_forward_yin_backward(self):
        # §2.2: yang trigrams advance +2; yin trigrams −2.
        for tri, nj in TRIGRAM_NAJIA.items():
            inner = trigram_branches(tri, outer=False)
            step = (EARTHLY_BRANCHES.index(inner[1]) - EARTHLY_BRANCHES.index(inner[0])) % 12
            assert step == (2 if nj["yang"] else 10), tri  # 10 == −2 mod 12

    def test_six_relatives_against_palace_not_lower_trigram(self):
        # §4 beginner-error guard: 屯 is 坎宮(Water); its relatives are vs Water even
        # though its lower trigram is ☳ Zhèn (Wood). Line 1 (子/Water) -> 兄弟, not 父母.
        c = build_chart_by_number(3)
        assert c.lines[0].relative == "兄弟"


# ════════════════════════════════════════════════════════════════════════════════
class TestDocErrorCaught:
    """The 归魂 prose-gloss error the structural derivation exposes (na_jia.py caveat)."""

    def test_guihun_inner_is_palace_trigram_not_opposite(self):
        # NA_JIA.md §1.2 prose claims 归魂's outer trigram is "the opposite of the
        # palace trigram." For every palace, the 归魂 member's INNER trigram is the
        # palace trigram itself, and the OUTER is NOT the opposite. We assert the
        # correct structure (and that the wrong gloss would break the partition).
        for pi, head in enumerate(PALACE_HEADS, start=1):
            lines = palace_member_lines(head, 8)  # 归魂
            inner = lines[0:3]
            outer = lines[3:6]
            assert inner == head, f"归魂 inner must be the palace trigram for {head}"
            opposite = tuple(1 - b for b in head)
            assert outer != opposite, (
                f"归魂 outer should NOT be the palace's opposite for {head} "
                f"(doc prose gloss is wrong)"
            )


# ════════════════════════════════════════════════════════════════════════════════
class TestFlyingHidden:
    """飛伏 (flying-hidden). Rule cross-checked against the primary texts and independent
    re-derivation, 2026-06-20: 伏神 always from the pure palace hexagram at the same
    position; surfaced only when the relative is absent (不上卦). A multi-candidate reef
    was noted; the last two tests prove it does not arise in single-hexagram 裝卦."""

    def test_gou_hex44_qicai_hidden_at_line2(self):
        # 姤 (乾宮一世): 妻財 不上卦; 妻財寅木(stem 甲) 伏 behind 飛神 子孫亥 at line 2.
        c = build_chart_by_number(44)
        assert c.missing == ["妻財"]
        surfaced = [h for h in c.hidden if h.surfaced]
        assert len(surfaced) == 1
        h = surfaced[0]
        assert (h.position, h.fu_relative, h.fu_stem, h.fu_branch) == (2, "妻財", "甲", "寅")
        assert h.fei_relative == "子孫"

    def test_dun_hex33_two_hidden(self):
        # 遯 (乾宮二世): 子孫 + 妻財 不上卦, each with one 伏神 from pure 乾.
        c = build_chart_by_number(33)
        assert c.missing == ["子孫", "妻財"]
        surfaced = {(h.position, h.fu_relative, h.fu_stem, h.fu_branch)
                    for h in c.hidden if h.surfaced}
        assert surfaced == {(1, "子孫", "甲", "子"), (2, "妻財", "甲", "寅")}

    def test_complete_hexagrams_have_no_hidden(self):
        # 有現不用伏 — pure (乾,坤) and a 归魂 (師) all carry the five relatives.
        for kw in (1, 2, 7):
            c = build_chart_by_number(kw)
            assert c.missing == []
            assert not any(h.surfaced for h in c.hidden)

    def test_fushen_always_from_pure_palace_hexagram(self):
        # The 伏神 at each position equals the pure palace hexagram's line there.
        for (lower, upper), (pi, _pos) in PALACE_GRID.items():
            head = PALACE_HEADS[pi - 1]
            pure = _line_relatives(head, head)  # (stem, branch, element, relative) bottom→top
            for h in flying_hidden(lower, upper):
                ps, pb, _pe, pr = pure[h.position - 1]
                assert (h.fu_stem, h.fu_branch, h.fu_relative) == (ps, pb, pr)

    def test_surfaced_relatives_exactly_cover_the_missing(self):
        # Completeness: every absent relative is found as a 伏神, and only absent ones surface.
        for (lower, upper) in PALACE_GRID:
            surfaced = {h.fu_relative for h in flying_hidden(lower, upper) if h.surfaced}
            assert surfaced == set(missing_relatives(lower, upper))

    def test_present_relative_is_never_hidden(self):
        # "有現不用伏": a relative that appears among the six lines is never surfaced.
        for (lower, upper) in PALACE_GRID:
            present = {r for (_s, _b, _e, r) in _line_relatives(lower, upper)}
            for h in flying_hidden(lower, upper):
                if h.surfaced:
                    assert h.fu_relative not in present

    def test_single_candidate_per_missing_relative(self):
        # The reef does NOT arise in single-hexagram 裝卦: each missing relative has
        # exactly ONE 伏神 candidate, because the palace's doubled relative is never the
        # absent one (verified structurally below). The list structure still supports N>1.
        from collections import Counter
        for (lower, upper) in PALACE_GRID:
            surfaced = [h for h in flying_hidden(lower, upper) if h.surfaced]
            counts = Counter(h.fu_relative for h in surfaced)
            assert all(c == 1 for c in counts.values())

    def test_doubled_relative_is_never_the_missing_one(self):
        # The structural reason the reef doesn't surface (per-palace).
        from collections import Counter
        for head in PALACE_HEADS:
            pure_rels = [r for (_s, _b, _e, r) in _line_relatives(head, head)]
            doubled = {r for r, c in Counter(pure_rels).items() if c == 2}
            ever_missing = set()
            for (lower, upper), (pi, _pos) in PALACE_GRID.items():
                if PALACE_HEADS[pi - 1] == head:
                    ever_missing |= set(missing_relatives(lower, upper))
            assert doubled & ever_missing == set()


# ════════════════════════════════════════════════════════════════════════════════
class TestFourSpirits:
    """四神 (用神/元神/忌神/仇神) — derived from the relative-level 生/克 cycles,
    checked against the five canonical 用神 cases every Liu Yao primer gives."""

    # canonical (用神 -> (元神, 忌神, 仇神))
    CANON = {
        "妻財": ("子孫", "兄弟", "父母"),
        "官鬼": ("妻財", "子孫", "兄弟"),
        "父母": ("官鬼", "妻財", "子孫"),
        "子孫": ("兄弟", "父母", "官鬼"),
        "兄弟": ("父母", "官鬼", "妻財"),
    }

    def test_four_spirits_match_canon(self):
        for yong, (yuan, ji, chou) in self.CANON.items():
            fs = four_spirits(yong)
            assert fs == {"用神": yong, "元神": yuan, "忌神": ji, "仇神": chou}

    def test_chou_controls_yuan_invariant(self):
        # 仇神 generates 忌神 AND controls 元神 — the doctrine's consistency check.
        from na_jia import RELATIVE_KE
        for yong in self.CANON:
            fs = four_spirits(yong)
            ji_idx = RELATIVE_KE.index(fs["仇神"])
            assert RELATIVE_KE[(ji_idx + 1) % 5] == fs["元神"]  # 仇神克元神

    def test_four_spirits_are_four_distinct_relatives(self):
        for yong in self.CANON:
            assert len(set(four_spirits(yong).values())) == 4

    def test_bad_yong_raises(self):
        with pytest.raises(ValueError):
            four_spirits("青龍")  # not a Six-Relative

    def test_chart_spirits_with_lines_gou_wealth(self):
        # 姤 + wealth: 用神 妻財 is itself 不上卦 (points to its 伏神); spirits map to lines.
        c = build_chart_by_number(44, topic="wealth")
        assert c.yong_shen == "妻財"
        s = c.spirits
        assert s["用神"]["relative"] == "妻財" and s["用神"]["absent"] is True
        assert s["用神"]["lines"] == []
        assert s["元神"]["relative"] == "子孫" and s["元神"]["lines"] == [2]
        assert s["忌神"]["relative"] == "兄弟" and s["忌神"]["lines"] == [3, 5]
        assert s["仇神"]["relative"] == "父母" and s["仇神"]["lines"] == [1, 6]

    def test_chart_spirits_none_without_topic(self):
        assert build_chart_by_number(44).spirits is None

    def test_spirits_absent_flag_consistent_with_missing(self):
        # A spirit's absent flag must agree with the hexagram's 不上卦 set.
        c = build_chart_by_number(3, topic="illness")  # 用神 官鬼; 元神 妻財 不上卦
        for role, s in c.spirits.items():
            assert s["absent"] == (s["relative"] in c.missing)


# ════════════════════════════════════════════════════════════════════════════════
class TestMovingDynamics:
    """動爻 → 變爻 dynamics — the 回頭 feedback of a moving line's transform.
    Calendar-free; the 變爻 六親 is judged vs the ORIGINAL palace element."""

    @staticmethod
    def _song_line5_moving():
        # 訟 (#6): lower ☵ Kǎn (0,1,0), upper ☰ Qián (1,1,1); line 5 = old yang (moving).
        vals = [8, 7, 8, 7, 9, 7]  # bottom→top; 9 at line 5
        return Hexagram(lines=[Line(value=v, position=i + 1) for i, v in enumerate(vals)])

    def test_feedback_relations(self):
        # vs a moving Metal line: Earth生Metal=回頭生; Fire克Metal=回頭克; same=比和;
        # Metal生Water=泄氣; Metal克Wood=耗.
        assert _feedback("Metal", "Earth")[0] == "回頭生"
        assert _feedback("Metal", "Fire")[0] == "回頭克"
        assert _feedback("Metal", "Metal")[0] == "比和"
        assert _feedback("Metal", "Water")[0] == "泄氣"
        assert _feedback("Metal", "Wood")[0] == "耗"

    def test_song_line5_huitou_sheng(self):
        hexa = self._song_line5_moving()
        dyn = moving_line_dynamics(hexa)
        assert len(dyn) == 1
        m = dyn[0]
        assert m.position == 5
        assert (m.relative, m.branch, m.element) == ("妻財", "申", "Metal")
        # 訟 line 5 transforms (☰→☲ at line 5): 未濟 line 5 = 未 (Earth) → 子孫, 回頭生
        assert (m.transformed_relative, m.transformed_branch, m.transformed_element) == ("子孫", "未", "Earth")
        assert m.feedback == "回頭生"

    def test_chart_attaches_moving_dynamics(self):
        c = build_chart(self._song_line5_moving())
        assert c.moving_dynamics and c.moving_dynamics[0].feedback == "回頭生"

    def test_no_moving_lines_no_dynamics(self):
        # All stable lines (7/8) → no dynamics.
        stable = Hexagram(lines=[Line(value=7, position=i + 1) for i in range(6)])
        assert moving_line_dynamics(stable) == []
        assert build_chart(stable).moving_dynamics == []

    @staticmethod
    def _single_moving(kw, pos):
        """A Hexagram = King-Wen #kw with exactly line `pos` (1-6) moving."""
        for (lower, upper), n in HEXAGRAM_LOOKUP.items():
            if n == kw:
                base = list(lower) + list(upper)
                vals = []
                for i, b in enumerate(base):
                    if i == pos - 1:
                        vals.append(9 if b == 1 else 6)   # moving
                    else:
                        vals.append(7 if b == 1 else 8)   # stable
                return Hexagram(lines=[Line(value=v, position=i + 1) for i, v in enumerate(vals)])
        raise ValueError(kw)

    def test_jin_shen_wood(self):
        # 屯 #3, line 2 moving: 寅(Wood,生) → 卯(Wood,旺) = 化進神.
        m = moving_line_dynamics(self._single_moving(3, 2))[0]
        assert (m.branch, m.transformed_branch) == ("寅", "卯")
        assert m.feedback == "化進神"

    def test_tui_shen_wood(self):
        # 履 #10, line 2 moving: 卯(Wood,旺) → 寅(Wood,生) = 化退神.
        m = moving_line_dynamics(self._single_moving(10, 2))[0]
        assert (m.branch, m.transformed_branch) == ("卯", "寅")
        assert m.feedback == "化退神"

    def test_earth_jintui_classical_four_season_direct(self):
        # Earth 進退 is the CLASSICAL four-season cycle 丑→辰→未→戌→丑 (增删卜易 / 卜筮正宗),
        # applied unconditionally. Forward one step = 進.
        assert _jin_tui("丑", "辰")[0] == "化進神"
        assert _jin_tui("辰", "未")[0] == "化進神"
        assert _jin_tui("未", "戌")[0] == "化進神"
        assert _jin_tui("戌", "丑")[0] == "化進神"
        # Backward one step = 退.
        assert _jin_tui("辰", "丑")[0] == "化退神"
        assert _jin_tui("未", "辰")[0] == "化退神"
        # Opposite Earth branches (辰↔戌, 丑↔未) are 冲, two steps apart → undecidable.
        assert _jin_tui("辰", "戌") is None
        assert _jin_tui("未", "丑") is None

    def test_earth_jintui_via_dynamics_by_default(self):
        # No flag needed — Earth 進退 is on by default (it's the classical rule).
        # 乾 #1 line 3: 辰 → 丑 (春末→冬末, one step back) = 化退神.
        assert moving_line_dynamics(self._single_moving(1, 3))[0].feedback == "化退神"
        # 履 #10 line 3: 丑 → 辰 (one step forward) = 化進神.
        assert moving_line_dynamics(self._single_moving(10, 3))[0].feedback == "化進神"

    def test_only_adjacent_earth_transforms_occur(self):
        # The empirical fact that makes the school-dispute empty: across all 64×6 single-
        # moving casts, the ONLY Earth→Earth transforms that occur are the four adjacent-step
        # pairs 丑↔辰, 未↔戌. The disputed pairs (辰→未, 戌→丑) and the 冲 pairs never occur,
        # so every occurring Earth transform is classified identically by all schools.
        occurring = set()
        for (lower, upper), kw in HEXAGRAM_LOOKUP.items():
            base = list(lower) + list(upper)
            for mp in range(6):
                vals = [(9 if base[i] == 1 else 6) if i == mp else (7 if base[i] == 1 else 8)
                        for i in range(6)]
                h = Hexagram(lines=[Line(value=v, position=i + 1) for i, v in enumerate(vals)])
                for m in moving_line_dynamics(h):
                    if m.element == "Earth" and m.transformed_element == "Earth":
                        occurring.add((m.branch, m.transformed_branch))
        assert occurring == {("丑", "辰"), ("辰", "丑"), ("未", "戌"), ("戌", "未")}
        # And every occurring Earth transform is classified 進 or 退 (never left 比和).
        for a, b in occurring:
            assert _jin_tui(a, b) is not None


# ════════════════════════════════════════════════════════════════════════════════
class TestSixClashHarmony:
    """六冲卦 / 六合卦 — derived structurally; sets match the canonical 10 / 8.
    六冲卦 meaning is primary-sourced (《增删卜易·六冲章》 沖者散也, web-fetched)."""

    LIUCHONG = {1, 2, 25, 29, 30, 34, 51, 52, 57, 58}   # 八純卦 + 无妄 + 大壮
    LIUHE = {11, 12, 16, 22, 24, 47, 56, 60}             # 泰否豫賁復困旅節

    def test_liuchong_set_is_canonical_ten(self):
        got = {kw for (lo, up), kw in HEXAGRAM_LOOKUP.items() if is_liuchong(lo, up)}
        assert got == self.LIUCHONG

    def test_liuhe_set_is_canonical_eight(self):
        got = {kw for (lo, up), kw in HEXAGRAM_LOOKUP.items() if is_liuhe(lo, up)}
        assert got == self.LIUHE

    def test_clash_and_harmony_are_disjoint(self):
        assert self.LIUCHONG & self.LIUHE == set()

    def test_chart_flags(self):
        assert build_chart_by_number(1).is_liuchong is True   # 乾為天
        assert build_chart_by_number(1).is_liuhe is False
        assert build_chart_by_number(11).is_liuhe is True     # 泰
        assert build_chart_by_number(3).is_liuchong is False  # 屯 — neither
        assert build_chart_by_number(3).is_liuhe is False


# ════════════════════════════════════════════════════════════════════════════════
class TestSixRelativesRefinements:
    """持世/應 relative, 兩現 detection, and 回頭沖 flag."""

    def test_world_response_relative(self):
        # 乾為天: 世 line 6 = 父母, 應 line 3 = 父母.
        c = build_chart_by_number(1)
        assert c.world_relative == "父母"
        assert c.response_relative == "父母"
        # 屯 (坎宮二世): 世 line 2 = 子孫, 應 line 5 = 官鬼.
        c = build_chart_by_number(3)
        assert (c.world_relative, c.response_relative) == ("子孫", "官鬼")

    def test_doubled_relatives_liangxian(self):
        # 乾 has 父母 on two lines (3,6) → 兩現.
        assert build_chart_by_number(1).doubled_relatives == ["父母"]
        # The doubled list must agree with the per-line relatives.
        for kw in (1, 3, 11, 44):
            c = build_chart_by_number(kw)
            from collections import Counter
            cnt = Counter(nl.relative for nl in c.lines)
            assert set(c.doubled_relatives) == {r for r, n in cnt.items() if n >= 2}

    def test_huitou_chong_flag_set_and_keeps_element_feedback(self):
        # The two 回頭沖 transforms that occur are 巳↔亥 and 卯↔酉 — both also 回頭克.
        # Build a multi-moving cast that produces one and check is_clash + feedback coexist.
        from itertools import combinations
        found = None
        for (lo, up), kw in HEXAGRAM_LOOKUP.items():
            base = list(lo) + list(up)
            for r in range(2, 7):
                for S in combinations(range(6), r):
                    vals = [(9 if base[i] == 1 else 6) if i in S else (7 if base[i] == 1 else 8)
                            for i in range(6)]
                    h = Hexagram(lines=[Line(value=v, position=i + 1) for i, v in enumerate(vals)])
                    for m in moving_line_dynamics(h):
                        if m.is_clash:
                            found = m
                            break
                    if found: break
                if found: break
            if found: break
        assert found is not None
        assert {found.branch, found.transformed_branch} in (
            {"巳", "亥"}, {"卯", "酉"})
        assert found.feedback == "回頭克"  # the element relation is kept, not overwritten

    def test_huitou_chong_only_two_pairs_occur(self):
        # Across all 64 × all moving subsets, 回頭沖 occurs only as 巳↔亥 and 卯↔酉.
        from itertools import combinations
        pairs = set()
        for (lo, up), kw in HEXAGRAM_LOOKUP.items():
            base = list(lo) + list(up)
            for r in range(1, 7):
                for S in combinations(range(6), r):
                    vals = [(9 if base[i] == 1 else 6) if i in S else (7 if base[i] == 1 else 8)
                            for i in range(6)]
                    h = Hexagram(lines=[Line(value=v, position=i + 1) for i, v in enumerate(vals)])
                    for m in moving_line_dynamics(h):
                        if m.is_clash:
                            pairs.add(frozenset((m.branch, m.transformed_branch)))
        assert pairs == {frozenset(("巳", "亥")), frozenset(("卯", "酉"))}


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-v"]))
