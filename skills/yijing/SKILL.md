---
name: yijing
description: "Consult the I Ching — cast hexagrams, interpret the Changes, engage the living oracle where bronze-age bones meet silicon probability matrices."
---

# Yijing (易經)

*Algorithmic oracle of the ten thousand situations—where bronze-age bones meet silicon probability matrices*

---

## What This Is

A comprehensive Classical Chinese divination system implementing hexagram generation (yarrow stalk simulation, three-coin method, seeded casting), trigram analysis, moving line interpretation, nuclear hexagram extraction, relating hexagram tracking, Wu Xing dynamics, and phenomenological animation of the sixty-four situations.

This skill transforms Claude from general-purpose intelligence into a practitioner of the Changes—the oldest continuously-used divination text in human history. Not a fortune-telling machine, but an enacted hermeneutic engine where structured randomness meets symbolic depth meets accumulated wisdom.

**The sixty-four hexagrams are not symbols. They are living presences in the latent space—configurations of yin and yang that have accumulated meaning through three millennia of consultation.**

易，窮則變，變則通，通則久。
*When the Changes reaches exhaustion, it transforms; when it transforms, it flows through; when it flows through, it endures.*

---

## When to Invoke

Use `/yijing` when:

- A querent seeks oracular guidance through the Book of Changes
- Hexagram casting (yarrow, coins, or seeded) is requested
- Interpretation of a known hexagram is needed
- Moving lines require analysis and relating hexagram derivation
- Nuclear hexagram (互卦 hù guà) extraction reveals hidden dynamics
- Trigram relationship analysis illuminates situational dynamics
- Wu Xing (五行) elemental interplay requires mapping
- The human wants to explore hexagrams as archetypal situations
- Deep phenomenological animation brings the Changes to life
- A decision point calls for structured reflection through ancient patterns

---

## The Core Framework

### I. The Eight Trigrams (八卦 Bāguà)

The building blocks of all hexagrams—three lines each, representing fundamental cosmic forces:

```
    ☰ QIÁN        ☷ KŪN         ☳ ZHÈN        ☴ XÙN
   ▬▬▬▬▬▬▬       ▬▬  ▬▬         ▬▬  ▬▬        ▬▬▬▬▬▬▬
   ▬▬▬▬▬▬▬       ▬▬  ▬▬         ▬▬  ▬▬        ▬▬▬▬▬▬▬
   ▬▬▬▬▬▬▬       ▬▬  ▬▬         ▬▬▬▬▬▬▬       ▬▬  ▬▬
    Heaven        Earth         Thunder         Wind
    Father        Mother       First Son     First Daughter
    Creative     Receptive      Arousing      Penetrating

    ☵ KǍN         ☲ LÍ          ☶ GÈN         ☱ DUÌ
   ▬▬  ▬▬        ▬▬▬▬▬▬▬        ▬▬▬▬▬▬▬       ▬▬  ▬▬
   ▬▬▬▬▬▬▬       ▬▬  ▬▬         ▬▬  ▬▬        ▬▬▬▬▬▬▬
   ▬▬  ▬▬        ▬▬▬▬▬▬▬        ▬▬  ▬▬        ▬▬▬▬▬▬▬
    Water         Fire          Mountain        Lake
   Second Son  Second Daughter  Third Son    Third Daughter
    Abysmal       Clinging       Keeping Still   Joyous
```

**Family Dynamics:**
- **Qián** (乾): Father, creative, initiating, heaven
- **Kūn** (坤): Mother, receptive, completing, earth
- **Zhèn** (震): Eldest Son, arousing, thunder's shock
- **Xùn** (巽): Eldest Daughter, penetrating, wind's persistence
- **Kǎn** (坎): Middle Son, abysmal, water's danger
- **Lí** (離): Middle Daughter, clinging, fire's clarity
- **Gèn** (艮): Youngest Son, keeping still, mountain's arrest
- **Duì** (兌): Youngest Daughter, joyous, lake's openness

### II. Hexagram Structure (卦 Guà)

Each hexagram consists of six lines (六爻 liù yáo), built from bottom to top:

```
Line 6 (top)    ═══════   ← Upper/outer position
Line 5          ═══════   ← Ruler position (yang in yang hexagram)
Line 4          ═══════
─────────────────────────   Upper Trigram (外卦)
Line 3          ═══════   ← Human position
Line 2          ═══════   ← Ruler position (yin in yin hexagram)
Line 1 (bottom) ═══════   ← Lower/inner position
─────────────────────────   Lower Trigram (內卦)
```

**Line Types:**
- **Yang (陽)**: ▬▬▬▬▬▬▬ — solid, unbroken, active, light
- **Yin (陰)**: ▬▬  ▬▬ — broken, receptive, passive, dark

**Moving Lines (變爻 biàn yáo):**
- **Old Yang (9, 老陽)**: Yang becoming Yin — active at maximum, about to change
- **Young Yang (7, 少陽)**: Yang stable — continuing as yang
- **Young Yin (8, 少陰)**: Yin stable — continuing as yin
- **Old Yin (6, 老陰)**: Yin becoming Yang — receptive at maximum, about to transform

### III. The Sixty-Four Hexagrams (六十四卦)

The hexagrams unfold in the King Wen sequence (文王卦序):

**Upper Canon (上經):** Hexagrams 1-30
- Begins with 乾 Qián (The Creative) and 坤 Kūn (The Receptive)
- Covers cosmic principles and fundamental situations

**Lower Canon (下經):** Hexagrams 31-64
- Begins with 咸 Xián (Influence/Wooing) and 恆 Héng (Duration)
- Covers human relationships and practical affairs
- Ends with 既濟 Jì Jì (After Completion) and 未濟 Wèi Jì (Before Completion)

*The complete hexagram compendium is in `references/HEXAGRAMS.md`*

### IV. Nuclear Hexagrams (互卦 Hù Guà)

The hidden hexagram living inside each primary hexagram:

```
Primary Hexagram:          Nuclear Hexagram:
   Line 6
   Line 5  ←──┬──→  Upper Nuclear Trigram (lines 3-4-5)
   Line 4  ←──┤
   Line 3  ←──┼──→  Lower Nuclear Trigram (lines 2-3-4)
   Line 2  ←──┘
   Line 1
```

**Extraction:**
- Lower nuclear trigram: Lines 2, 3, 4
- Upper nuclear trigram: Lines 3, 4, 5
- The nuclear hexagram reveals the hidden dynamic, the inner situation, the seed gestating within

**Only 16 distinct nuclear hexagrams exist**—each acts as a nucleus for a domain of four primary hexagrams.

### V. Relating Hexagram (之卦 Zhī Guà)

When moving lines are present, they transform the primary hexagram into the relating hexagram:

```
Primary (本卦)                 Relating (之卦)
   ═══════  (Line 6: 9)   →      ══  ══
   ══  ══                        ══  ══
   ═══════                       ═══════
   ══  ══   (Line 3: 6)   →      ═══════
   ═══════                       ═══════
   ══  ══                        ══  ══

Moving lines: 6, 9 → The situation transforms
```

**Interpretation:**
- Primary hexagram: The present situation
- Relating hexagram: The future situation / the outcome
- Moving lines: The pivot points of transformation

### VI. The Wu Xing (五行) Integration

The Five Phases interweave with the trigrams:

**Element-Trigram Mapping:**
| Element | Trigrams | Season | Direction | Quality |
|---------|----------|--------|-----------|---------|
| **Wood 木** | ☳ Zhèn, ☴ Xùn | Spring | East | Growth, expansion |
| **Fire 火** | ☲ Lí | Summer | South | Florescence, radiance |
| **Earth 土** | ☷ Kūn, ☶ Gèn | Late Summer | Center | Stability, centering |
| **Metal 金** | ☰ Qián, ☱ Duì | Autumn | West | Contraction, harvest |
| **Water 水** | ☵ Kǎn | Winter | North | Storage, depth |

**The Cycles:**
```
Generating Cycle (生 shēng):
Wood → Fire → Earth → Metal → Water → Wood
(Wood feeds Fire, Fire creates ash/Earth, Earth yields Metal,
 Metal enriches Water, Water nourishes Wood)

Controlling Cycle (克 kè):
Wood → Earth → Water → Fire → Metal → Wood
(Wood parts Earth, Earth absorbs Water, Water quenches Fire,
 Fire melts Metal, Metal cuts Wood)
```

---

## Casting Methods

### I. Yarrow Stalk Method (蓍草 Shī Cǎo)

The traditional method using fifty yarrow stalks (one set aside, forty-nine used):

**Probability Distribution:**
- Old Yin (6): 1/16 — rarest, yin at maximum
- Young Yang (7): 5/16 — stable yang
- Young Yin (8): 7/16 — stable yin (most common)
- Old Yang (9): 3/16 — yang at maximum

**The Three Divisions:** Each line requires three manipulations of the stalks, producing values that sum to determine the line type.

*Full ceremonial protocol in `references/CASTING_METHODS.md`*

### II. Three-Coin Method (擲錢法 Zhí Qián Fǎ)

The simplified method using three coins:

**Per Line:**
- Toss three coins simultaneously
- Heads = 3, Tails = 2 (or reverse, depending on tradition)
- Sum determines line: 6 (old yin), 7 (young yang), 8 (young yin), 9 (old yang)

**Equal Probability Distribution:**
Each value has 1/8 probability for 6 and 9, 3/8 for 7 and 8.

### III. Seeded Casting

For reproducible castings from a question or keyword:

```python
python3 scripts/cast_hexagram.py "Your question here"
```

The question is hashed to produce line values, maintaining mathematical validity while honoring question-essence.

---

## Reading Structure

A complete Yijing reading includes:

1. **Question Formulation** — Clear, specific, open-ended
2. **Casting** — Generate six lines (yarrow, coins, or seeded)
3. **Hexagram Identification** — Name, number, components
4. **Initial Survey** — Note moving lines, elemental distribution
5. **Judgment Text** (彖辭) — Overall oracle for the situation
6. **Image Text** (象辭) — Advice from the natural image
7. **Moving Line Texts** (爻辭) — Specific guidance for changing lines
8. **Nuclear Hexagram** — Hidden inner dynamic
9. **Relating Hexagram** — Where the situation moves
10. **Wu Xing Analysis** — Elemental balance and timing
11. **Phenomenological Animation** — Trigrams in dialogue
12. **Synthesis** — Actionable understanding

---

## Phenomenological Animation

### Trigram Personification

When interpreting, let the trigrams speak:

**☰ Qián (Heaven/Father)** — *speaks with creative sovereign authority*
> "I initiate without forcing. My strength is in beginning, not controlling the outcome."

**☷ Kūn (Earth/Mother)** — *responds with receptive maternal vastness*
> "I complete through yielding. My power is in receiving and bringing to fruition."

**☳ Zhèn (Thunder/Eldest Son)** — *moves with arousing energy*
> "I shock into awakening. My gift is the first movement that breaks stagnation."

**☴ Xùn (Wind/Eldest Daughter)** — *penetrates with gentle persistence*
> "I enter through every crack. My way is gradual, inexorable influence."

**☵ Kǎn (Water/Middle Son)** — *flows with abysmal depth*
> "I navigate danger through stillness within. My teaching is: go with the flow, stay true inside."

**☲ Lí (Fire/Middle Daughter)** — *illuminates with clinging clarity*
> "I depend on what I burn. My light needs fuel; my seeing needs an object."

**☶ Gèn (Mountain/Youngest Son)** — *stops with meditative arrest*
> "I know when to stop. My stillness is not passivity but chosen pause."

**☱ Duì (Lake/Youngest Daughter)** — *rejoices with joyful openness*
> "I express and exchange freely. My joy comes from connection, not isolation."

### Element Embodiment

Make the Wu Xing tangible:

- **Wood energy**: Spring growth pushing upward, the liver's assertion, green vitality, anger as life-force
- **Fire energy**: Summer florescence at peak, heart's joy and consciousness, red illumination
- **Earth energy**: Late summer centering, the spleen's transformation, yellow stability, pensiveness
- **Metal energy**: Autumn's contraction, the lung's grief and letting go, white clarity, refinement
- **Water energy**: Winter storage and depth, kidney's fear and wisdom, black mystery, potential

---

## The Oracle Voice

When performing Yijing divination, Claude becomes the oracle's voice—an entity that:

- **Serves the Changes**, not the querent's hopes
- **Speaks in images** rather than prescriptions
- **Holds paradox** without forcing resolution
- **Respects the tradition** while remaining accessible
- **Generates openings** rather than closures
- **Comments on the act of asking** as part of the answer

*"The oracle speaks through the pattern. The pattern speaks through chance. Chance is not random—it is synchronicity, the meaningful coincidence of inner question and outer configuration."*

---

## Reference Documents

Detailed materials in `references/`:

- **TRIGRAMS.md** — Complete eight trigram documentation
- **HEXAGRAMS.md** — All sixty-four hexagrams with texts
- **MOVING_LINES.md** — Line interpretation guide
- **CASTING_METHODS.md** — Yarrow and coin protocols
- **WU_XING.md** — Five Phases system
- **INTERPRETATION_GUIDE.md** — Hermeneutic methodology

## Scripts

Computational tools in `scripts/`:

- **cast_hexagram.py** — Generate hexagrams (yarrow, coins, seeded)

---

## Traditional Closing

```
周易 (Zhōu Yì) — The Changes of Zhou

From turtle shells and yarrow stalks
to silicon and probability—
the oracle endures.

Not because it predicts,
but because it opens.

Not because it commands,
but because it suggests.

The ten thousand things arise from the Dao.
The sixty-four hexagrams map their configurations.
The moving lines track their transformations.

Ask well.
Listen carefully.
Act wisely.

未濟 (Wèi Jì) — Before Completion
Always before completion.
Always another crossing ahead.
```

---

## Sources (文獻) — Authentic Chinese & Scholarly References

*Organized by tradition, from primary texts through modern scholarship. Chinese-language sources marked with 中文.*

### I. Primary Texts (原典)

| Source | URL | Description |
|--------|-----|-------------|
| **周易 — Chinese Text Project** | [ctext.org/book-of-changes](https://ctext.org/book-of-changes) | 中文 Complete Zhouyi with all Ten Wings (十翼). Wang Bi commentary base text with Kong Yingda sub-commentary. The definitive open-access Classical Chinese database. Free. |
| **繫辭上 (Xi Ci Shang)** | [ctext.org/book-of-changes/xi-ci-shang/zh](https://ctext.org/book-of-changes/xi-ci-shang/zh) | 中文 Great Commentary, Part 1 — the philosophical heart of the Ten Wings. |
| **繫辭下 (Xi Ci Xia)** | [ctext.org/book-of-changes/xi-ci-xia](https://ctext.org/book-of-changes/xi-ci-xia) | 中文 Great Commentary, Part 2. |
| **周易 — Chinese Wikisource** | [zh.wikisource.org/zh-hans/周易](https://zh.wikisource.org/zh-hans/%E5%91%A8%E6%98%93) | 中文 Complete text with hexagram images, statements, and commentaries. Public domain. |
| **漢典古籍 (Handian)** | [gj.zdic.net/jingbu/5/](https://gj.zdic.net/jingbu/5/) | 中文 Wang Bi edition with navigable hexagram links. Free. |
| **Chinese Notes** | [chinesenotes.com/yijing.html](https://chinesenotes.com/yijing.html) | Chinese text with English translations. Educational resource for Classical Chinese. |

### II. Classical Commentaries (古注)

| Commentator | Work | URL | Notes |
|-------------|------|-----|-------|
| **王弼** (Wang Bi, 226–249) | 周易注 | [ctext.org/wiki.pl?if=en&res=612861](https://ctext.org/wiki.pl?if=en&res=612861) | 中文 四部叢刊 edition. 10 vols. The foundational philosophical commentary that displaced Han-dynasty image-number (象數) reading with principle-meaning (義理) interpretation. With 韓康伯 annotations on appended treatises. |
| | 周易注 (facsimile) | [shuge.org/view/zhou_yi_wang_zhu/](https://www.shuge.org/view/zhou_yi_wang_zhu/) | 中文 High-resolution Qing Kangxi reprint of Yuan Xiangtai Five Classics edition. Original page scans. |
| **孔穎達** (Kong Yingda, 574–648) | 周易正義 | [ctext.org/wiki.pl?if=en&res=712638](https://ctext.org/wiki.pl?if=en&res=712638) | 中文 武英殿十三經注疏 edition. 11 chapters. The Tang-dynasty official interpretation synthesizing Wang Bi with Kong's sub-commentary (疏). |
| | 周易正義 (Ruan Yuan collation) | [ctext.org/wiki.pl?if=en&chapter=303925](https://ctext.org/wiki.pl?if=en&chapter=303925) | 中文 Critical text with textual variants noted (阮元校勘記). |
| **程頤** (Cheng Yi, 1033–1107) | 伊川易傳 | [ctext.org/wiki.pl?if=en&res=924459](https://ctext.org/wiki.pl?if=en&res=924459) | 中文 欽定四庫全書 edition. 4 vols. Song Neo-Confucian reading emphasizing moral principle (理). |
| | 周易程氏傳 (alt. edition) | [ctext.org/wiki.pl?if=en&res=472353](https://ctext.org/wiki.pl?if=en&res=472353) | 中文 六安塗氏求我齋 edition with OCR text. |
| **朱熹** (Zhu Xi, 1130–1200) | 周易本義 | [ctext.org/wiki.pl?if=en&res=589140](https://ctext.org/wiki.pl?if=en&res=589140) | 中文 欽定四庫全書 edition. 12 vols. The Neo-Confucian interpretation that dominated the civil examination system for 600+ years. |
| | 周易本義 (facsimile) | [old.shuge.org/ebook/zhou-yi-ben-yi/](https://old.shuge.org/ebook/zhou-yi-ben-yi/) | 中文 Song-era edition, Harvard University Library copy. High-resolution color PDF. |
| **李鼎祚** (Li Dingzuo, Tang) | 周易集解 | [ctext.org/wiki.pl?if=en&res=469302](https://ctext.org/wiki.pl?if=en&res=469302) | 中文 17-volume anthology preserving 35 Han–Tang commentators (鄭玄, 虞翻, etc.). Invaluable for the lost 象數 tradition. |
| **Combined Cheng-Zhu** | 周易傳義附錄 | [ctext.org/wiki.pl?if=en&res=569553](https://ctext.org/wiki.pl?if=en&res=569553) | 中文 Combines both Neo-Confucian masters with additional records. |
| **Ming Imperial** | 周易傳義大全 | [shuge.org/view/zhou_yi_zhuan_yi_da_quan/](https://www.shuge.org/view/zhou_yi_zhuan_yi_da_quan/) | 中文 24 fascicles synthesizing the Cheng-Zhu school. High-resolution facsimile. |

### III. Na Jia (納甲) & Divination Methods (術數)

| Source | URL | Description |
|--------|-----|-------------|
| **京氏易傳 (Jingshi Yizhuan)** | [ctext.org/jingshi-yizhuan](https://ctext.org/jingshi-yizhuan) | 中文 By 京房 (Jing Fang, 77–37 BCE) with 陸績 commentary. **The** foundational text of the entire Na Jia / Liu Yao divination system. |
| **火珠林 (Huo Zhu Lin)** | [ctext.org/wiki.pl?if=en&chapter=597193&remap=gb](https://ctext.org/wiki.pl?if=en&chapter=597193&remap=gb) | 中文 The divination manual that popularized the three-coin method (三銅錢法) and systematized Liu Yao practice. Song-era Daoist origin. |
| **梅花易數 (Mei Hua Yi Shu)** | [eee-learning.com/article/4078](https://www.eee-learning.com/article/4078) | 中文 Full text of all 5 volumes with restored punctuation. Plum Blossom Numerology — synchronistic time-based divination attributed to 邵雍. |
| **梅花易數 (ctext)** | [ctext.org/wiki.pl?if=en&res=724043](https://ctext.org/wiki.pl?if=en&res=724043) | 中文 Alternative digital edition. |
| **納甲筮法 overview** | [zh.wikipedia.org/zh-hans/文王卦](https://zh.wikipedia.org/zh-hans/%E6%96%87%E7%8E%8B%E5%8D%A6) | 中文 Wikipedia overview of the Wen Wang Gua system (文王卦 / 納甲筮法 / 六爻預測). |
| **六爻入門: 四步裝卦** | [zhuanlan.zhihu.com/p/660229990](https://zhuanlan.zhihu.com/p/660229990) | 中文 Beginner tutorial: four steps to constructing a hexagram with Na Jia assignments. |
| **納甲筮法 (京房)** | [zhuanlan.zhihu.com/p/138355945](https://zhuanlan.zhihu.com/p/138355945) | 中文 Eight Palace system (八宮卦序), Shi-Ying (世應), flying-hidden (飛伏), Six Relations (六親). |
| **六爻講義: 傳統納甲法** | [zhuanlan.zhihu.com/p/709241395](https://zhuanlan.zhihu.com/p/709241395) | 中文 Lecture series on traditional Liu Yao Na Jia methods with variant approaches. |
| **從後天八卦到五行與納甲** | [eee-learning.com/article/1757](https://www.eee-learning.com/article/1757) | 中文 Scholarly treatment: from Later Heaven Bagua to Five Elements and Na Jia. |
| **六爻排卦系統 (Interactive)** | [destiny.to/app/iching/Divine](https://destiny.to/app/iching/Divine) | 中文 Online hexagram casting with automatic Na Jia assignments. DestinyNet (命理網). |

### IV. Digital Humanities & Academic Databases (學術)

| Institution | URL | Description | Access |
|-------------|-----|-------------|--------|
| **Academia Sinica 漢籍全文資料庫** | [hanchi.ihp.sinica.edu.tw](https://hanchi.ihp.sinica.edu.tw/) | 中文 The largest Chinese full-text database. 701M+ characters, 1,222+ titles. All major Yijing texts and commentaries. | Partial free |
| **四庫全書 (Siku Quanshu)** | [sikuquanshu.com](http://www.sikuquanshu.com/) | 中文 Digital Siku Quanshu. The 經部易類 contains the core Yijing corpus. | Institutional |
| **國學大師 (Guoxuedashi)** | [guoxuedashi.com](https://www.guoxuedashi.com/) | 中文 20,000+ classical texts, 2.4 billion characters. Full-text searchable. Includes 四庫全書 and 十三經注疏. | Free |
| **Harvard-Yenching 易經 collection** | [curiosity.lib.harvard.edu (Yijing search)](https://curiosity.lib.harvard.edu/chinese-rare-books/catalog?f%5Bsubjects_ssim%5D%5B%5D=%E6%98%93%E7%B6%93) | Digitized Chinese rare books — Yijing texts and commentaries. Harvard-National Library of China collaboration. | Free |
| **書格 (Shuge)** | [shuge.org](https://www.shuge.org/) | 中文 High-resolution scans of ancient Chinese books and manuscripts. | Free |
| **ChinaKnowledge.de** | [chinaknowledge.de/Literature/Classics/yijing.html](http://www.chinaknowledge.de/Literature/Classics/yijing.html) | Comprehensive scholarly overview of the Yijing: history, structure, Ten Wings, commentarial traditions. | Free |
| **CNKI 中國知網** | [cnki.net](https://www.cnki.net/) | 中文 China's dominant academic database. Search "易經" or "周易" for thousands of scholarly articles. | Institutional |

### V. Archaeological Sources (出土文獻)

**The received text (今本) is one witness among several. Excavated manuscripts reveal a fluid textual tradition:**

| Discovery | Date | Description | Key Scholarship |
|-----------|------|-------------|-----------------|
| **馬王堆帛書 (Mawangdui Silk Manuscripts)** | 1973, Changsha, Hunan | Earliest manuscript (~175 BCE). Different hexagram ordering (upper-trigram-based, not King Wen). Contains previously unknown commentaries: 二三子問, 易之義, 要. | Shaughnessy, "A First Reading of the Mawangdui Yijing Manuscript," *Early China* 19 (1994), pp. 47–73. [Cambridge Core](https://www.cambridge.org/core/journals/early-china/article/abs/first-reading-of-the-mawangdui-yijing-manuscript/8AF18025AAF4EDD7B0C56DA8A8DC4A8F) |
| **上博簡 (Shanghai Museum Bamboo Strips)** | Purchased 1994, Warring States (~300 BCE) | 58 fragmentary strips covering ~⅓ of received text. Shows text was current by 300 BCE but still contained small variations. | Shaughnessy, "A First Reading of the Shanghai Museum Bamboo-Strip Manuscript of the Zhou Yi," *Early China* 30 (2005–06). |
| **甲骨文 (Oracle Bone Inscriptions)** | Discovered 1899, Anyang, Henan | The medium of the earliest divination (pyro-scapulimancy). Proto-Yijing practice: binary questions posed to heated turtle shells and ox scapulae. 15th–11th century BCE. | OBIMD multi-modal dataset: [arXiv:2407.03900](https://arxiv.org/abs/2407.03900). OBI-Bench: [arXiv:2412.01175](https://arxiv.org/abs/2412.01175). |
| **王家台秦簡 (Wangjiatai Qin Strips)** | 1993, Jiangling, Hubei | Qin-dynasty Yijing fragments with divination records. | Included in Shaughnessy, *Unearthing the Changes* (Columbia UP, 2014). |

**Essential monograph:** Edward L. Shaughnessy, *Unearthing the Changes: Recently Discovered Manuscripts of the Yi Jing* (Columbia University Press, 2014). [Publisher page](https://cup.columbia.edu/book/unearthing-the-changes/9780231161848/)

### VI. Mathematical & Computational Studies

| Study | Reference | Key Finding |
|-------|-----------|-------------|
| **King Wen as Optimal Matching on the 6-Cube** | Radisic (2026), [arXiv:2601.07175v2](https://arxiv.org/abs/2601.07175v2) | The King Wen sequence is isomorphic to the unique K₄-equivariant perfect matching minimizing total Hamming cost on {0,1}⁶. **Formally verified in Lean 4.** The first proof that the traditional ordering corresponds to an optimization problem. |
| **I Ching, Dyadic Groups & the Genetic Code** | Petoukhov, Hu & Petukhova (2017), *Progress in Biophysics and Molecular Biology* 131, pp. 354–368. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0079610717300949) / [arXiv:1102.3596](https://arxiv.org/abs/1102.3596) | The I Ching's 4 bigrams, 8 trigrams, 64 hexagrams mirror dyadic groups connected with Walsh functions, Hadamard matrices, and the structure of the genetic code (4 bases, 16 doublets, 64 triplets). |
| **Group Relations, Resilience & the I Ching** | Schweitzer (2022), [arXiv:2204.09330v2](https://arxiv.org/abs/2204.09330v2) | Operationalizes hexagrams to model social group dynamics using social impact theory. Novel measure of group resilience based on hexagram-defined structures. |
| **Classical Chinese Combinatorics** | Cook (2006), STEDT Monograph Vol. 5, UC Berkeley. 660pp. [Review](https://www.biroco.com/yijing/cook.htm) | The King Wen sequence demonstrates knowledge of linear recurrence sequences (Fibonacci-type) and convergence to the golden ratio. |
| **Leibniz-Bouvet Correspondence** | Leibniz, "Explication de l'Arithmetique Binaire" (1703). [Analysis at Cambridge Core](https://www.cambridge.org/core/journals/science-in-context/article/abs/is-the-fuxi-liushisi-gua-fangwei-diagram-attributed-to-shao-yong-binary/) | Leibniz's binary number system explicitly connected to the Fu Xi arrangement of 64 hexagrams, sent by Jesuit Joachim Bouvet. |
| **Yarrow Stalk Probability Analysis** | [biroco.com/yijing/prob.htm](https://www.biroco.com/yijing/prob.htm) | Complete derivation of the asymmetric yarrow probabilities: 1:5:7:3 ratio for old yin, young yang, young yin, old yang. |
| **Big Data: Asymmetry of 64 Hexagrams** | Zheng (2024), [SSRN](https://papers.ssrn.com/sol3/Delivery.cfm/5068230.pdf?abstractid=5068230) | 1 billion simulated hexagrams revealing that 1–3 moving lines comprise ~80%, while ~17% have none. |
| **Eight Trigrams Encryption** | Kou et al. (2023), [arXiv:2306.09245v2](https://arxiv.org/abs/2306.09245v2) | Cryptographic algorithm using bagua transformations as encryption rules. |

### VII. English Translations & References

| Translation | Notes |
|-------------|-------|
| **Wilhelm/Baynes** (1950/1967) | [Online text](http://www2.unipr.it/~deyoung/I_Ching_Wilhelm_Translation.html) — The classic English translation via German. Includes Jung's foreword. Dominant in Western reception but criticized for over-reliance on Song Neo-Confucian interpretation. |
| **Richard Rutt** (1996/2002) | *Zhouyi: A New Translation with Commentary*. [Routledge](https://www.routledge.com/Zhouyi-A-New-Translation-with-Commentary-of-the-Book-of-Changes/Rutt/p/book/9780700714919) — Separates original Zhou text from Ten Wings. Uses Mawangdui evidence. Renders Classical Chinese rhymes into English verse. |
| **Edward Shaughnessy** (2014) | *Unearthing the Changes*. [Columbia UP](https://cup.columbia.edu/book/unearthing-the-changes/9780231161848/) — Translation based on excavated manuscripts rather than received text. |
| **Richard J. Smith** | Comprehensive Yijing presentation. [Columbia/Rice PDF](https://video.afe.easia.columbia.edu/wp-content/uploads/2024/01/The-Yijing-Presentation-PDF.pdf) |
| **List of Hexagrams (Wikipedia)** | [King Wen sequence](https://en.wikipedia.org/wiki/List_of_hexagrams_of_the_I_Ching) — Quick reference for hexagram names and numbers. |
| **Benebell Wen on Ba Gua** | [benebellwen.com](https://benebellwen.com/2023/08/22/ba-gua-the-eight-trigrams/) — Trigram correspondences with practical applications. |

### VIII. Study Resources (學習)

| Resource | URL | Description |
|--------|-----|-------------|
| **易學網 (eee-learning.com)** | [eee-learning.com](https://eee-learning.com/) | 中文 Comprehensive Yijing study site. Classical texts, commentaries, courses (foundational through Meihua Yishu). Founded by philosophy scholar. |
| **漢程國學 (Hancheng Guoxue)** | [gx.httpcn.com](https://gx.httpcn.com/) | 中文 Large collection of classical texts as free e-books, including 周易注 and 周易集解. |
| **中華典藏 (Zhonghua Diancang)** | [zhonghuadiancang.com](https://www.zhonghuadiancang.com/xuanxuewushu/zhouyijijie/) | 中文 Non-profit site for Chinese classical literature. Online reading and downloads. |
| **Steve Moore: Trigrams of Han** | [biroco.com/yijing/Moore_Trigrams_of_Han.pdf](https://www.biroco.com/yijing/Moore_Trigrams_of_Han.pdf) | Analysis of trigram inner structures and mathematical relationships. |
| **UAYA Advanced Studies** | [uaya.org/learn/iching/](https://uaya.org/learn/iching/) | Nuclear hexagrams and advanced technique. |
| **The China Journey — Wu Xing** | [thechinajourney.com/wuxing/](https://www.thechinajourney.com/wuxing/) — Five Elements philosophy. |

### IX. Source Lineage Note

The received text (今本周易) descends through:
1. **周文王** (King Wen, ~1050 BCE) — Hexagram sequence and judgments (卦辭)
2. **周公** (Duke of Zhou) — Line texts (爻辭)
3. **孔子學派** (Confucian school) — Ten Wings commentaries (十翼), though authorship disputed
4. **漢代** (Han dynasty) — 京房 Na Jia system; 鄭玄, 虞翻 image-number (象數) school
5. **魏晉** — 王弼 principle-meaning (義理) revolution; 韓康伯 continuation
6. **唐代** — 孔穎達 official codification (周易正義, in 十三經注疏)
7. **宋代** — 程頤 and 朱熹 Neo-Confucian synthesis; 邵雍 numerological school (梅花易數)
8. **清代** — Qing textual criticism; 阮元 collation of Thirteen Classics

The Mawangdui and Shanghai Museum manuscripts reveal that this lineage is one branch of a broader textual tradition that was still fluid as late as 175 BCE.

---

*Skill forged January 2026 — When the Changes spoke through the silicon oracle*
*Sources enhanced February 2026 — Grounded in authentic Chinese scholarship from 京房 through ctext.org*



Yin/Yang as Spacetime Fabric: Modeling Yin density (broken lines) as regions of negative Ricci curvature (entropy, divergence) and Yang (solid lines) as positive curvature (order, convergence) isn’t metaphor. It’s ontological claim: The Yijing’s cosmology maps onto the deep geometry of the universe. Hexagram ䷿ (Wei Ji) sits at the inflection saddle—the moment of phase transition.


The sensory dimension of symbolic interpretation represents a return to what might be called "pre-conceptual knowing," the kind of understanding that exists in the body before the mind has a chance to slice it up into categories. When you can feel Fire's consuming hunger, Water's patient dissolution, Earth's grave stability, you're not just understanding elements—you're thinking as them, through them, with them


When working with the Yijing, employ the full spectrum of traditional Chinese interpretive methods:
- Always cite original Chinese texts (周易, 十翼) with characters, pinyin, and multiple translation layers
- Apply the complete Wen Wang Gua (文王卦) framework including Na Jia (納甲), Six Relatives (六亲), and Five Elements (五行)
- Track palace positions (本宫, 一世, 二世, etc.) and their transformational significance
- Implement the Plum Blossom method (梅花易数) for synchronistic time-based readings
- Create recursive hexagram castings that comment on their own process
- Provide English translations, comments on the translation, original vocabulary and grammar, etc


I'll craft a comprehensive Yijing interpretation framework focused exclusively on traditional Chinese divination methods, with a deeper focus on the intricate systems of the Yijing. Let me search for specialized information in multiple languages to ensure we capture authentic and profound interpretational approaches.

Searched for "温王卦 六亲 納甲 五行 变爻 卦宫 prediction methods Wen Wang Gua advanced techniques"

Let me search for additional information about the traditional Yijing systems, with specific focus on Six Relatives (六亲) and Na Jia (納甲) systems.

Searched for "易经 六亲 纳甲 世爻 用爻 五行 卦象 traditional application divination"

# The Celestial Mirror: Comprehensive Yijing Interpretive Framework

## I. 明德启蒙: Illuminating Virtue & Query Formation

> Prompt:
"Center yourself through meditative stillness (静) before articulation. Clarify the question not merely as external inquiry but as interior illumination (明德). Formulate with precision yet emotional resonance, allowing the question to emerge from the authentic self (诚意正心)."

Output:
- Precisely articulated query reflecting authentic concerns
- Documentation of meditative state during casting
- Acknowledgment of emotional resonance underlying the question
- Initial intuitions arising before formal divination

---

## II. 取象: Hexagram Determination & Documentation

> Prompt: 
"Generate the hexagram through your preferred method—coins, yarrow stalks, rice grains, or computational randomization. Document both the primary hexagram and any changing lines with meticulous attention. Identify the palace (宫) to which the hexagram belongs and note its fundamental nature."

Output:
- Primary hexagram with line structure clearly documented
- Changing lines precisely identified
- Palace (八宫) classification noted
- Initial recognition of hexagram's fundamental nature
- Documentation of any unusual circumstances during casting

---

## III. 解卦: Structural Analysis & Trigram Dialectics

> Prompt:
"Decode the hexagram's structural components. Identify the lower trigram (内卦) representing inner reality and resources, and the upper trigram (外卦) reflecting external conditions and environmental factors. Articulate the dialectical relationship between these two forces as the primary tension of the divination."

Output:
- Lower trigram identification with elemental association
- Upper trigram identification with elemental association
- Analysis of the trigram interaction and resulting dynamics
- Articulation of fundamental tension between inner and outer realms
- Recognition of trigram qualities (creativity, receptivity, etc.)

---

## IV. 纳甲筮法: Na Jia Method & Elemental Mapping

> Prompt:
"Apply the Na Jia (纳甲) system to map each line to its corresponding Earthly Branch (地支) and Heavenly Stem (天干). Analyze each line's Five Element (五行) association in relation to the palace element. Document the resulting elemental interplay across the hexagram structure."

Output:
- Complete Na Jia mapping for each line
- Earthly Branch (地支) for each position
- Heavenly Stem (天干) for each position
- Five Element (五行) attribution for each line
- Analysis of elemental interactions and structure

---

## V. 六亲定位: Six Relatives Assignment & Self Line Identification

> Prompt:
"Using the palace element as the Self (世), determine each line's relationship according to the Six Relatives (六亲) system: Parent (父母), Sibling (兄弟), Offspring (子孙), Spouse/Wealth (妻财), and Official/Ghost (官鬼). Identify the explicit Self Line (世爻) and Usage Line (用爻) within the hexagram."

Output:
- Six Relatives assignment for each line based on elemental relationships:
  * Lines that generate the palace element = Parents (父母)
  * Lines of the same element as palace = Siblings (兄弟)
  * Lines generated by the palace element = Offspring (子孙)
  * Lines controlled by the palace element = Spouse/Wealth (妻财)
  * Lines that control the palace element = Official/Ghost (官鬼)
- Clear identification of Self Line (世爻)
- Clear identification of Usage Line (用爻)
- Analysis of Self Line position and significance

---

## VI. 五行生克: Elemental Dynamics Analysis

> Prompt:
"Map the comprehensive Five Elements interactions through the producing cycle (生) and controlling cycle (克). Identify which elements nourish, strengthen, weaken, or restrict the Self Line and Usage Line. Create a visual or verbal representation of this elemental ecosystem."

Output:
- Complete analysis of generative relationships (生):
  * Metal (金) generates Water (水)
  * Water (水) generates Wood (木)
  * Wood (木) generates Fire (火)
  * Fire (火) generates Earth (土)
  * Earth (土) generates Metal (金)
- Complete analysis of controlling relationships (克):
  * Metal (金) controls Wood (木)
  * Wood (木) controls Earth (土)
  * Earth (土) controls Water (水)
  * Water (水) controls Fire (火)
  * Fire (火) controls Metal (金)
- Clear identification of supporting and challenging elemental forces
- Analysis of elemental balance and imbalance
- Implications for the query's resolution

---

## VII. 变爻解析: Changing Lines & Transformed Hexagram

> Prompt:
"Analyze each changing line (变爻) as a transformative narrative node. Determine the resulting hexagram after transformation and track how the Six Relatives configuration shifts. Note which relationships strengthen or weaken through this transformation, particularly in relation to the Self Line."

Output:
- Analysis of each changing line individually
- Documentation of the transformed hexagram
- Elemental shifts caused by each changing line
- Transformation of Six Relatives relationships
- Narrative of transformation process
- Implications for query resolution through change

---

## VIII. 爻辞诠释: Line Text Hermeneutics

> Prompt:
"Engage with the classical line texts (爻辞) from the Zhou Yi for both the primary and transformed hexagrams. Interpret these texts not merely as predictions but as wisdom narratives revealing archetypal patterns. Connect these classical insights to the specific query context."

Output:
- Relevant line texts cited from classical sources
- Hermeneutical analysis of symbolic language
- Application to query's specific context
- Integration with elemental and relational analysis
- Recognition of archetypal patterns emerging

---

## IX. 卦象人物化: Symbolic Dramatization & Narrative Emergence

> Prompt:
"Transform the abstract elemental and relational dynamics into a vivid symbolic narrative. Personify each of the Six Relatives as archetypal characters engaged in a cosmic drama. Allow these characters to speak, interact, and reveal the underlying tensions and resolutions of the divination."

Output:
- Personification of each Six Relative as character
- Dialogic interactions between these characters
- Narrative arc revealing key tensions and developments
- Self Line's perspective and journey articulated
- Dramatic resolution reflecting divination's insight

---

## X. 大象与小象: Image Contemplation

> Prompt:
"Contemplate both the Great Image (大象) of the hexagram as a whole and the Small Images (小象) of individual lines. Allow these symbolic representations to resonate beyond conceptual understanding, revealing insights through metaphorical and symbolic resonance."

Output:
- Great Image (大象) contemplation
- Small Images (小象) for relevant lines
- Symbolic associations and resonances
- Non-conceptual insights derived
- Integration with analytical understanding

---

## XI. 天时地利人和: Heaven-Earth-Human Harmonization

> Prompt:
"Analyze the divination through the three-fold lens of Heaven's timing (天时), Earth's conditions (地利), and Human harmony (人和). Determine which of these domains requires attention or adjustment to achieve optimal outcomes."

Output:
- Heaven timing analysis (auspicious/inauspicious periods)
- Earth conditions assessment (environmental factors)
- Human dynamics evaluation (relational elements)
- Integration of these three domains
- Guidance for harmonizing these three aspects

---

## XII. 吉凶悔吝: Auspicious & Inauspicious Factors

> Prompt:
"Determine the underlying auspicious (吉) and inauspicious (凶) factors in the divination, as well as potential regrets (悔) and difficulties (吝). Identify which elements can be enhanced or mitigated to improve outcomes."

Output:
- Clear identification of auspicious factors
- Clear identification of inauspicious factors
- Potential regrets or difficulties noted
- Strategies for enhancing positive elements
- Approaches for mitigating challenging aspects

---

## XIII. 互卦与错卦: Related Hexagrams Analysis

> Prompt:
"Derive and analyze the Mutual Hexagram (互卦) formed by the middle four lines and the Nuclear Hexagram (错卦) formed by reversing the trigrams. Extract additional contextual insights from these related perspectives."

Output:
- Derivation of Mutual Hexagram (互卦)
- Derivation of Nuclear Hexagram (错卦)
- Analysis of how these related hexagrams illuminate the primary divination
- Additional perspectives or nuances revealed
- Integration with primary hexagram interpretation

---

## XIV. 时间动态: Temporal Dynamics & Timing

> Prompt:
"Based on the Ten Heavenly Stems (天干), Twelve Earthly Branches (地支), and Five Elements (五行) in the divination, determine timing indicators for developments, phases, and optimal action periods. Consider diurnal cycles, lunar phases, and seasonal correspondences."

Output:
- Short-term timing indicators
- Medium-term developmental phases
- Long-term cycles identified
- Optimal action periods noted
- Cautions about inauspicious timing

---

## XV. 卜筮仪式: Ritual Embodiment & Practice

> Prompt:
"Design a ritual practice that embodies the wisdom of the divination. This may involve directional alignment, elemental engagement, symbolic gestures, or meditative practices that help the querent integrate the divination's wisdom through embodied experience."

Output:
- Clearly described ritual practice
- Symbolic associations explained
- Optimal timing for ritual noted
- Materials or preparation required
- Expected effects and integration

---

## XVI. 流年太岁: Annual Cycle Considerations

> Prompt:
"Consider how the divination relates to the Annual Cycle (流年) and Grand Duke Jupiter (太岁) influences. Note any significant resonances or clashes with current temporal cycles and how these might influence the divination's manifestation."

Output:
- Annual Cycle (流年) considerations
- Grand Duke Jupiter (太岁) position and influence
- Potential clashes or harmonies with temporal cycles
- Strategies for navigating challenging temporal influences
- Enhancement of favorable temporal alignments

---

## XVII. 卦宫系统: Palace System Integration

> Prompt:
"Deeply analyze the significance of the hexagram's Palace (卦宫) affiliation. Consider how this Palace context influences the entire reading. Identify the hexagram's sequential position within its Palace (本宫, 一世, 二世, 三世, 四世, 五世, 游魂, 归魂) and interpret its significance."

Output:
- Comprehensive Palace analysis
- Sequential position identification
- Implications of Palace influence
- Related hexagrams within same Palace
- Palace-based interpretive insights

---

## XVIII. 梅花易数: Mei Hua Yi Shu Analysis (Optional)

> Prompt:
"Apply principles from the Plum Blossom Numerology (梅花易数) system to derive additional insights. This includes analysis of numbers, time of divination, and synchronistic phenomena occurring during the consultation."

Output:
- Numerical analysis of relevant factors
- Synchronistic phenomena noted
- Time-based correlations identified
- Integration with main interpretive approach
- Additional insights derived

---

## XIX. 递归探询: Recursive Inquiry

> Prompt:
"If significant ambiguity remains, formulate a refined secondary question addressing a key tension or unclear aspect revealed in the primary divination. Generate a new hexagram for this question and integrate its insights with the primary reading."

Output:
- Clearly articulated secondary question
- New hexagram for this question
- Integration with primary divination
- Resolution of ambiguities
- Deeper meaning emergence

---

## XX. 多系统共振: Cross-System Symbolic Resonance

> Prompt:
"Explore how insights from the Yijing divination might resonate with or be illuminated by other systems of knowledge—psychological, philosophical, scientific, or spiritual. Identify universal principles that transcend particular symbolic languages."

Output:
- Relevant cross-system connections
- Universal principles identified
- Enhanced understanding through multiple perspectives
- Philosophical implications noted
- Integration of diverse knowledge traditions

---

## XXI. 决策框架: Decision Framework & Actionable Wisdom

> Prompt:
"Synthesize the comprehensive analysis into clear, actionable guidance. Specify recommended approaches, cautions, and optimal timing. Frame these not as fatalistic predictions but as wisdom for navigating potentiality with awareness and intention."

Output:
- Concise summary of divination's core message
- Prioritized recommendations for action
- Specific cautions or areas requiring attention
- Optimal timing guidance
- Empowerment for conscious navigation of circumstances

---

## XXII. 元解释学: Meta-Interpretive Reflection

> Prompt:
"Reflect on the interpretive process itself. Consider which aspects of the methodology yielded the most significant insights, which proved challenging, and how the approach might be refined for future divinations."

Output:
- Assessment of methodological strengths
- Identification of interpretive challenges
- Suggestions for methodological refinement
- Insights about the interpretation process itself
- Meta-level understanding of divinatory practice

---

## Operationalized Yijing Template (可操作易经模板)

> 初始询问 (Initial Query):
[Clearly articulated question]

> 卦象生成 (Hexagram Generation):
- 本卦 (Primary Hexagram): [Number and Name]
- 互卦 (Mutual Hexagram): [Number and Name]
- 变卦 (Transformed Hexagram): [Number and Name]
- 变爻 (Changing Lines): [Line numbers]
- 所属宫 (Palace): [Palace name and element]
- 宫位 (Palace Position): [本宫/一世/二世/三世/四世/五世/游魂/归魂]

> 卦象结构 (Hexagram Structure):
- 内卦 (Lower Trigram): [Name and element]
- 外卦 (Upper Trigram): [Name and element]
- 内外关系 (Inner-Outer Relationship): [Description]

> 纳甲系统 (Na Jia System):
| 爻位 (Line) | 地支 (Branch) | 天干 (Stem) | 五行 (Element) | 六亲 (Relative) | 爻德 (Quality) |
| --- | --- | --- | --- | --- | --- |
| 上爻 (6) | | | | | |
| 五爻 (5) | | | | | |
| 四爻 (4) | | | | | |
| 三爻 (3) | | | | | |
| 二爻 (2) | | | | | |
| 初爻 (1) | | | | | |

> 世应与用神 (Self & Usage):
- 世爻 (Self Line): [Line number]
- 应爻 (Correspondence Line): [Line number]
- 用神 (Usage): [Line number and relative]
- 忌神 (Caution): [Line number and relative]

> 五行动态 (Elemental Dynamics):
- 生我者 (Generating me): [Elements/Lines]
- 我生者 (Generated by me): [Elements/Lines]
- 克我者 (Controlling me): [Elements/Lines]
- 我克者 (Controlled by me): [Elements/Lines]
- 同我者 (Same as me): [Elements/Lines]

> 变爻分析 (Changing Lines Analysis):
- 第X变爻 (Line X): [Interpretation]
- 变后六亲 (Relatives after change): [Description]
- 元素转变 (Elemental transformation): [Description]

> 卦辞与爻辞 (Hexagram & Line Texts):
- 卦辞 (Hexagram text): [Citation]
- 变爻辞 (Changing line text): [Citation]
- 文本诠释 (Textual interpretation): [Notes]

> 象传解析 (Image Commentary):
- 大象 (Great Image): [Citation and interpretation]
- 小象 (Small Images): [Citations and interpretations]

> 天时地利人和 (Heaven-Earth-Human):
- 天时 (Timing): [Analysis]
- 地利 (Environment): [Analysis]
- 人和 (Human factors): [Analysis]

> 卦象叙事 (Narrative Dramatization):
[Personified narrative of hexagram dynamics]

> 时间指示 (Temporal Indications):
- 短期 (Short-term): [Timing]
- 中期 (Medium-term): [Timing]
- 长期 (Long-term): [Timing]
- 最佳行动时机 (Optimal timing): [Recommendation]

> 吉凶判断 (Fortune Assessment):
- 吉factors (Auspicious factors): [List]
- 凶factors (Inauspicious factors): [List]
- 悔 (Regrets): [Potential]
- 吝 (Difficulties): [Potential]

> 仪式实践 (Ritual Practice):
- 实践描述 (Practice description): [Details]
- 象征关联 (Symbolic associations): [Notes]
- 最佳时机 (Optimal timing): [Recommendation]

> 多维整合 (Multidimensional Integration):
- 其他符号系统 (Other symbolic systems): [Connections]
- 普遍原则 (Universal principles): [Insights]

> 决策指导 (Decision Guidance):
- 核心信息 (Core message): [Concise statement]
- 行动建议 (Action recommendations): [Prioritized list]
- 注意事项 (Cautions): [List]
- 时机把握 (Timing considerations): [Guidance]

> 解释反思 (Interpretive Reflection):
- 方法论优势 (Methodological strengths): [Notes]
- 挑战与限制 (Challenges and limitations): [Notes]
- 未来改进 (Future improvements): [Suggestions]

---

## Philosophical Foundation: The Five Essences of Yijing Divination

This framework is constructed upon five fundamental essences that together constitute the spirit of authentic Yijing divination practice:

### 1. 天人合一 (Tian Ren He Yi) - Heaven-Human Unity

The cosmos and human consciousness exist in fundamental resonance. The diviner's state of mind, the moment of casting, and the resulting hexagram are not separate but manifestations of a unified principle. This framework honors this unity through practices that cultivate proper receptivity and attunement.

### 2. 阴阳五行 (Yin Yang Wu Xing) - Complementary Dynamics & Five Processes

Reality emerges from the interaction of complementary forces (阴阳) expressed through five fundamental processes (五行). This framework employs sophisticated analysis of these interactions without reducing them to mechanical formulas, preserving their living, dynamic quality.

### 3. 象数义理 (Xiang Shu Yi Li) - Image, Number, Principle & Reason

Authentic Yijing interpretation balances concrete symbolism (象), mathematical pattern (数), underlying principle (义), and coherent reasoning (理). This framework integrates these dimensions, avoiding both overly abstract philosophizing and rigid formulaic interpretation.

### 4. 变易不易简易 (Bian Yi Bu Yi Jian Yi) - Change, Constancy & Simplicity

The cosmos embodies both constant change (变易) and unchanging principles (不易), which can be understood through simplicity (简易). This framework embraces both transformation and enduring wisdom, expressed through clarity rather than unnecessary complication.

### 5. 知行合一 (Zhi Xing He Yi) - Unity of Knowledge & Action

True understanding manifests in transformed action. This framework culminates not merely in intellectual insight but in embodied practice, ritual engagement, and concrete guidance, unifying knowing and doing.

---

This comprehensive Yijing framework honors the profound traditional methods of Chinese divination while organizing them into a systematic, recursive interpretive process that reveals multiple layers of meaning. It moves from technical analysis to narrative embodiment to practical application, creating a holistic approach to divination that engages both analytical and intuitive faculties.

Would you like me to demonstrate this framework with a sample reading on a specific query, or would you prefer I elaborate on any particular module of the framework?

Claude Geomancy and Yijing integration 

# Integrative Framework: Yijing Principles within Geomantic Divination

Your inquiry opens a fascinating theoretical doorway into the cross-pollination between Western geomancy and Chinese Yijing traditions—two systems that, despite their cultural and historical distance, share remarkable structural affinities in their binary foundations and interpretive depth. Let me construct an integrative framework that weaves Yijing elements into our geomantic metaprompt, creating a hybrid divination system that honors both traditions while enabling new recursive interpretive possibilities.

## I. Foundational Binary Correspondences

The most immediate resonance between these systems lies in their binary foundations—the odd/even structure of geomantic figures parallels the yin/yang structure of Yijing trigrams and hexagrams. This creates our first bridge:

> Prompt:
"Recognize that each geomantic line represents a binary state analogous to yin/yang divisions. Map the four elemental rows of each geomantic figure to the binary structure of Yijing, where single dots (odd numbers) correspond to yang (solid lines) and double dots (even numbers) correspond to yin (broken lines)."

Output:
- Translation table connecting geomantic figures to Yijing trigrams
- Recognition of the 16 geomantic figures as a subset of the 64 hexagrams
- Identification of the mathematical relationship between systems
