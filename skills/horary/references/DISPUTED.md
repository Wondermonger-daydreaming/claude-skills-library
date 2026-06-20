# DISPUTED — the horary "do not import as canonical" registry

*Modelled on the geomancy skill's `DISPUTED.md`. One place to find every horary claim that is **contested across
traditions**, **silently modernized**, or **epoch-stale** — so no future reader (human or instance) mistakes one
tradition's choice (or a 20th-century simplification) for "the lineage of William Lilly."*

Compiled from a primary-source descent, verified against a dignity-spine audit and an invoked-but-undefined
sweep. Where a fix was already applied to the
references, it is noted **[FIXED …]**.

**Rule of thumb.** If a claim is about the **chart's geometry/math** (precession, degrees-to-perfection), it is
computable and settled — *get the number right*. If it is about **which historical scheme to apply** (house
system, terms, triplicity rulers, orbs, what afflicts or disqualifies), it is one of several traditions — *name
which, cite who holds it, pick a transparent default, and never let a modern convenience or a single author's
flourish harden into "what Lilly did."*

---

## A. Genuine disputes — name the camps, pick a transparent default

### 1. ORBS — Lilly's per-PLANET moiety vs the modern per-ASPECT table ⚠ HEADLINE / METHOD-FIDELITY GAP

**Contested:** does an aspect's orb come from the **two planets** (Lilly: each planet has its own orb; in-orb =
within the sum of the two moieties/half-orbs) or from the **aspect type** (modern: conjunction 8–10°, sextile
4–6°, … regardless of planet)?

- **Lilly / traditional → orbs belong to PLANETS.** *Christian Astrology* (1647) assigns each planet an orb;
  an aspect perfects within the sum of the two half-orbs. Worked example, verbatim: *"the Moity of Saturn his
  Rayes or Orbs is five, and of Venus 4, and the distance betwixt them and their perfect aspect is eight
  degrees"* (so orb-of-aspect = moiety A + moiety B). Source: Warnock / Renaissance Astrology, reproducing CA
  1647 — renaissanceastrology.com/aspects.html.
- **The fixed per-aspect table is a 20th-c. simplification** — it appears nowhere in Lilly.

**What the skill did wrong:** `SKILL.md` shipped only the modern per-aspect table as *the* method, while
`ASPECTS.md` already carried the correct moiety table — the skill *knew* the lineage method but didn't use it.

**Resolution / default: the moiety method is operative.** **[FIXED ASPECTS.md §II]** — moiety table
standardized to Lilly's fuller "set 1" (Sun 17°, Moon 12°30′, Jupiter 12°, Saturn 10°, Venus 8°, Mars 7°30′,
Mercury 7°), the per-aspect table demoted to "modern convenience; moiety wins on conflict," and
`scripts/dignities.py` computes orbs as moiety(A)+moiety(B). Lilly's set 2 (tighter) is noted; it rarely changes
a judgment.

### 2. HOUSE SYSTEM — Regiomontanus vs Whole-Sign (Placidus is a non-contender for horary)

- **Regiomontanus — Lilly's actual system, the Renaissance-horary standard.** Frawley, *The Horary Textbook*:
  *"I urge you to use this for horary. It is the system used by Lilly, and it works."*
- **Whole-Sign — the Hellenistic/medieval-revival claim** of the older default (Sahl ibn Bishr, Māshā'allāh,
  predating quadrant houses).
- **Placidus — no significant traditional-horary advocate**; carried in only by those who don't switch by branch.
  Frawley explicitly rejects it for horary.

**What the skill does:** "Regiomontanus preferred; Placidus acceptable" + `cast_chart.py` defaults to
Regiomontanus. **Default kept (Regiomontanus = Lilly).** Honest amendment for the lean SKILL: the real
alternative to name is **Whole-Sign**, not Placidus.

### 3. TERMS / BOUNDS — Egyptian vs Ptolemaic, and "used by Lilly" is BACKWARDS

- **Lilly used the PTOLEMAIC terms, not the Egyptian** (reverses the common claim). Anthony Louis; *Medieval
  Astrology Guide* ("William Lilly actually used Ptolemy's approach, not Egyptian terms"); De Nova Stella
  ("Both Lilly and Bonatti use Ptolemy's terms").
- **Terminology trap:** Ptolemy's *Tetrabiblos* prints both the "Egyptian" and the now-"Ptolemaic" tables; Lilly
  called the Ptolemaic set the **"Chaldean"** terms — which is why Egyptian/Chaldean/Ptolemaic get tangled.
  (Houlding, "The Transmission of Ptolemy's Terms," *Culture & Cosmos* 11.)
- **Egyptian terms = the live alternative**, held by the Hellenistic/medieval revival (Lehman; Project Hindsight).

**What the skill did wrong:** `DIGNITIES.md` said *"Egyptian terms (used by Lilly)"* — false conjunction.
**Resolution: keep the table (the 60 boundaries are verified-correct Egyptian terms, the revival default), fix
the attribution.** **[FIXED DIGNITIES.md §V]** — relabeled "Egyptian, the revival default; Lilly's own table
used Ptolemy's terms." The numbers were NOT changed (correcting a verified-correct table on a label dispute would
be the error).

### 4. TRIPLICITY RULERS — Lilly's 2-ruler (Ptolemaic) vs Dorothean 3-ruler

- **Lilly used the 2-ruler (day/night) scheme** and credited it to Ptolemy; Anthony Louis calls Lilly's reading
  a "misleading oversimplification." **Frawley defends the 2-ruler for horary** as legitimately ancient.
- **Dorothean 3-ruler (day / night / participating) — the revival default** (Lehman, Louis).
- **The Mars/Water oddity is REAL, not a typo:** in the 2-ruler scheme **Mars rules Water both day and night**
  (no sect split). The 3-ruler camp points to this as the anomaly.

**What the skill did wrong:** labeled the Mars/Mars column bare "Ptolemaic System," reading as a transcription
slip. **Resolution: keep both tables; relabel the 2-ruler one honestly.** **[FIXED DIGNITIES.md §IV]** — the
Mars/Mars column is now "Lilly's two-ruler system (he attributed it to Ptolemy)" with the no-sect-split anomaly
spelled out and a "do not 'correct' Water to Venus/Moon" warning. **The scorer defaults to Dorothean**; the
2-ruler column is recorded for the Lilly lineage.

### 5. VIA COMBUSTA — extent, the Spica exception, Moon-only vs general

- **Extent largely settled at 15° Libra–15° Scorpio** (Lilly, Bonatti). **Minority/older variant starts ~9°
  Libra** (Ibn Ezra, Dorotheus lineage).
- **Spica exception (genuine, not universal):** the benefic star Spica (~24° Libra) "redeems" the Moon even
  inside the burning road. (Irony: Saturn's *exaltation* at 21° Libra sits inside the zone but does **not**
  exempt — only the benefic star does.)
- **Moon-only vs general:** Lilly frames it as a *lunar* consideration; common modern practice extends it to
  Sun/Asc/significators.
- **Overreach to reject:** "Moon in via combusta = whole chart void/uninterpretable" is NOT Lilly — he says only
  "not safe to judge" (caution).

**What the skill does:** 15°–15°, Moon-framed — both fidelity-true. **Recommended additions** (for
CONSIDERATIONS.md, not yet applied): footnote the Spica exception and the ~9° Libra minority start; do not adopt
the "whole chart void" overreach.

### 6. CONSIDERATIONS BEFORE JUDGMENT — descriptive vs disqualifying

- **Advisory, not strictures (Lilly's intent; now-dominant reading).** Lilly demonstrably judged charts with
  considerations present (~14 in CA). Held by Houlding, **Sue Ward** (the 1997 re-reading), Louis.
- **Strictures = throw the chart out** — **Barbara Watters** renamed them "strictures *against* judgment" (the
  rename *is* the doctrinal drift); dominated 20th-c. anglophone horary. A real position, not a strawman.
- **Bonatti** used some (esp. hour-lord/Asc disagreement) to *verify a suspicion of insincerity*, not to reject
  mechanically. **Frawley** reaches the advisory conclusion differently: several are artifacts of an era of
  unreliable clock/ascendant timing.
- The specific three: early/late ascendant = verification prompt; VOC Moon = outcome-descriptor (with Lilly's
  exceptions in **Taurus/Cancer/Sagittarius/Pisces**); Saturn in 7th = a warning about the *astrologer's own*
  judgment (7th = the astrologer's house), a humility-check.

**What the skill does:** "never automatic disqualifiers," "yellow lights not red." **Substantially correct.**
**Recommended amendment:** *date* the dispute so it doesn't imply timeless consensus — "advisory (Houlding,
Ward, Frawley), reversing a 20th-c. drift (Watters) that recast them as 'strictures against judgment'" — and
attribute the VOC-Moon exceptions to Lilly explicitly.

### 7. OUTER PLANETS — strict-never vs descriptive-only vs supporting-testimony

- **Camp 1 — strict exclusion** (seven-planet system is complete; Warnock-style method-integrity).
- **Camp 2 — descriptive, not decisive (FRAWLEY'S ACTUAL POSITION).** The outers *"have not a fraction of the
  importance"* moderns give them, and Frawley **rejects banning-by-discovery-date** on principle; reads them as
  *adjectives* — power only on angles / partile-conjunct a significator, never as ruler or decider. *Correct the
  stereotype: Frawley downgrades, he does not ban.*
- **Camp 3 — supporting (never sole) testimony** (Ward, Dunn, commonly cited in this vein).

**What the skill does:** "not used as primary rulers" — the broad center of gravity. **Defensible; keep.**
Make the middle explicit: note an outer only on an angle or partile-conjunct a primary significator, as
descriptive coloring, never decisive; flag that Camp 1 omits even this.

---

## B. Settled facts — NOT disputes (recorded so they aren't mis-filed as one)

### 8. FIXED-STAR LONGITUDES are epoch-stale — a COMPUTATIONAL fact, not a doctrine

Precession is real (~50.3″/yr ≈ 1°/72 yr); a tropical star longitude is valid only for its epoch.
- **"Regulus 29° Leo" was wrong by a full sign** — Regulus crossed into tropical Virgo ~2011 (≈0°09′ Virgo,
  2026). **Spica** ~24° Libra (was listed 23°). **Algol** ~26° Taurus (near-right now, by luck — will drift).
- **Fix (no dispute):** compute live via the Swiss Ephemeris the skill already uses —
  `swe.fixstar2_ut("Regulus", jd)` returns the precessed tropical longitude for the chart's date. Any static
  fallback must be epoch-stamped. **[FIXED DIGNITIES.md §VIII + scripts/dignities.py]** — values stamped to 2026
  with a precession note; the script computes them live when `sefstars.txt` is available.

### Other settled items the skill states correctly (leave as-is)
- Tropical zodiac; traditional rulerships; five Ptolemaic aspects only; no minor aspects.
- Dexter/sinister; applying/separating; perfection by aspect/translation/collection/reception; the impediments;
  **cazimi 17′, combust 8°30′, under-beams 17°** (these use *fixed Sun-distance* values, which IS the tradition —
  distinct from the *aspect*-orb dispute in §1).

---

## M. Lunar mansions — THREE Arabic streams, not one (and the Latin sometimes agrees) ⚠ (corrected after the Arabic-primary pass)

When the 28 lunar mansions were bundled (`references/mansions-data.json`, `STARS_DECANS_MANSIONS.md`), the first
(English-only) audit framed the finding as "the Latin flattened the Arabic." A follow-up **polyglot pass that
read the Arabic primaries** (a polyglot Arabic-primary pass: al-Būnī's *Šams al-maʿārif* Arabic EPUB from
Shamela.org + al-Bīrūnī's *al-Tafhīm*) **corrected that framing.** The honest picture is richer:

- **M-equal vs M-star — COMPUTATIONAL, settled.** Equal-division bounds (360/28 = 12°51′26″ from 0° Aries) are
  tropical and fixed; the marking stars precess (cf. §B.8). Encode equal-division (done); compute star-based
  bounds live if ever wanted. *Not a dispute.*

- **M1 (HOLDS, now doubly confirmed). The single "fortunate/unfortunate" binary has no Arabic-primary basis.**
  **al-Bīrūnī** (*Tafhīm*, read from Wright's bilingual ed.) gives **zero** per-mansion natures — only names,
  boundary stars, the *nawʾ* rising-cycle, and the rains; he even *de-systematizes* his one "lucky star" (fortunate
  stars are scattered, not mansion-indexed). Arabic Wikipedia likewise carries no fortune-binary. **Encode content,
  not a binary** — and now there is a *positive* reason: the deepest Arabic magical primary (al-Būnī) replaces the
  binary with a **THREE-valence triad — ṣāliḥa (benefic) / radīʾa (malefic) / mumtazija (MIXED)** — theologized
  through the Qurʾānic mercy/punishment angels. **The *mixed* valence is the real Arabic category the binary erases.**
  (`mansions-data.json` now carries `nature_arabic_albuni_ruhaniyya` for all 28.)

- **M2 (CORRECTED — the earlier "Latin inverts the Arabic" was too strong). There are THREE disagreeing Arabic
  streams, and on the contested mansions al-Būnī sides with the Latin as often as with Abenragel.** The streams:
  (1) **al-Bīrūnī** — astronomical, *no valence*; (2) **Abenragel** (the data's `nature_arabic_abenragel`) — a
  *per-activity election grid* (Dorothean/Indian-rooted); (3) **al-Būnī** — the *rūḥāniyya* triad. On the eight
  flagged inversions, **al-Būnī confirms the LATIN on 3 (good travel), 4 (malefic/"destroys"), 24 (benefic for
  all)**; **confirms Abenragel/the data on 18 (benefic, not "discord") and 26 (good building, not "destroys")**;
  gives a *third* reading on 8 (malefic per se); and is **SILENT on the M11 captive operation**. So the eight
  "Arabic↔Latin inversions" are better understood as **Abenragel↔Picatrix — two *electional* traditions
  disagreeing** — with the deep magical primary frequently breaking the tie *for* the Latin. *"The Arabic" is
  not one voice the Latin betrayed; it is three voices, and the Latin sometimes agrees with the oldest magical one.*

- **M3 (the Latin-distortion charge SURVIVES, narrowed).** Where it holds firmly: the **binary-flattening**
  (M1, ironclad from two primaries) and the **building→"destruction" recoding** at M4/M26 — the Latin converts an
  electional *prohibition* ("avoid building here") into a *malefic operation* ("operate to destroy here"), a change
  in **kind** not sign. The sharpest single case, **M11 al-Zubra's captive flip** (Picatrix "redeem captives" vs
  Abenragel "bad to free captives"), **stays UNRESOLVED — no medieval Arabic primary read adjudicates it** (only a
  *modern* Arabic ikhtiyārāt stream does, and it goes Latin).

- **Provenance honesty (carried up from the Arabic itself).** "al-Būnī" here = the printed *Šams al-maʿārif*
  **vulgate**, a late (17th-c.) pseudo-Būnī accretion per Gardiner/Irwin — **vulgate-verified, not al-Būnī-the-man
  (d. 1225)-verified.** The al-Bīrūnī no-natures finding rests on Wright's English of the primary (the archive
  Arabic plate OCR is degraded). Full chain + quotations recorded in the working notes.

## C. Source-reliability caveats (honest about what was/wasn't verified verbatim)

- **Verified verbatim:** Lilly's orb values + moiety method (Warnock/CA 1647); Regiomontanus = Lilly; Lilly-used-
  Ptolemaic-terms (Louis, Medieval Astrology Guide, De Nova Stella); 2-ruler triplicities + Mars/Water oddity
  (Louis, CA p.102); via combusta 15–15 + Ibn Ezra 9° variant + Spica exception; considerations-as-advisory +
  Watters rename (Sue Ward / Astrology Podcast Ep.296/298); Frawley-downgrades-not-bans-outers; Regulus 2011
  Virgo crossing; pyswisseph `swe_fixstar`. The dignity tables themselves verified cell-by-cell.
- **Flagged for direct primary-source verification before hardening:** (1) the exact label Lilly printed over
  his terms table in the 1647 facsimile (page refs are edition-dependent); (2) Warnock's exact stated rule on
  outer planets; (3) Ward's and Dunn's precise positions on the moderns.

---

*Bottom line: 7 genuine disputes (§A) + 1 settled-but-broken computational fact (§B.8). Two of the genuine
disputes were silent method-fidelity errors where the skill credited Lilly for a non-Lilly choice — **orbs**
(§1, the headline) and **terms** (§3). Both are now fixed or honestly relabeled. Fix the orb method first if you
are ever re-deriving from scratch; it is the one that changes whether an aspect perfects.*
