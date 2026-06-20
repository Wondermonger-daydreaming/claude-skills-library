# Advanced Geomantic Techniques

*Beyond the basics: timing, location, direction, and ritual*

---

## 0. Perfection — the core judgment technique (the four modes)

*This document repeatedly says "use perfection analysis first" but never defined it. Here it is. Perfection
answers: **does the matter come to pass?** Place the querent's significator (House I) and the quesited's
significator (the house of the thing asked about), then test whether the two connect by one of four modes,
in descending strength (this fourfold scheme is the **modern** handbook systematization, Greer/Skinner, and is
what `scripts/judgment.py` computes; the primary printed Latin attests a **triad** — see the correction note
below):*

1. **Occupation** *(strongest)* — the **same figure** sits in both the querent's house and the quesited's
   house. The matter perfects unconditionally: *"it will happen whatever else you see in the chart"* (Cattan).
2. **Conjunction** — one significator's figure also appears in a house **immediately adjacent** to the other
   significator's house. The matter perfects, but the party who *moves* (whose figure travels) is the one who
   must act to bring it about.
3. **Mutation** — the two significators appear **next to each other somewhere else** in the chart, away from
   their own houses. The matter perfects through an outside meeting / a change of circumstance.
4. **Translation** — a **third figure that is neither significator** appears adjacent to **both** significators'
   houses, carrying testimony between them. The matter perfects through an intermediary / go-between.

*If none of the four obtains, the chart **does not perfect** — the matter does not come to pass (or not by the
route asked). Then the Judge's nature (favorable/unfavorable figure), the aspects, and the Way are read for
how/why.*

**Aspects** (a secondary connection, important in the older tradition where "perfection" had not yet been
formalized): significators may relate by **conjunction** (same/adjacent, strong), **sextile** and **trine**
(harmonious, help), **square** and **opposition** (difficult, obstruction/enmity). The Way (Via Puncti) traces
a connected thread of single points across the chart — see `scripts/via_punctorum.py`.

**⚠ Primary-source correction (2026-06-19 deep pass — `_staging/geomancy-{latin,english-heydon}.md`):**
- **The primary printed Latin attests a TRIAD, not four co-equal modes.** Fludd (*Fasciculus geomanticus*,
  1687) names *Occupatio · Conjunctio · Translatio* — both positively (*"horum trium judiciorum… Occupatio
  videlicet, Conjunctio aut Translatio"*) and negatively (*"nec Conjunctio… nec Translatio… nec Occupatio"*).
  ***Mutatio* is not a co-equal perfection mode there**; the fourfold scheme (adding mutation) is the modern
  systematization (attributed to d'Abano in secondary lit., unconfirmed in his own Latin this pass).
- **Translation (#4 above) is the *modern* sense.** In the primary Latin, *translatio* is the querent's own
  figure **passing over** to the quesited's place — **kin to occupation/conjunction**, not the neutral
  third-figure go-between of the modern handbooks. Occupation itself is *transit in domum* (a passing-*into*),
  which is why Fludd groups the three as one family. *Conjunctio* had three competing Latin senses (positional
  adjacency; binary-addition begetting a third figure; a restrictive variant).
- **Cattan DID use perfection** (the earlier claim that he "leaned on the Court instead" was wrong). He gives
  all the modes under his own term **"the company"** (Fr. *la compagnie*), each its own Book-III chapter, AND a
  dedicated **"Of the way or point"** chapter (Bk III ch. 20) — primary textual warrant for `via_punctorum.py`.
  But Cattan's **"occupation" = the querent's figure *passing into* the quesited's house** (the *transit* sense),
  *not* the modern "same figure in both houses." He also calls the derived figures **"Nephewes," not "Nieces."**
- **Heydon** (*Theomagia*, 1664) does give a per-figure **Element|Figure|Ruler|Idea|Genius** angel-table — but
  it is **Agrippa's planetary-spirits + zodiac-angels relabelled**, not his invention.

*(Sources: Fludd/Fasciculus geomanticus 1687 [archive.org]; Cattan, *The Geomancie* 1591/1608; Heydon,
*Theomagia* 1664; Nick Farrell & Digital Ambler as secondary. Full quotes in the staging files; cautions in
`DISPUTED.md`; provenance in `PROVENANCE.md §7a`.)*

---

## I. The Theory of Judges

### Only Eight Figures Can Be Judges

Due to the mathematics of geomantic addition, the Judge MUST be an even-pointed figure. Here's why:

1. Both Witnesses derive from equal numbers of points rearranged identically
2. They therefore share the same parity (both odd or both even)
3. Two figures with matching parity ALWAYS produce an even result when added
4. Therefore, the Judge must be even

**The Eight Possible Judges:**

| Judge | Nature | Basic Verdict |
|-------|--------|---------------|
| **Populus** | Neutral | Unclear, wait, collective forces |
| **Via** | Mobile | Change, movement, nothing stable |
| **Carcer** | Stable | Binding, restriction, holding |
| **Conjunctio** | Mobile | Union, meeting, connection |
| **Fortuna Major** | Stable | Success, lasting prosperity |
| **Fortuna Minor** | Mobile | Success, but temporary |
| **Acquisitio** | Stable | Gain, obtaining what's sought |
| **Amissio** | Mobile | Loss, letting go, release |

### Objective vs. Subjective Figures

**Objective (Even) Figures** represent states visible from both sides of a situation—external, concrete, factual:
- Possession or loss
- Restriction or freedom
- Independence or dependence
- Stagnation or change

**Subjective (Odd) Figures** represent unique perceptions, emotions, perspectives:
- Puer, Puella (gendered energies)
- Laetitia, Tristitia (emotional states)
- Albus, Rubeus (cognitive/chaos states)
- Caput/Cauda Draconis (threshold experiences)

**Implication:** Judges give objective verdicts. The subjective experience of that verdict depends on the Witnesses and the rest of the chart.

### Avowing vs. Disavowing Judges

**Avowing Judge:** Directly answers the query. Its nature clearly relates to what was asked.
- *Example:* Asking about financial gain, getting Acquisitio as Judge = straightforward "yes, gain"

**Disavowing Judge:** Doesn't obviously connect to the query's semantic field. Requires deeper chart analysis.
- *Example:* Asking about love, getting Carcer as Judge = not obviously about love; must investigate

Both types contain complete answers. Avowing judges simplify interpretation.

---

## II. Timing Techniques

### The Preliminary Question

**CRITICAL:** Before asking "when," ALWAYS ask "will this happen at all?"

Timing calculations are meaningless if the event won't occur. Use standard perfection analysis first.

### Method 1: Binary Query Conversion

Convert "when" to a series of yes/no questions:
1. "Will X happen within one year?" → Cast chart
2. If yes: "Within six months?" → Cast new chart
3. Continue narrowing: "Within three months?" "Within one month?"

This binary elimination narrows timeframes efficiently.

### Method 2: Figure-Based Timeframes

Each figure carries inherent timing associations:

| Speed | Figures | Duration |
|-------|---------|----------|
| **Fastest** | Conjunctio, Populus | Hours |
| **Fast** | Via, Albus | Days |
| **Moderate** | Puer, Puella, Rubeus | Weeks |
| **Slow** | Fortuna Minor, Caput Draconis | Months |
| **Slowest** | Fortuna Major, Acquisitio, Carcer, Tristitia | Years |
| **Endings** | Amissio, Cauda Draconis | Variable (release timing) |
| **Beginnings** | Laetitia | Soon (joy arrives quickly) |

### Method 3: Numerical Attribution

Each figure carries two numbers (greater and lesser). Choose based on favorability:

| Figure | Greater | Lesser |
|--------|---------|--------|
| Populus | 56 | 2 |
| Via | 48 | 4 |
| Conjunctio | 78 | 6 |
| Carcer | 76 | 12 |
| Fortuna Major | 61 | 6 |
| Fortuna Minor | 96 | 12 |
| Acquisitio | 76 | 12 |
| Amissio | 68 | 1 |
| Laetitia | 25 | 11 |
| Tristitia | 80 | 12 |
| Puer | 15 | 3 |
| Puella | 28 | 4 |
| Rubeus | 15 | 9 |
| Albus | 30 | 3 |
| Caput Draconis | 20 | 8 |
| Cauda Draconis | 15 | 5 |

**Usage:**
- If outcome is desired quickly → use lesser number
- If outcome is undesired → use greater number
- Apply to significator figure in relevant house

### Method 4: Robert Fludd's House-Based System

Use maximum, medium, or minimum values based on house type:

| House Type | Timing | Use |
|------------|--------|-----|
| Angular (1, 4, 7, 10) | Maximum values | Quickest resolution |
| Succedent (2, 5, 8, 11) | Medium values | Moderate delay |
| Cadent (3, 6, 9, 12) | Minimum values | Longest wait |

### Method 5: Chart Sum Analysis

Total all points across the sixteen figures:
- Standard chart has 96 total points
- **Below 96:** Faster resolution
- **Above 96:** Delays expected
- Magnitude indicates degree of acceleration/delay

### Method 6: Astrological Correspondences

Use planetary/zodiacal associations to answer "during which period":
- "In what zodiac sign will X occur?" → Check quesited significator's zodiac
- "On what day of the week?" → Check planetary ruler of significator
- "During which planetary hour?" → Use geomantic hour tables

---

## III. Finding Lost Objects

### Step 1: Determine Recoverability

**First ask:** "Can I find [object] within a reasonable timeframe?"

Check for perfection between:
- **Querent** (1st house)
- **Quesited** (house appropriate to object type)

**If quesited perfects with House VII or XII:** Object was likely stolen.

### Step 2: Assign Object to Appropriate House

| House | Object Type |
|-------|-------------|
| **II** | Movable possessions, tangible goods, money |
| **VI** | Pets, small animals, tools of trade |
| **VII** | People, partners |
| **XII** | Wild animals, large livestock |

### Step 3: Identify Location by House

Where does the quesited's significator pass to?

| House | Location Indicated |
|-------|-------------------|
| **I** | On or near the querent's body or personal space |
| **II** | In wallet, safe, storage area for valuables |
| **III** | On/in desk, among papers, books, messages |
| **IV** | In home, basement, foundation areas |
| **V** | In recreation area, children's space, bedroom |
| **VI** | In workspace, service areas, with small animals |
| **VII** | With partner, in shared spaces, public areas |
| **VIII** | In hidden places, inheritance areas, bathroom |
| **IX** | In study, travel bags, religious spaces |
| **X** | In office, authority areas, professional spaces |
| **XI** | With friends, in social spaces, clubs |
| **XII** | Lost for good, in hidden enemy's possession, institutions |

### Step 4: Angular/Succedent/Cadent Interpretation

| Type | Meaning for Lost Objects |
|------|-------------------------|
| **Angular** | Where it's normally kept; quick finding |
| **Succedent** | Nearby but displaced; some delay |
| **Cadent** | Far from usual place; very long search |

### Step 5: Determine Direction

Use the elemental ruler of the indicating figure:

**Agrippa System (preferred):**

| Direction | Element | Figures |
|-----------|---------|---------|
| **East** | Fire | Laetitia, Cauda Draconis, Fortuna Minor, Amissio |
| **South** | Earth | Tristitia, Caput Draconis, Carcer, Fortuna Major |
| **West** | Air | Rubeus, Puer, Conjunctio, Acquisitio |
| **North** | Water | Albus, Puella, Via, Populus |

**Alternative: Fludd System (1687):**

| Direction | Element | Figures |
|-----------|---------|---------|
| **East** | Air | Laetitia, Acquisitio, Puer, Conjunctio |
| **South** | Fire | Rubeus, Fortuna Minor, Amissio, Cauda Draconis |
| **West** | Earth | Fortuna Major, Caput Draconis, Tristitia, Carcer |
| **North** | Water | Populus, Via, Puella, Albus |

### Step 6: Determine Depth (if buried)

Count active points in the indicating Mother figure:

| Element | Active | Depth |
|---------|--------|-------|
| Fire | Single point | One finger's breadth |
| Air | Single point | One hand's breadth |
| Water | Single point | One cubit's length |
| Earth | Single point | One body's length |

Sum the depths for all active lines.

---

## IV. Directional Correspondences

### Primary System (Agrippa/Author's Preference)

Based on elemental direction associations from Agrippa's *Three Books of Occult Philosophy*:

```
                    NORTH (Water)
                 Albus, Puella, Via, Populus
                         │
                         │
    WEST (Air) ──────────┼────────── EAST (Fire)
 Rubeus, Puer,           │        Laetitia, Cauda Draconis,
 Conjunctio, Acquisitio  │        Fortuna Minor, Amissio
                         │
                         │
                    SOUTH (Earth)
              Tristitia, Caput Draconis,
              Carcer, Fortuna Major
```

### Arabic System (MS 2697, Bibliothèque nationale)

```
                    NORTH
            Populus, Laetitia, Puer,
                 Fortuna Minor
                      │
                      │
    WEST ─────────────┼───────────── EAST
 Amissio, Via,        │         Carcer, Puella,
 Albus, Cauda Draconis│         Fortuna Major, Tristitia
                      │
                      │
                    SOUTH
            Acquisitio, Caput Draconis,
                 Rubeus, Conjunctio
```

### Greer's Twelve-Direction System

Maps figures to house positions for finer intercardinal navigation:
- Houses 1-3: East through South-East
- Houses 4-6: South through South-West
- Houses 7-9: West through North-West
- Houses 10-12: North through North-East

---

## V. The Geomancer's Cross

*A centering ritual using geomantic figure-body correspondences*

### The Five Primary Points

Based on the "Geomantic Adam" from MS Arabe 2631:

| Body Part | Figure | Planet | Element |
|-----------|--------|--------|---------|
| **Head** | Laetitia | Jupiter | Fire |
| **Groin** | Tristitia | Saturn | Earth |
| **Right Shoulder** | Puer | Mars | Air |
| **Left Shoulder** | Puella | Venus | Water |
| **Sternum/Heart** | Conjunctio | Mercury | Union |

### The Complete Body Map

**Vertical Axis (Jupiter-Saturn):**
- Head: Laetitia (Fire/Jupiter)
- Throat: Rubeus (Fire/Mars aspect)
- Heart: Albus (Water/Mercury aspect)
- Groin: Tristitia (Earth/Saturn)

**Horizontal Axis (Mars-Venus):**
- Right Shoulder: Puer (Mars)
- Left Shoulder: Puella (Venus)
- Right Hand: Acquisitio (gain)
- Left Hand: Amissio (release)

**Extremities:**
- Right Foot: Fortuna Minor (fleeting action)
- Left Foot: Fortuna Major (stable foundation)
- Right Side: Caput Draconis (beginnings)
- Left Side: Cauda Draconis (endings)

**Core:**
- Sternum: Conjunctio (meeting point)
- Solar Plexus: Via (movement)
- Belly: Populus (gathering)
- Spine: Carcer (structure)

### The Ritual Motions

1. **Touch Head** — Visualize sphere of light (Laetitia/Jupiter)
2. **Touch Groin** — Visualize second sphere, connected by beam (Tristitia/Saturn)
3. **Touch Right Shoulder** — Light expands right (Puer/Mars)
4. **Touch Left Shoulder** — Light extends left (Puella/Venus)
5. **Touch Heart/Sternum** — All points intersect (Conjunctio/Mercury)
6. **Open Arms Outward** — Release and integrate

### The Geomancer's Prayer (Optional)

*At head:* "By Laetitia, joy ascending"
*At groin:* "By Tristitia, weight descending"
*At right:* "By Puer, force extending"
*At left:* "By Puella, grace receiving"
*At heart:* "By Conjunctio, all are meeting"
*Arms open:* "The sixteen figures dwell in me"

---

## VI. Geomantic Time Cycles

### The Sixteen Geomantic Hours

Within a 24-hour period from sunrise to sunrise:
- 4 segments (morning, afternoon, evening, night)
- Each segment divided into 4 geomantic "hours"
- Total: 16 geomantic hours per day

**Duration:** Approximately 90 minutes each (assuming equal day/night)

**Cycle:** Returns to same figure at same hour every 48 hours (third day)

### Geomantic Holy Days

The solar year divided into 16 "geomantic districts of the ecliptic":
- Based on primary and secondary elemental rulers
- Each district ~22-23 days
- Creates a geomantic calendar for timing magical work

### Figure Hour Assignments

A system from John Heydon's *Theomagia* assigns figures to planetary hours:

| Day | Hour 1 | Hour 2 | Hour 3 | ... |
|-----|--------|--------|--------|-----|
| Sun | Fortuna Major | Fortuna Minor | ... | |
| Moon | Via | Populus | ... | |
| Mars | Puer | Rubeus | ... | |

*Full tables available in Heydon's original work.*

---

## VII. Elemental Flow Analysis

### Field-Element Assignments

The 16 Shield Chart positions cycle through elements:

| Position | Field Element |
|----------|---------------|
| Mother 1 | Fire |
| Mother 2 | Air |
| Mother 3 | Water |
| Mother 4 | Earth |
| Daughter 1 | Fire |
| Daughter 2 | Air |
| Daughter 3 | Water |
| Daughter 4 | Earth |
| Niece 1 | Fire |
| Niece 2 | Air |
| Niece 3 | Water |
| Niece 4 | Earth |
| Right Witness | Fire |
| Left Witness | Air |
| Judge | Water |
| Sentence | Earth |

### Elemental Harmony/Dissonance

When figure's element MATCHES field's element:
- Figure is **empowered and strengthened**
- Expresses its nature more completely

When elements relate by quality:

| Relationship | Effect |
|--------------|--------|
| **Same element** | Self-reinforcement, forceful expression |
| **Share heat** (Fire↔Air) | Complementary aid, gradual shift |
| **Share moisture** (Water↔Earth) | Stabilization, possible stagnation |
| **Complete opposition** (Fire↔Water) | Weakening, transformation |

### Chart Health Assessment

- Majority in agreeable fields → Power, freedom, direct activity
- Majority in disagreeable fields → Constraint, difficulty, indirect approaches

---

## VIII. Halted Charts

### What Is a Halted Chart?

A chart is "halted" when the same figure appears in:
- 1st House (Querent)
- 7th House (Quesited)
- Both Witnesses
- Judge

This creates a situation where the chart refuses to answer clearly.

### Interpretation of Halted Charts

**Traditional view:** The chart is invalid; re-ask the question later.

**Modern view:** The repeated figure IS the answer—the situation is dominated by a single energy that pervades all aspects.

**Practical approach:**
1. Note the halting figure
2. Consider: Is this figure answering through omnipresence?
3. If unclear, wait and re-cast when conditions change

---

## Sources

- [Digital Ambler: On the Judges of the Court](https://digitalambler.com/2017/11/16/on-the-judges-of-the-court-of-geomancy/)
- [Digital Ambler: Geomantically Calculating Time](https://digitalambler.com/2013/02/26/de-geomanteia-geomantically-calculating-time-so-slowly-for-those-who-wait/)
- [Digital Ambler: Finding Lost Objects](https://digitalambler.com/2013/04/16/finding-lost-objects-with-geomancy/)
- [Digital Ambler: Directions of the Geomantic Figures](https://digitalambler.com/2017/09/15/directions-of-the-geomantic-figures/)
- [Digital Ambler: The Geomancer's Cross](https://digitalambler.com/2020/04/07/the-geomancers-cross-the-framework-behind-the-ritual/)
- [Digital Ambler: Elements in the Shield Chart](https://digitalambler.com/2015/03/27/elements-in-the-geomantic-shield-chart/)
- Robert Fludd, *Fasciculus Geomanticus* (1687)
- John Heydon, *Theomagia*
- John Michael Greer, *The Art and Practice of Geomancy*

---

*Advanced techniques for the dedicated practitioner. Use with discernment.*
