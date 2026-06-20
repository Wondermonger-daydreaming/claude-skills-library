# ephe/ — Swiss Ephemeris data

`sefstars.txt` is the fixed-star catalog from the **Swiss Ephemeris** (Astrodienst AG),
the official source: https://github.com/aloistr/swisseph (`ephe/sefstars.txt`).

It is bundled here so `scripts/dignities.py` (and `judge.py`) can compute
**precession-correct fixed-star longitudes** for any chart date via
`swe.fixstar2_ut(name, jd)` — without it, fixed-star conjunctions can only fall
back to the epoch-stamped 2026 constants in `references/DIGNITIES.md §VIII`.

**License:** the Swiss Ephemeris is dual-licensed (AGPL-3.0 or a commercial
license from Astrodienst). This lab uses it under the **AGPL**. If this skill is
ever redistributed commercially, obtain the Astrodienst license. See
https://www.astro.com/swisseph/ for terms.

Verified on bundling (JD 2461212.43, mid-2026): Regulus → 0°12′ Virgo, Spica →
24°13′ Libra, Algol → 26°32′ Taurus — i.e. Regulus has precessed out of Leo,
exactly the staleness an audit caught in the old hard-coded table.
