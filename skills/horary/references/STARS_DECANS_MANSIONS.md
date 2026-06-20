# Fixed Stars, Decans, and Lunar Mansions

*The three star-anchored layers beyond the planets. All three are now **computable** —
`scripts/stars.py` (decans + mansions, pure Python from the JSON data files) and
`scripts/dignities.py` (live fixed-star longitudes via the bundled Swiss Ephemeris).*

The coherence worth seeing: **all three are star-anchored.** Decans began as 36 rising
star-groups; lunar mansions are each marked by a fixed star; and fixed stars themselves
precess. So `ephe/sefstars.txt` underpins the whole layer — it gives the precessed star
positions, and the same precession is *why* the decan stars and mansion stars drift while
the tropical 10°-thirds and 12.857°-mansions stay put.

---

## I. Fixed Stars

A handful of stars add strong testimony when a significator sits within ~5° (Lilly): the
royal **Regulus** (+6), benefic **Spica** (+5), malefic **Algol** (−5), and others.

**They precess (~1°/72 yr), so never freeze their longitudes.** A primary-source audit caught
the old table claiming "Regulus 29° Leo" — but Regulus crossed into Virgo c. 2011.

- **Live computation:** `python scripts/dignities.py --fixstar Regulus <jd>` or
  `scripts/stars.py --star Regulus <jd>` → the precessed tropical longitude for that date,
  from `ephe/sefstars.txt` (the official Swiss Ephemeris catalog, now bundled).
- **Fallback constants** (epoch-stamped 2026) live in `DIGNITIES.md §VIII` with the
  precession note. Verified live: Regulus 0°12′ Virgo, Spica 24°13′ Libra, Algol 26°32′ Taurus.

## II. Decans (Faces)

The 36 ten-degree thirds of the zodiac. Two things to keep separate:

- **The planetary ruler** = the **Chaldean face ruler** (Mars at 0° Aries, descending
  Chaldean order) — already the horary "face" (+1 dignity), in `DIGNITIES.md §VI` and
  computed by `dignities.face_ruler` / `stars.decan(...)["ruler_chaldean_face"]`.
- **The decan's deeper identity** — a stack of traditions, in `references/decans-data.json`
  (36 decans × 20 attribute layers, from a multi-tradition *Decans Table* compilation): **Liber Hermetis**
  names + image-descriptions; the **Sacred Book of Hermes to Asclepius** names, descriptions,
  governed body-parts, **stones** and **plants**; the **Ptolemaic / Ostanes / Firmicus
  Maternus decan-gods**; the **Testament of Solomon** decan-spirits with their **invocations**
  and **thwarting angels**. (Picatrix / Hygromanteia / PGM columns exist as placeholders.)

**Decans do NOT precess** in this use — the 10° thirds are fixed to the tropical zodiac.
(The *original Egyptian decan stars* precess, but the dignity/talismanic division does not.)

**Numbering caveat:** the data follows the **Liber Hermetis order, beginning at Cancer**
(decan #1 = Cancer 1, the Thema-Mundi convention), not at Aries. Lookups key off the
*sign + third* ("Aries 2"), so the ordering is transparent to callers.

`python scripts/stars.py --decan 13.68` → "Aries 2", Chaldean ruler Sun, Liber Hermetis
"Sabaoth", and the full attribute stack.

## III. Lunar Mansions (manāzil al-qamar, منازل القمر)

The 28 stations of the Moon. **Two systems, never to be conflated:**

- **Equal-division** (the encoded default): 360 ÷ 28 = **12°51′26″** per mansion from **0°
  Aries**. Tropical, **fixed, non-precessing**. This is the Picatrix/Agrippa system.
- **Star-based:** each mansion anchored to a marking star (al-Sharaṭayn ≈ β/γ Arietis,
  al-Qalb = Antares, al-Jabha = Regulus …). These stars **precess**, so star-based bounds
  drift and are epoch-bound. al-Bīrūnī lists the mansions by their boundary stars.

Data in `references/mansions-data.json`: number, **Arabic name + meaning**, the **Latin
(Picatrix/Agrippa) name kept visible as a corruption** (Azobra ← al-Zubra, Athoray ←
al-Thurayyā …), equal-division bounds, the precessing marking star, and **dual natures** —
Latin (Picatrix/Agrippa) beside Arabic (Abenragel) — with the Arabic↔Latin **delta** flagged.

`python scripts/stars.py --mansion 130` → Mansion 11, al-Zubra (the mane), marked by Zosma.

**⚠ Three Arabic streams, not one — see `DISPUTED.md §M`.** The single "fortunate/
unfortunate" binary has *no* Arabic-primary basis (al-Bīrūnī gives no valence at all), and
the deepest Arabic magical primary, **al-Būnī's *Šams al-maʿārif*** (now read in Arabic),
replaces it with a **three-valence triad** — benefic / malefic / **mixed** (the *mixed* term
is the real category the binary erases). The `mansions-data.json` carries **three** nature
columns now: `nature_latin_picatrix_agrippa`, `nature_arabic_abenragel`, and
`nature_arabic_albuni_ruhaniyya`. The earlier "the Latin flattened the Arabic" framing was
**corrected**: on the eight contested mansions al-Būnī sides *with the Latin* as often as with
Abenragel — so the inversions are really **Abenragel↔Picatrix** (two electional traditions),
not a clean Latin distortion. The Latin-distortion charge survives only for the binary itself
and the building→"destruction" recoding (M4/M26). The captive flip (M11) stays unresolved by
any medieval primary. (al-Būnī = the *Šams al-maʿārif* vulgate, a late pseudo-Būnī text —
vulgate-verified, not al-Būnī-the-man-verified.)

---

## Scripts

| Command | Returns |
|---------|---------|
| `stars.py --decan <lon>` | decan (sign+third), Chaldean ruler, full attribute stack |
| `stars.py --mansion <lon>` | equal-division lunar mansion, Arabic+Latin name, dual natures |
| `stars.py --star <name> <jd>` | precessed tropical longitude of a fixed star |
| `stars.py --test` | self-check (36 decans + 28 mansions; rulers match `dignities.face_ruler`) |
| `dignities.py --fixstar <name> <jd>` | same star computation, from the dignity engine |

*Data: `references/decans-data.json`, `references/mansions-data.json`, `scripts/ephe/sefstars.txt`.*
