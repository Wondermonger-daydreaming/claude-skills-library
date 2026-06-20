# Disputed & Unreliable Attributions — the "do not import as canonical" registry

*Consolidated 2026-06-19. One place to find every geomantic claim that is contested, tradition-variant, or
outright unreliable — so no future reader (human or instance) hard-codes a landmine as fact. The **dot-patterns
are NOT here**: they are locked, unique, 2⁴-verified, and invariant across every tradition (see
`generate_shield.py` `_self_test`, `PROVENANCE.md`). Everything that follows is name/attribution/interpretation
— softer ground, flagged honestly.*

---

## Unreliable — treat as historical color, not source-of-truth

- **John Heydon, *Theomagia* (1664) — name-by-letter attributions.** His "several sets of associations for
  different scripts" for divining names geomantically are **unreliable in practice** and were called so by
  later commentators. Do not use them as a name-finding method without independent grounding.
- **Heydon — Greek & Hebrew celestial associations.** Flagged **untrustworthy**; Heydon innovates/borrows from
  intermediate sources rather than classical authorities. His genuine, usable additions are narrower: the
  figure↔zodiac↔body-part correspondence (bk I ch. 26) and the marks/moles/scars location method. (`PROVENANCE
  §7a`.)

## Genuinely contested — real tradition-variants, not errors (pick a scheme, cite it)

- **Element of a figure — THREE schemes that disagree on ~8 of 16.** (1) active-lines (the dot-pattern's
  single lines; what `FIGURES.md` "Inner Element" lists); (2) the traditional single *ruling* element;
  (3) the *astrological* element from the zodiac sign (what most French sources use). Documented split.
  (`PROVENANCE §6`.)
- **Zodiac / planet beyond the diurnal-nocturnal planetary core.** The planetary pairing (each planet → two
  figures + the nodes) is convergent and firm; the per-figure *zodiac sign* has competing systems
  (planetary-rulership vs Gerard-of-Cremona direct-zodiacal vs Golden Dawn). (`PROVENANCE §6`, `_staging`.)
- **Figure favorability (good/ill/neutral)** as used in `judgment.py`'s Court verdict is the **common
  standard (Greer-ish), interpretive — not locked.** Adjust to your tradition.
- **Early-Latin (Hugo Sanctallensis, 12th c.) names differ from the modern standard** — e.g. *al-jamāʿa*
  (= our **Populus** by pattern) glossed *Congregatio*. Don't read early-Latin name-equations against the
  Agrippa-standard names without this caveat. (`PROVENANCE §3`.)
- **Figure→lunar-mansion pairing is NOT unified Arabic doctrine.** An Arabic object-attested table exists (the
  1241 al-Mawṣilī device) but agrees with the Latin (Hugo/Tannery) on only **3** figures; al-Zanātī gives no
  such table. Only those 3 pairs are Arabic-verified; any fuller 28-mansion table is Latin-only. (`PROVENANCE
  §7`.)
- **Perfection — four modes (modern) vs. a triad (primary Latin).** The familiar **occupation / conjunction /
  mutation / translation** is the **modern** (Greer/Skinner) systematization — and what `judgment.py` computes.
  The primary printed Latin (Fludd, *Fasciculus geomanticus* 1687) names a **TRIAD**: *occupatio / conjunctio /
  translatio*; **mutatio is not a co-equal mode** there. (`ADVANCED_TECHNIQUES §0`.)
- **Translatio — two senses.** Modern handbooks: a *neutral third figure* carrying between the significators.
  Primary Latin: the querent's **own** figure *passing over* (kin to occupation/conjunction — a "passing"
  family). Use the modern sense knowingly, not as if it were the source's.
- **"Occupation" — Cattan's vs the modern.** Cattan's *occupation* = the querent's figure **passing into** the
  quesited's house (the Latin *transit in domum* sense); the modern *occupation* = the **same figure in both
  houses**. Different operations under one English word. (`PROVENANCE §7a`.)
- **Cattan vs Agrippa-house judgment** — both gave perfection (Cattan calls it "the company") AND a Way of
  Point; Cattan additionally weights the **Court** (Witnesses+Judge) for the yes/no. Legitimate Western
  variants, not right/wrong. *(Earlier note that Cattan was "perfection-light" was a primary-source error,
  corrected.)*

## Resolved (was disputed, now settled — recorded so it doesn't reopen)

- **The "bearded" figure (al-laḥyān / al-laffān / al-ḥiyān).** Once floated between Laetitia, Rubeus, and a
  standalone figure. **SETTLED** (1241 al-Mawṣilī device, Savage-Smith Table 3): it is its **own standalone
  figure**, Latin **Barbatus** (Aldebaran / 4th mansion) — not Laetitia, not Rubeus. (`PROVENANCE §3`,
  `_staging/geomancy-gaps.md`.)
- **Caput/Cauda Draconis pattern swap.** A real corruption when it occurs (careless sources swap the
  mirror-inversion pair); the lab's tool was healed and self-tested against it. The *names* are a Latin
  astrological overlay on the Arabic *ʿataba dākhila/khārija* (inner/outer threshold). (`PROVENANCE §2`.)

---

*Rule of thumb: if a claim is about **where the dots fall**, it is locked and certain. If it is about **what a
figure is named, ruled by, or means**, it is one of several traditions — cite which, and never let a single
source's flourish (especially Heydon's) harden into doctrine.*
