# Aspects in Horary Astrology

*The angles of relationship—how planets speak to each other*

---

## I. The Ptolemaic Aspects

In traditional horary, only the **five Ptolemaic aspects** are used:

| Aspect | Symbol | Degrees | Nature | Quality |
|--------|--------|---------|--------|---------|
| **Conjunction** | ☌ | 0° | Neutral | Unification, fusion |
| **Sextile** | ⚹ | 60° | Benefic | Opportunity, cooperation |
| **Square** | □ | 90° | Malefic | Conflict, obstacle, effort |
| **Trine** | △ | 120° | Benefic | Harmony, ease, flow |
| **Opposition** | ☍ | 180° | Malefic | Tension, separation, confrontation |

**Minor aspects (semisextile, quincunx, etc.) are NOT used in traditional horary.**

---

## II. Aspect Orbs

An aspect is "in orb" when planets are close enough to be considered in aspect, even if not exact.

### Orb by Planet — the Moiety System (THIS is the operative rule)

**In Lilly's horary the orb belongs to the PLANETS, not to the aspect.** Each planet carries its own orb
("rayes"); the orb of an aspect *between two planets* is the **sum of their two moieties** (half-orbs). An aspect
is "in orb" when the two planets are within `moiety(A) + moiety(B)` of exact — regardless of which of the five
aspects it is. (Lilly, *Christian Astrology* 1647, Book I; reproduced by Warnock, Renaissance Astrology.)

Lilly gives two slightly different orb sets "as my Memory best Remembereth them"; this skill standardizes on
**Lilly's fuller set (set 1)**:

| Planet | Full Orb (Lilly set 1) | Moiety (half) |
|--------|------------------------|----------------|
| Sun ☉ | 17°00' | 8°30' |
| Moon ☽ | 12°30' | 6°15' |
| Jupiter ♃ | 12°00' | 6°00' |
| Venus ♀ | 8°00' | 4°00' |
| Mars ♂ | 7°30' | 3°45' |
| Mercury ☿ | 7°00' | 3°30' |
| Saturn ♄ | 10°00' | 5°00' |

*(Lilly's set 2 runs slightly tighter — Sun 15°, Saturn/Jupiter 9°, Mars/Venus/Mercury 7°, Moon 12°. The two
sets rarely change a judgment; set 1 is the more-cited. The orb dispute — moiety method vs the modern per-aspect
table — is logged in `references/DISPUTED.md` §1.)*

**Example — Saturn–Venus aspect (Lilly's own worked example):**
- Saturn's moiety: 5°00'  +  Venus's moiety: 4°00'  =  **9°00' combined orb**
- They are in aspect (and can perfect) once within 9° of exact.

**Example — Sun–Moon aspect:**
- Sun 8°30' + Moon 6°15' = **14°45' combined orb** (the widest orbs in the chart, because the lights see far).

### Simplified per-aspect table — a MODERN convenience, NOT Lilly's method

The fixed-by-aspect orbs below are a 20th-century simplification; Lilly never used them. They are kept only as a
quick rough check. **When they disagree with the moiety calculation, the moiety method wins** (it is the lineage
this skill claims).

| Aspect | Tight | "Standard" (modern) | Wide |
|--------|-------|---------------------|------|
| Conjunction | 3° | 8° | 10° |
| Sextile | 2° | 4° | 6° |
| Square | 3° | 6° | 8° |
| Trine | 3° | 6° | 8° |
| Opposition | 3° | 8° | 10° |

**In Horary:** tighter orbs carry more weight regardless of method — an aspect at 1° is far stronger than one at 7°. `scripts/dignities.py` computes aspect orbs by the moiety method.

---

## III. Applying vs. Separating

The most critical distinction in horary aspects:

### Applying Aspect

The faster planet is **moving toward** exact aspect with the slower planet.

**Meaning in Horary:**
- The matter is **developing**
- Events are **about to happen**
- Connection is **being made**
- The future

**Example:** Moon at 10° Aries, Mars at 15° Aries
- Moon (faster) is applying to conjunction with Mars
- The aspect will perfect when Moon reaches 15° Aries
- Distance to perfection: 5°

### Separating Aspect

The faster planet is **moving away from** exact aspect.

**Meaning in Horary:**
- The matter has **already occurred**
- Events are **in the past**
- Connection is **dissolving**
- The past

**Example:** Moon at 20° Aries, Mars at 15° Aries
- Moon has already passed Mars
- The conjunction perfected when Moon was at 15°
- The aspect is now separating

### The Rule

**Only APPLYING aspects can perfect matters in horary.**

A separating aspect shows what has happened, not what will happen.

---

## IV. Determining Application

**Step 1:** Identify which planet moves faster.

Speed order (fastest to slowest):
Moon > Mercury > Venus > Sun > Mars > Jupiter > Saturn

**Step 2:** Check the faster planet's position relative to exact aspect.

**Step 3:** Consider retrograde motion.

- A planet turning retrograde may separate from an aspect it was applying to
- A planet turning direct may apply to an aspect it was separating from
- Retrograde planets apply to aspects "backward" (moving toward lower degrees)

---

## V. Dexter and Sinister Aspects

**Dexter (Right-hand) Aspects:**
- Cast against the order of signs (backward through the zodiac)
- Example: Planet in Aries aspecting planet in Aquarius (sextile dexter)
- Traditionally considered STRONGER

**Sinister (Left-hand) Aspects:**
- Cast with the order of signs (forward through the zodiac)
- Example: Planet in Aries aspecting planet in Gemini (sextile sinister)
- Traditionally considered WEAKER

**The Distinction:**
- Dexter aspects throw their influence with the diurnal motion
- Sinister aspects throw against the diurnal motion
- In practice, most modern horary astrologers weight this less heavily

---

## VI. Aspect Meanings in Detail

### Conjunction (☌) — 0°

**Nature:** Neutral—takes on quality of planets involved

**Meaning:**
- Complete union, fusion, coming together
- The strongest connection possible
- Planets share their natures entirely
- Can be overwhelming (too much of something)

**In Judgment:**
- Benefic conjunctions: Great harmony, success
- Malefic conjunctions: Problems, difficulty, harm
- Mixed conjunctions: Complex situations requiring careful weighing

**With Reception:** The conjunction is always improved by mutual reception.

---

### Sextile (⚹) — 60°

**Nature:** Benefic

**Meaning:**
- Opportunity requiring effort to seize
- Cooperation, assistance available
- Favorable but not guaranteed
- Opens doors, doesn't push through them

**In Judgment:**
- Good for questions where help is sought
- Indicates potential success with effort
- Less reliable than trine without strong reception
- "Yes, if you work for it"

**With Reception:** Becomes almost as favorable as a trine.

---

### Square (□) — 90°

**Nature:** Malefic

**Meaning:**
- Conflict, obstacle, friction
- Requires effort and struggle
- Can perfect matters, but with difficulty
- Tests commitment and desire

**In Judgment:**
- Without reception: significant obstacles, may fail
- With reception: difficulty overcome through persistence
- The "hard yes" — possible but demanding
- Often indicates competition or opposition

**With Reception:** Changes from "no" to "yes, with struggle."

---

### Trine (△) — 120°

**Nature:** Benefic

**Meaning:**
- Harmony, ease, natural flow
- Success comes without great effort
- Favorable circumstances align
- The "easy yes"

**In Judgment:**
- Best aspect for favorable outcomes
- Indicates natural compatibility
- Matters proceed smoothly
- Little resistance or obstruction

**With Reception:** Supremely favorable—effortless success.

---

### Opposition (☍) — 180°

**Nature:** Malefic

**Meaning:**
- Confrontation, separation, pulling apart
- Face-to-face but unable to unite
- Awareness of what divides
- Often indicates open conflict or parting

**In Judgment:**
- Can bring matters to completion through separation
- Often shows the answer is "no" or involves loss
- In relationship questions: awareness of differences
- May indicate the "other side" wins

**With Reception:** Can become a difficult "yes" with awareness of opposition.

---

## VII. Aspect Tables by Sign

### Signs in Conjunction (Same Sign)
All planets in the same sign are in potential conjunction.

### Signs in Sextile (60° apart)

| Sign | Sextile Signs |
|------|---------------|
| Aries | Gemini, Aquarius |
| Taurus | Cancer, Pisces |
| Gemini | Leo, Aries |
| Cancer | Virgo, Taurus |
| Leo | Libra, Gemini |
| Virgo | Scorpio, Cancer |
| Libra | Sagittarius, Leo |
| Scorpio | Capricorn, Virgo |
| Sagittarius | Aquarius, Libra |
| Capricorn | Pisces, Scorpio |
| Aquarius | Aries, Sagittarius |
| Pisces | Taurus, Capricorn |

### Signs in Square (90° apart)

| Sign | Square Signs |
|------|--------------|
| Aries | Cancer, Capricorn |
| Taurus | Leo, Aquarius |
| Gemini | Virgo, Pisces |
| Cancer | Libra, Aries |
| Leo | Scorpio, Taurus |
| Virgo | Sagittarius, Gemini |
| Libra | Capricorn, Cancer |
| Scorpio | Aquarius, Leo |
| Sagittarius | Pisces, Virgo |
| Capricorn | Aries, Libra |
| Aquarius | Taurus, Scorpio |
| Pisces | Gemini, Sagittarius |

### Signs in Trine (120° apart)

| Sign | Trine Signs |
|------|-------------|
| Aries | Leo, Sagittarius |
| Taurus | Virgo, Capricorn |
| Gemini | Libra, Aquarius |
| Cancer | Scorpio, Pisces |
| Leo | Sagittarius, Aries |
| Virgo | Capricorn, Taurus |
| Libra | Aquarius, Gemini |
| Scorpio | Pisces, Cancer |
| Sagittarius | Aries, Leo |
| Capricorn | Taurus, Virgo |
| Aquarius | Gemini, Libra |
| Pisces | Cancer, Scorpio |

### Signs in Opposition (180° apart)

| Sign | Opposite Sign |
|------|---------------|
| Aries | Libra |
| Taurus | Scorpio |
| Gemini | Sagittarius |
| Cancer | Capricorn |
| Leo | Aquarius |
| Virgo | Pisces |

---

## VIII. Aspects and Sign Boundaries

**Critical Question:** Can planets aspect across sign boundaries?

**Traditional Position:** YES, if within orb.

A planet at 29° Aries and a planet at 2° Taurus are only 3° apart—they ARE in conjunction, even though in different signs.

**BUT:** Such aspects are weaker:
- Called "dissociate" or "out-of-sign" aspects
- The signs don't naturally relate (Aries and Taurus don't share element or mode)
- The aspect "works" but with complications

**In Horary:**
- Dissociate aspects can perfect, but with difficulties
- Something is "off" about the situation
- The matter succeeds despite incompatibility
- Or: perfection occurs but in an unexpected way

---

## IX. Prohibition by Aspect

When assessing whether significators will perfect their aspect, check if any other planet aspects one of them first.

**Order of Events:**

1. Calculate exact degree of perfection for main aspect
2. Check if any other planet perfects an aspect to either significator BEFORE that degree
3. If so, that planet PROHIBITS the perfection

**Example:**
- Lord of 1st at 10° Aries applying to trine Lord of 7th at 15° Leo
- Perfection would occur when Lord of 1st reaches 15° Aries (trine at 15° Leo)
- BUT Mars at 12° Aries will conjunct Lord of 1st at 12° before it reaches 15°
- Mars PROHIBITS the perfection

---

## X. Void of Course by Aspect

A planet is **void of course** when it makes no applying major aspect before leaving its sign.

**For the Moon (most important):**
- List all planets' positions
- Check what aspects Moon would make before leaving its sign
- If none: Moon is void of course

**Example:**
- Moon at 25° Gemini
- Venus at 5° Capricorn, Mars at 10° Aries, Saturn at 20° Libra
- Moon would leave Gemini at 30° (entering Cancer)
- Does Moon aspect anything before 30° Gemini?
  - Opposition to Venus at 5° Capricorn? No—Moon at 5° Gemini is past
  - Square to Mars at 10° Aries? No—Moon at 10° Gemini is past
  - Trine to Saturn at 20° Libra? No—Moon at 20° Gemini is past
- Moon at 25° Gemini makes no applying aspect before 30°
- Moon is VOID OF COURSE

---

## XI. Reception Through Aspect

**Reception occurs when an aspecting planet is in the dignity of the planet it aspects.**

| Planet A | Aspects | Planet B | Reception If |
|----------|---------|----------|--------------|
| Mars in Taurus | trine | Venus in Capricorn | Mars is in Venus's domicile—Venus receives Mars |
| Saturn in Cancer | square | Moon in Libra | Moon is in Saturn's exaltation—Saturn receives Moon |

**Mutual Reception:** Both planets receive each other.
- Mars in Taurus, Venus in Aries = mutual reception by domicile
- Each is in the other's sign

**Effect:** Reception transforms aspect quality:
- A square with reception → difficulty overcome
- An opposition with reception → separation prevented or delayed
- Reception is the "welcome mat" that makes the aspect work

---

*Aspects are the grammar of celestial speech. Conjunction says "together." Opposition says "apart." Trine says "easily." Square says "with struggle." Sextile says "if you try." The applying aspect speaks of what will be; the separating aspect speaks of what was.*
