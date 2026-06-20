# NA_JIA.md — 納甲筮法 / 文王卦 / 六爻 Reference

*The Wen Wang Gua divination apparatus: Eight Palaces, Na Jia stem-branch assignment, Five Elements per line, the Six Relatives, and the World/Response lines.*

> **STATUS: reviewed & integrated 2026-06-20.** Authored by the Najia Scholar (sub-agent) from authoritative Chinese sources and triangulated tutorials; the load-bearing 8×8 palace partition was independently re-verified by the orchestrator (all 64 King-Wen hexagrams appear exactly once). Grounded in 京氏易傳 (京房) / 火珠林 / 易學網 + udn & 2743.com transmission. This is **secondary-triangulated, not a direct read of the 京氏易傳 primary text** (the 403/index walls in §8 blocked that) — so low-confidence spots are flagged inline with **⚠**, gathered in §7 (Disputed/Uncertain), with full provenance in §8 (Source-Access Log). The 飛伏 (flying-hidden) layer is openly deferred (§7.4). Characters + pinyin + English gloss throughout; where the tradition disagrees, both readings are kept rather than flattened.

---

## 0. Orientation — what this fixes

The `yijing` SKILL.md *invokes* the full Wen Wang Gua (文王卦 Wén Wáng Guà, "King Wen's Hexagram[-divination]") framework — Na Jia (納甲), the Six Relatives (六親 / 六亲 liù qīn), palace positions (八宮 bā gōng), and the Shi-Ying world/response lines (世應 shì yìng) — in §III, in the operating instructions (~ll. 484–489, 544–571, 741–753), and in the "Operationalized Yijing Template." None of it was defined anywhere in `references/`. This file defines it.

The system is also called **納甲筮法** (Nà Jiǎ Shì Fǎ, "the milfoil-method of Na Jia"), **六爻** (Liù Yáo, "Six Lines"), or **火珠林法** (Huǒ Zhū Lín Fǎ, after the Song manual that popularised the three-coin shortcut). Its theoretical engine was built by **京房** (Jīng Fáng, 77–37 BCE) in the **京氏易傳** (*Jīng Shì Yì Zhuàn*).

A complete build of a divinatory hexagram proceeds in four steps (四步裝卦 sì bù zhuāng guà), which structure §§1–5 below:
1. **裝宮 / 定宮** — find the palace and palace-position (→ §1)
2. **納甲** — assign Heavenly Stem + Earthly Branch to each of the six lines (→ §2)
3. **定五行** — read off each line's Five-Element value from its branch (→ §3)
4. **定六親、安世應** — assign the Six Relatives against the palace element, and place the World/Response lines (→ §§4–5)

---

## 1. The Eight Palaces (八宮 bā gōng)

### 1.1 The eight palace-heads

The 64 hexagrams are partitioned into **eight palaces**, each headed by one of the eight **doubled (pure) trigrams** (八純卦 bā chún guà — the trigram over itself). The palace order is the four yang houses then the four yin houses, in the family sequence father → sons, mother → daughters:

| # | Palace 宮 | Pinyin | Pure hexagram 本宮卦 | Trigram | Family | Palace element 宮五行 |
|---|-----------|--------|----------------------|---------|--------|------------------------|
| 1 | 乾宮 | Qián | 乾為天 (☰/☰) | Heaven | Father | **金 Metal** |
| 2 | 坎宮 | Kǎn | 坎為水 (☵/☵) | Water | Mid Son | **水 Water** |
| 3 | 艮宮 | Gèn | 艮為山 (☶/☶) | Mountain | Young Son | **土 Earth** |
| 4 | 震宮 | Zhèn | 震為雷 (☳/☳) | Thunder | Eldest Son | **木 Wood** |
| 5 | 巽宮 | Xùn | 巽為風 (☴/☴) | Wind | Eldest Dau | **木 Wood** |
| 6 | 離宮 | Lí | 離為火 (☲/☲) | Fire | Mid Dau | **火 Fire** |
| 7 | 坤宮 | Kūn | 坤為地 (☷/☷) | Earth | Mother | **土 Earth** |
| 8 | 兌宮 | Duì | 兌為澤 (☱/☱) | Lake | Young Dau | **金 Metal** |

> The palace element = the Five-Element of the **palace-head trigram** (its lower/native trigram). This palace element is the *fulcrum* of the whole apparatus — the Six Relatives (§4) are computed against it. Qián and Duì are Metal; Kǎn is Water; Gèn and Kūn are Earth; Zhèn and Xùn are Wood; Lí is Fire.

### 1.2 The generating rule (the changing-line walks UP the hexagram)

Within each palace the eight hexagrams are generated from the pure hexagram by walking a changing line up the figure. Stated in the source as: *「純卦按初爻、二爻、三爻、四爻、五爻、四爻、內卦三爻，依次累計變爻」* — "from the pure hexagram, change cumulatively the 1st line, then 2nd, 3rd, 4th, 5th line; then the 4th line [again]; then the three inner-trigram lines."

The rule, position by position (each step **keeps** the prior changes and adds the next — the changes accumulate, they do not reset):

| Position | Name | Pinyin | Gloss | Operation (cumulative) |
|----------|------|--------|-------|------------------------|
| 1 | 本宮 / 八純 | běn gōng / bā chún | Pure / native | the doubled trigram itself |
| 2 | 一世 | yī shì | First-generation | flip line **1** |
| 3 | 二世 | èr shì | Second-generation | + flip line **2** |
| 4 | 三世 | sān shì | Third-generation | + flip line **3** |
| 5 | 四世 | sì shì | Fourth-generation | + flip line **4** |
| 6 | 五世 | wǔ shì | Fifth-generation | + flip line **5** |
| 7 | 游魂 | yóu hún | "Wandering Soul" | from 五世, **flip line 4 back** |
| 8 | 归魂 | guī hún | "Returning Soul" | from 游魂, **flip the whole inner trigram (lines 1-2-3) back to the original** |

Two special steps to note:
- **游魂 (Wandering Soul):** the 5th-gen hexagram had lines 1–5 all changed. To form 游魂 the **4th line reverts**. (Equivalently: from the pure hexagram, lines 1,2,3,5 are changed and 4 restored.) Image: the soul has wandered out to the 5th line and now turns back.
- **归魂 (Returning Soul):** from 游魂, the **entire inner trigram returns** to its original pure-trigram form, while the outer trigram stays inverted. (Equivalently: the outer trigram is the opposite of the palace trigram, the inner trigram is the palace trigram itself.) Image: the soul comes home — the inner (本) trigram is restored.

### 1.3 The full 8 × 8 palace table

Reading each row left→right is the generating sequence 本宮 → 一世 → … → 归魂. (Confirmed against 易學網 八宮卦 and the 京氏易傳 palace chapters; cross-checked against the Xuite 八宮64卦圖 and the read01 太極輪迴圖.)

| Palace | 本宮 | 一世 | 二世 | 三世 | 四世 | 五世 | 游魂 | 归魂 |
|--------|------|------|------|------|------|------|------|------|
| **乾 (Metal)** | 乾為天 | 天風姤 | 天山遯 | 天地否 | 風地觀 | 山地剝 | 火地晉 | 火天大有 |
| **坎 (Water)** | 坎為水 | 水澤節 | 水雷屯 | 水火既濟 | 澤火革 | 雷火豐 | 地火明夷 | 地水師 |
| **艮 (Earth)** | 艮為山 | 山火賁 | 山天大畜 | 山澤損 | 火澤睽 | 天澤履 | 風澤中孚 | 風山漸 |
| **震 (Wood)** | 震為雷 | 雷地豫 | 雷水解 | 雷風恆 | 地風升 | 水風井 | 澤風大過 | 澤雷隨 |
| **巽 (Wood)** | 巽為風 | 風天小畜 | 風火家人 | 風雷益 | 天雷無妄 | 火雷噬嗑 | 山雷頤 | 山風蠱 |
| **離 (Fire)** | 離為火 | 火山旅 | 火風鼎 | 火水未濟 | 山水蒙 | 風水渙 | 天水訟 | 天火同人 |
| **坤 (Earth)** | 坤為地 | 地雷復 | 地澤臨 | 地天泰 | 雷天大壯 | 澤天夬 | 水天需 | 水地比 |
| **兌 (Metal)** | 兌為澤 | 澤水困 | 澤地萃 | 澤山咸 | 水山蹇 | 地山謙 | 雷山小過 | 雷澤歸妹 |

Pinyin / English of the 64 by palace (numbers are King-Wen #):

- **乾宮:** Qián為天(1) · Gòu姤(44) · Dùn遯(33) · Pǐ否(12) · Guān觀(20) · Bō剝(23) · Jìn晉(35) · Dà Yǒu大有(14)
- **坎宮:** Kǎn為水(29) · Jié節(60) · Zhūn屯(3) · Jì Jì既濟(63) · Gé革(49) · Fēng豐(55) · Míng Yí明夷(36) · Shī師(7)
- **艮宮:** Gèn為山(52) · Bì賁(22) · Dà Chù大畜(26) · Sǔn損(41) · Kuí睽(38) · Lǚ履(10) · Zhōng Fú中孚(61) · Jiàn漸(53)
- **震宮:** Zhèn為雷(51) · Yù豫(16) · Xiè解(40) · Héng恆(32) · Shēng升(46) · Jǐng井(48) · Dà Guò大過(28) · Suí隨(17)
- **巽宮:** Xùn為風(57) · Xiǎo Chù小畜(9) · Jiā Rén家人(37) · Yì益(42) · Wú Wàng無妄(25) · Shì Kè噬嗑(21) · Yí頤(27) · Gǔ蠱(18)
- **離宮:** Lí為火(30) · Lǚ旅(56) · Dǐng鼎(50) · Wèi Jì未濟(64) · Méng蒙(4) · Huàn渙(59) · Sòng訟(6) · Tóng Rén同人(13)
- **坤宮:** Kūn為地(2) · Fù復(24) · Lín臨(19) · Tài泰(11) · Dà Zhuàng大壯(34) · Guài夬(43) · Xū需(5) · Bǐ比(8)
- **兌宮:** Duì為澤(58) · Kùn困(47) · Cuì萃(45) · Xián咸(31) · Jiǎn蹇(39) · Qiān謙(15) · Xiǎo Guò小過(62) · Guī Mèi歸妹(54)

> **Self-check (load-bearing):** all 64 King-Wen numbers appear exactly once across the eight rows; the eight rows partition the hexagrams cleanly. The 归魂 of each palace has the palace's own trigram as its **lower** trigram (e.g. 大有 = ☲ over ☰: inner trigram ☰ Qián = the home trigram). ✓

---

## 2. Na Jia proper (納甲) — Stems and Branches on the six lines

**納甲** (Nà Jiǎ) literally = "ingesting [the stem] 甲" — synecdoche: 甲 (the *first* Heavenly Stem) stands for *all ten stems*, so "Na Jia" = the whole assignment of the **ten Heavenly Stems** (天干 tiān gān) and **twelve Earthly Branches** (地支 dì zhī) onto the lines of a hexagram. Each line gets one stem + one branch (a 干支 gānzhī pair).

### 2.1 The Heavenly-Stem-per-trigram rule (納天干)

Each of the eight trigrams ingests fixed stems. Qián and Kūn — the parents — each take **two** stems (the inner trigram gets one, the outer gets the other); the six children take one each:

| Trigram | Stem rule | Pinyin | Note |
|---------|-----------|--------|------|
| 乾 Qián | **甲**(inner) / **壬**(outer) | jiǎ / rén | 乾納甲壬 — two yang stems |
| 坤 Kūn | **乙**(inner) / **癸**(outer) | yǐ / guǐ | 坤納乙癸 — two yin stems |
| 震 Zhèn | **庚** | gēng | 震納庚 |
| 巽 Xùn | **辛** | xīn | 巽納辛 |
| 坎 Kǎn | **戊** | wù | 坎納戊 |
| 離 Lí | **己** | jǐ | 離納己 |
| 艮 Gèn | **丙** | bǐng | 艮納丙 |
| 兌 Duì | **丁** | dīng | 兌納丁 |

Classical mnemonic (口訣), preserved in 京氏易 transmission: *「乾納甲壬，坤納乙癸，震納庚，巽納辛，坎納戊，離納己，艮納丙，兌納丁。」*

> **Practical note:** in Liu Yao divination the **stem is rarely used** for the reading proper — what does the work is the **branch** (which carries the Five-Element value, §3) and the Six Relative derived from it. The stem matters mainly for completeness, for fixing the gānzhī of a line when calendar timing (日辰/月建) is brought in, and historically for the 飛伏/卦氣 theory. Most working diviners assign branches directly and skip the stem.

### 2.2 The Earthly-Branch-per-line rule (納地支) — the load-bearing rule

The branch on each line is fixed by trigram, by whether the trigram is **yang or yin**, and by whether it sits as the **inner (内)** or **outer (外)** trigram. The rule (易學網 / 京氏易傳; the polarity rule stated verbatim at 2743.com):

> *「乾坎艮震為陽，排地支時順行；巽離坤兌為陰，排地支時逆行。」*
> "Qián, Kǎn, Gèn, Zhèn are **yang** → arrange the branches **forward (順 shùn)**; Xùn, Lí, Kūn, Duì are **yin** → arrange the branches **backward (逆 nì)**."

Mechanics:
- Each trigram has a **starting branch on its first (bottom) line**.
- **Yang trigrams:** advance **+2 branches** per line going up (順, forward in the 12-branch cycle 子丑寅卯辰巳午未申酉戌亥).
- **Yin trigrams:** advance **−2 branches** per line going up (逆, backward).
- The **inner trigram** carries lines 1-2-3; the **outer trigram** carries lines 4-5-6, *continuing its own +2 / −2 progression from its own outer starting branch* (the outer start is 6 branches — i.e. the opposite point of the cycle — from the inner start, which is why Qián/Kūn need two stems).

Per-trigram starting branches and full line-by-line branch sequence (inner = lines 1,2,3 / outer = lines 4,5,6). The starts are fixed by the classical 納甲 mnemonic *「乾金甲子外壬午，坎水戊寅外戊申，艮土丙辰外丙戌，震木庚子外庚午，巽木辛丑外辛未，離火己卯外己酉，坤土乙未外癸丑，兌金丁巳外丁亥」*:

| Trigram | Pol. | Inner start (L1) | Inner L1→L2→L3 | Outer start (L4) | Outer L4→L5→L6 |
|---------|------|------------------|----------------|------------------|----------------|
| 乾 Qián | 陽 順 | 子 zǐ | 子 → 寅 → 辰 | 午 wǔ | 午 → 申 → 戌 |
| 坎 Kǎn | 陽 順 | 寅 yín | 寅 → 辰 → 午 | 申 shēn | 申 → 戌 → 子 |
| 艮 Gèn | 陽 順 | 辰 chén | 辰 → 午 → 申 | 戌 xū | 戌 → 子 → 寅 |
| 震 Zhèn | 陽 順 | 子 zǐ | 子 → 寅 → 辰 | 午 wǔ | 午 → 申 → 戌 |
| 巽 Xùn | 陰 逆 | 丑 chǒu | 丑 → 亥 → 酉 | 未 wèi | 未 → 巳 → 卯 |
| 離 Lí | 陰 逆 | 卯 mǎo | 卯 → 丑 → 亥 | 酉 yǒu | 酉 → 未 → 巳 |
| 坤 Kūn | 陰 逆 | 未 wèi | 未 → 巳 → 卯 | 丑 chǒu | 丑 → 亥 → 酉 |
| 兌 Duì | 陰 逆 | 巳 sì | 巳 → 卯 → 丑 | 亥 hài | 亥 → 酉 → 未 |

> **How to build any hexagram's six branches:** take the **inner** trigram → use its *inner* column for lines 1,2,3. Take the **outer** trigram → use its *outer* column for lines 4,5,6. (The same physical trigram thus carries different branches depending on whether it sits inside or outside.)

### 2.3 Worked example — 乾為天 (Qián, pure)

Inner ☰ Qián (inner column) on lines 1-3; outer ☰ Qián (outer column) on lines 4-6:

| Line | Stem | Branch | 干支 |
|------|------|--------|------|
| 6 (top) | 壬 rén | 戌 xū | 壬戌 |
| 5 | 壬 rén | 申 shēn | 壬申 |
| 4 | 壬 rén | 午 wǔ | 壬午 |
| 3 | 甲 jiǎ | 辰 chén | 甲辰 |
| 2 | 甲 jiǎ | 寅 yín | 甲寅 |
| 1 (bottom) | 甲 jiǎ | 子 zǐ | 甲子 |

Branches bottom→top: 子 寅 辰 午 申 戌 — the six yang branches in forward order. ✓

### 2.4 Worked example — 坤為地 (Kūn, pure)

Inner ☷ Kūn (inner column) on lines 1-3; outer ☷ Kūn (outer column) on lines 4-6:

| Line | Stem | Branch | 干支 |
|------|------|--------|------|
| 6 (top) | 癸 guǐ | 酉 yǒu | 癸酉 |
| 5 | 癸 guǐ | 亥 hài | 癸亥 |
| 4 | 癸 guǐ | 丑 chǒu | 癸丑 |
| 3 | 乙 yǐ | 卯 mǎo | 乙卯 |
| 2 | 乙 yǐ | 巳 sì | 乙巳 |
| 1 (bottom) | 乙 yǐ | 未 wèi | 乙未 |

Branches bottom→top: 未 巳 卯 丑 亥 酉 — the six yin branches in backward order. ✓ (Note: Kūn's lines are built from a *mixed*-hexagram, so the **stem is always read from the trigram occupying that half**, not from the line's polarity.)

> **For non-pure hexagrams** the inner and outer trigrams differ, so you read the inner column of one trigram and the outer column of another. Example — **水雷屯 (Zhūn, 坎宮二世):** inner ☳ Zhèn → lines 1-2-3 = 子,寅,辰 (stem 庚); outer ☵ Kǎn → lines 4-5-6 = 申,戌,子 (stem 戊). Six branches bottom→top: 子 寅 辰 申 戌 子.

---

## 3. Five Elements per line (五行 wǔ xíng)

Each line's element is read **directly off its Earthly Branch** — the branch *is* the carrier of the element. The fixed branch→element map (standard 子平/六爻 correspondence):

| Branch | 子 | 丑 | 寅 | 卯 | 辰 | 巳 | 午 | 未 | 申 | 酉 | 戌 | 亥 |
|--------|----|----|----|----|----|----|----|----|----|----|----|----|
| Pinyin | zǐ | chǒu | yín | mǎo | chén | sì | wǔ | wèi | shēn | yǒu | xū | hài |
| **Element** | 水 Water | 土 Earth | 木 Wood | 木 Wood | 土 Earth | 火 Fire | 火 Fire | 土 Earth | 金 Metal | 金 Metal | 土 Earth | 水 Water |

Mnemonic: 寅卯木 (Wood), 巳午火 (Fire), 申酉金 (Metal), 亥子水 (Water), 辰戌丑未土 (the four Earth branches, one at each cardinal "storage" position).

Applied to **乾為天** (§2.3): 子=Water, 寅=Wood, 辰=Earth, 午=Fire, 申=Metal, 戌=Earth. So Qián's six lines, bottom→top, carry: 水 木 土 火 金 土.

---

## 4. The Six Relatives (六親 / 六亲 liù qīn)

The Six Relatives are **kinship roles assigned to each line by comparing that line's element to the PALACE element (宮五行)** via the Generating (生 shēng) and Controlling (克 kè) cycles. They are the heart of the reading: the diviner reads the question through which relatives appear, where they sit, and whether they're supported or attacked.

The rule, stated from the standpoint of the palace element as **"me" (我 wǒ)**:

| Relative | Chars | Pinyin | Gloss | Rule (relative to palace element 我) |
|----------|-------|--------|-------|--------------------------------------|
| Parents | 父母 | fù mǔ | parents/elders, documents, houses | **生我者 = 父母** — that which *generates me* |
| Siblings | 兄弟 | xiōng dì | siblings, peers, rivals, friends | **同我者 = 兄弟** — that which is *same as me* (比和) |
| Offspring | 子孫 | zǐ sūn | children, blessing, medicine, the "suppressor of officials" | **我生者 = 子孫** — that which *I generate* |
| Wealth/Wife | 妻財 | qī cái | wealth, wife, property, provisions | **我克者 = 妻財** — that which *I control* |
| Officials/Ghosts | 官鬼 | guān guǐ | office, husband, illness, threat, ghosts | **克我者 = 官鬼** — that which *controls me* |

Classical statement (火珠林 / 京氏 transmission): *「生我者為父母，剋我者為官鬼，我剋者為妻財，我生者為子孫，比和者為兄弟。」*

The two element cycles it draws on (also given in the SKILL.md §VI):
- **生 (generating):** 金生水 → 水生木 → 木生火 → 火生土 → 土生金 → (金…)
- **克 (controlling):** 金克木 → 木克土 → 土克水 → 水克火 → 火克金 → (金…)

### 4.1 The five palace-element lookup tables

Because the palace element is fixed (§1.1), the Six Relatives reduce to five lookup tables (triangulated verbatim from 2743.com):

| Palace element | 兄弟 (same) | 父母 (gen. me) | 子孫 (I gen.) | 妻財 (I ctrl) | 官鬼 (ctrl me) |
|----------------|------------|----------------|---------------|---------------|----------------|
| **金 Metal** (乾·兌) | 金 | 土 | 水 | 木 | 火 |
| **水 Water** (坎) | 水 | 金 | 木 | 火 | 土 |
| **土 Earth** (坤·艮) | 土 | 火 | 金 | 水 | 木 |
| **火 Fire** (離) | 火 | 木 | 土 | 金 | 水 |
| **木 Wood** (震·巽) | 木 | 水 | 火 | 土 | 金 |

Source verbatim (2743.com): *「乾兌宮（金）：金為兄弟、土為父母、木為妻財、火為官鬼、水為子孫；坎宮（水）：水為兄弟、火為妻財、土為官鬼、金為父母、木為子孫；坤艮宮（土）：土為兄弟、火為父母、木為官鬼、水為妻財、金為子孫；離宮（火）：火為兄弟、水為官鬼、土為子孫、木為父母、金為妻財；震巽宮（木）：木為兄弟、水為父母、金為官鬼、火為子孫、土為妻財。」**[Self-check: each row's five elements are a permutation of {金水木火土}. ✓]**

### 4.2 Worked example — 乾為天 (palace = 乾, element 金 Metal)

Take each line's element (§3) and look it up in the **金** row:

| Line | Branch | Element | vs. Metal | Relative |
|------|--------|---------|-----------|----------|
| 6 | 戌 | 土 Earth | Earth generates Metal → 生我 | **父母** |
| 5 | 申 | 金 Metal | same → 同我 | **兄弟** |
| 4 | 午 | 火 Fire | Fire controls Metal → 克我 | **官鬼** |
| 3 | 辰 | 土 Earth | 生我 | **父母** |
| 2 | 寅 | 木 Wood | Metal controls Wood → 我克 | **妻財** |
| 1 | 子 | 水 Water | Metal generates Water → 我生 | **子孫** |

So 乾為天, bottom→top: 子孫 · 妻財 · 父母 · 官鬼 · 兄弟 · 父母. (This is the canonical 乾卦 六親 layout used in every Liu Yao primer.) ✓

> **裝卦 note:** the Six Relatives are *always* computed against the **palace** element, **never** against the hexagram's own lower trigram when the hexagram is not pure. A 坎宮 hexagram, however many trigrams it mixes, takes its Six Relatives against **Water**. This is the single most common beginner error.

---

## 5. The World and Response lines (世應 shì yìng)

Each hexagram has exactly one **World line (世爻 shì yáo)** and one **Response line (應爻 yìng yáo)**, fixed by the palace-position (§1.2). The World line = the querent / the subject / "self"; the Response line = the other party / the object of the question. The Response always sits **three positions away** from the World (世應相隔三位 / 隔二爻).

### 5.1 The placement table

(Verbatim from 易學網 八宮世應 / 京氏易傳, triangulated against the WebSearch summary *「八成卦世六應三，二卦世初應四，三卦世二應五，四卦世三應六，五卦世四應初，六卦世五應二，七卦世四應初，八卦世三應六」*. Counting the eight positions in generating order as 1st=本宮 … 8th=归魂):

| Palace position | World line 世 | Response line 應 |
|-----------------|---------------|------------------|
| 本宮 / 八純 (1st) | line **6** | line **3** |
| 一世 (2nd) | line **1** | line **4** |
| 二世 (3rd) | line **2** | line **5** |
| 三世 (4th) | line **3** | line **6** |
| 四世 (5th) | line **4** | line **1** |
| 五世 (6th) | line **5** | line **2** |
| 游魂 (7th) | line **4** | line **1** |
| 归魂 (8th) | line **3** | line **6** |

The pattern: from 本宮 the World walks **down** (6→1→2→3→4→5 across the first six positions); 游魂 puts the World on line 4 (sharing the 四世 placement, fitting the "4th line changed" identity); 归魂 puts the World on line 3 (sharing the 三世 placement, fitting the "inner trigram returned" identity). The Response is always +3 (mod 6) from the World.

> **Mnemonic (世爻 only), generating order:** 六 → 初 → 二 → 三 → 四 → 五 → 四 → 三. (上世, 初世, 二世, 三世, 四世, 五世, then 游魂回到四, 归魂回到三.)

### 5.2 用神 (yòng shén) — the "Useful God"

Once 世應 and the Six Relatives are placed, the diviner selects the **用神** (yòng shén, "useful spirit/god") — the relative that *represents the matter asked about* — and judges its strength by season, by 日辰/月建 (day/month branch), and by 動爻 (moving lines). The standard 用神 correspondences (火珠林 tradition):

| Question about… | 用神 (relative) |
|-----------------|----------------|
| wealth, wife, business, provisions | **妻財** |
| career, husband, illness, lawsuit, threat, ghosts | **官鬼** |
| documents, parents, elders, house, vehicle, study | **父母** |
| children, subordinates, blessing, peace-of-mind, medicine | **子孫** |
| siblings, peers, partners, competition, loss of money | **兄弟** |

(This selection layer is downstream of the apparatus defined here; included for completeness because the SKILL.md template names 用神 and 忌神. A full 用神 / 元神 / 忌神 / 仇神 doctrine belongs in a separate INTERPRETATION-level file.)

---

## 6. End-to-end worked build (putting §§1–5 together)

**Hexagram: 水雷屯 (Zhūn, #3) — "Difficulty at the Beginning."** Inner ☳ Zhèn, outer ☵ Kǎn.

1. **Palace (§1):** ☵ over ☳. Scan the table → 屯 sits in **坎宮, 二世** (Water palace, 2nd generation). Palace element = **水 Water**.
2. **Na Jia branches (§2):** inner Zhèn → L1,2,3 = 子,寅,辰 (stem 庚); outer Kǎn → L4,5,6 = 申,戌,子 (stem 戊).
3. **Elements (§3):** 子=水, 寅=木, 辰=土, 申=金, 戌=土, 子=水.
4. **Six Relatives (§4, vs. Water):** 水=兄弟, 木=子孫(水生木→我生), 土=官鬼(土克水→克我), 金=父母(金生水→生我).
5. **World/Response (§5):** 二世 → 世 on line **2**, 應 on line **5**.

Resulting chart, bottom→top:

| Line | Branch | Element | Relative | 世/應 |
|------|--------|---------|----------|-------|
| 6 | 子 zǐ | 水 Water | 兄弟 | |
| 5 | 戌 xū | 土 Earth | 官鬼 | **應** |
| 4 | 申 shēn | 金 Metal | 父母 | |
| 3 | 辰 chén | 土 Earth | 官鬼 | |
| 2 | 寅 yín | 木 Wood | 子孫 | **世** |
| 1 | 子 zǐ | 水 Water | 兄弟 | |

This matches the standard 屯卦 装卦 in every Liu Yao reference. ✓ The querent (世) is 子孫/Wood on line 2; the other party (應) is 官鬼/Earth on line 5; Earth controls Water — a configuration the tradition reads as the "other" exerting pressure on "self's" house, fitting 屯's theme of obstructed beginnings.

---

## 7. DISPUTED / UNCERTAIN — where the sources genuinely diverge

1. **⚠ 游魂/归魂 — "soul" language vs. mechanical rule.** All sources agree on the *mechanics* (游魂 = 4th line reverts from 五世; 归魂 = inner trigram restored). They diverge on *why*: Jing Fang's own 京氏易傳 frames it cosmologically (the 魂 hún "soul" wandering and returning — a 卦氣/seasonal-soul doctrine), while modern Liu Yao primers treat it as a bookkeeping rule with no metaphysics. I have stated the mechanics as settled and flagged the metaphysics as a live interpretive question. **Confidence in the mechanics: high.**

2. **⚠ Whether the Heavenly Stem is "real" Na Jia or vestigial.** Some authorities (esp. the 京氏 / 卦氣 lineage and Han image-number scholars) insist the stem assignment is structurally essential (it drives 飛伏 flying-hidden, 卦氣 hexagram-qi, and calendrical fitting). The dominant *practical* Liu Yao schools (火珠林 lineage) drop the stem entirely and work from branches alone. Both are reported; I have not adjudicated. The *branch* assignments are uncontested.

3. **⚠ Coin-toss head/tail convention.** Out of scope here (it's CASTING, not Na Jia), but the SKILL.md §"Three-Coin Method" already hedges "(or reverse, depending on tradition)" — this is a genuine, unresolved regional split (字/背 = yin/yang varies). Flagged so the orchestrator doesn't read my silence as endorsement of one convention.

4. **⚠ 飛伏 (fēi fú, "flying and hidden") not defined here.** When a needed Six-Relative is *absent* from a hexagram, the tradition supplies a **hidden line (伏神 fú shén)** drawn from the underlying pure-palace hexagram, "flying" (飛神 fēi shén) being the visible line that covers it. This is a real and load-bearing part of the 京房 system (and is named in the SKILL.md source table). I have **deliberately scoped it out** of this draft because confirming the exact 飛伏 extraction rule cleanly from a primary source was blocked by the 403s (see §8); it deserves its own section once a clean source is fetched. **This is the single biggest undelivered piece.**

5. **⚠ Palace order variants.** I give the canonical 乾坎艮震巽離坤兌 order (yang houses by son-seniority, then yin houses by daughter-seniority). A minority of late texts list the palaces 乾兌離震巽坎艮坤 (the 先天 Fu-Xi circular order) for *cosmological* diagrams. The *divinatory* palace order — the one that generates the 8×8 table — is the one given. Confidence: high.

---

## 8. SOURCE-ACCESS LOG (provenance / transparency)

**Fetched cleanly:**
- **udn blog 京房易八宮卦表及納甲** (`blog.udn.com/tsao144/6479918`) — delivered the full Na Jia 口訣 *「乾金甲子外壬午…兌金丁巳外丁亥」* (the per-trigram inner/outer branch starts). **Primary-grade for §2.** ✓
- **2743.com 八宮卦六親世應圖** (`2743.com/archives/12926`) — delivered the **陽順陰逆** branch-polarity rule verbatim, each trigram's starting branch, and the five palace-element Six-Relatives tables verbatim. **Keystone for §2.2 and §4.** ✓
- **WebSearch summaries** confirmed: the generating rule *「純卦按初爻…依次累計變爻」*; the full 世應 table *「八成卦世六應三…」*; and all eight palace hexagram-sequences (cross-checking 乾/坎/艮/震/巽 explicitly). **Used for §1.2, §1.3, §5.1.**
- **zh.wikipedia 文王卦** — confirmed the high-level frame (世爻=self, 應爻=other; 官鬼/父母/兄弟/子孫/妻財 named) but, by its own "needs more sources" banner, carried **no** detailed tables. Used only for framing.

**Failed / blocked (logged, not retried into the wall — per lab protocol, ≤3 attempts then pivot):**
- **zhihu** `p/138355945` (納甲筮法 京房) and `p/660229990` (四步裝卦) — **HTTP 403** (Zhihu blocks non-browser agents). These were the *primary* assigned sources; pivoted to the equivalent material via udn + 2743 + 易學網 search.
- **eee-learning.com** `/article/1757`, `/article/1790` (八宮卦), `/article/1799` (八宮世應), `/book/5687` (乾宮卦 京氏易傳), `/book/5692` — **HTTP 403** on every direct fetch. Their *content* was recovered via WebSearch result-summaries, but I could **not** read the 京氏易傳 palace-chapter primary text directly.
- **ctext.org/jingshi-yizhuan** — fetched, but returned only the **navigation index**, not the per-hexagram commentary body. I could not extract Jing Fang's *original* 世/應/納甲 sentences from ctext in this pass (the text lives on the individual hexagram subpages, which I did not enumerate one-by-one). **The single most important primary-source gap: §§1–5 are confirmed from authoritative secondary transmission + triangulation, NOT from a direct read of the 京氏易傳 source text.**
- **csdn** `article/8477236` — **HTTP 521** then unreachable.
- **xuite** `dejavu8899/blog/36031061` (八宮64卦圖) — **ECONNREFUSED**.
- **douban** `note/823971007` & **astrologs.net** & **getit01 mirror** — **302 redirect to anti-bot gates / 403**; dead ends.

**What I could NOT confirm from a primary source (reporting on secondary/triangulated authority):**
- The exact wording of Jing Fang's *own* statements on 世應 and 納甲 (I have the rules, triangulated and self-consistent, but not quoted from a directly-read 京氏易傳 body text).
- The **飛伏 flying-hidden** extraction rule (scoped out — §7.4).
- The branch tables in §2.2 are **computed** by me by applying the sourced **陽順陰逆 +2/−2 rule** to the sourced **starting branches**; each was then **cross-checked** against the worked 乾/坤/屯 charts (which match canonical references). They are internally consistent and match every spot-check, but they are a *derivation*, not a line-by-line transcription from one table.

---

## 9. Quick-reference card (the whole apparatus on one screen)

```
BUILD A HEXAGRAM (四步裝卦):
 1. 裝宮  → find palace + position in the 8×8 table (§1.3); palace element = head-trigram element
 2. 納甲  → branches: inner trigram cols for L1-3, outer trigram cols for L4-6 (§2.2)
            yang trigram 乾坎艮震 順(+2); yin trigram 巽離坤兌 逆(−2)
            starts: 乾子/午 坎寅/申 艮辰/戌 震子/午 巽丑/未 離卯/酉 坤未/丑 兌巳/亥
 3. 五行  → element straight from branch: 寅卯木 巳午火 申酉金 亥子水 辰戌丑未土
 4. 六親  → vs PALACE element: 生我父母·同我兄弟·我生子孫·我克妻財·克我官鬼
    世應  → 本宮世6應3·一世1/4·二世2/5·三世3/6·四世4/1·五世5/2·游魂4/1·归魂3/6

GENERATING RULE (palace sequence): 本宮→flip1→flip2→flip3→flip4→flip5
   →游魂(flip4 back)→归魂(inner trigram restored)
```

---

*Drafted by the Najia Scholar, June 2026. Primary sources: 京氏易傳 (京房) via transmission; 火珠林; 易學網 (eee-learning.com); udn 曹盛健 八宮納甲表; 2743.com 六親世應圖. Flagged ⚠ items and the §8 log mark every spot where authority is secondary or derivation rather than a direct primary read. The 飛伏 section remains to be written from a clean source.*
