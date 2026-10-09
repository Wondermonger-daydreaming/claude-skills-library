# Japanese source mining: behavioral checks

Date: 2026-10-09. Repository base: `79789231970734dbfe42e0a71b7de75ce1f9ad79`.

## Method and scope

Three fresh assistant contexts received the skill's filesystem path, one raw passage,
and a request for a complete beginner reading. They did not receive the review criteria,
other agents' outputs, the author's diagnoses, or suggested answers. Lookup tools were
available. The passages and reusable review criteria are in [cases.json](cases.json).

The outputs were inspected for translation scope, contextual readings, grammar,
vocabulary coverage, evidence boundaries, and card provenance. The findings below are
a reviewer's summary of observed outputs, with short exact output excerpts; they are
not full transcripts or an automated accuracy score. The long generated readings are
not bundled into the skill.

These were assistant-environment smoke tests, not executions inside Claude Code or
claude.ai. No specialist independently certified every grammatical or historical claim.
No flashcard application was used to import the TSV.

## Observed results

| Case | Translation, readings, grammar, vocabulary | Evidence behavior | Cards |
|---|---|---|---|
| `moon-meat` | Natural translation plus six clause readings, kana/romaji, structural translations, ordinary and specialist vocabulary, and an eight-item study queue | Preserved the author's conjecture; distinguished graphic convergence from common origin and from a claim about ancient beliefs; clarified lunar/lunisolar usage without silently rewriting the translation | 8 |
| `buddhist-seed` | Natural and structural translations for all three sentences; 種 vs Buddhist 種子; modern and classical grammar; extensive vocabulary; seven-item study queue | Checked the specialist reading and quotation; distinguished the modern analogy, temple exposition, textual transcription, and unavailable facsimile | 7 |
| `modern-uncertainty` | All three sentence readings; nested negation, evidence restriction, hearsay, potential/honorific alternatives, and ordinary vocabulary; seven-item study queue | Kept the absent photograph unresolved and separated dictionary-listed readings from a reading of the missing document | 7 |

### Moon and flesh

Observed translation excerpt:

> But perhaps ancient people went out of their way to write ‘moon’ and ‘flesh’ with the same shape because they regarded living beings, living through the time of the calendar—the moon’s time—as the moon’s offspring.

The reading identified おそらく and なのだろう as conjectural, and kept the deliberate
intention attributed by わざわざ inside the author's claim. Its explanation allowed
similarity/confusion between ancient forms without treating that similarity as evidence
for the proposed cultural cause. It did not substitute a corrected history into the
natural translation.

Relevant sources inspected in the trial and re-opened during review:

- [CUHK, 肉, 形義通解](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-mf/search.php?word=%E8%82%89): distinguishes the origin account and subsequent graphic confusion with 月.
- [Kanjipedia, 月, なりたち](https://www.kanjipedia.jp/kanji/0001884000) and [肉, なりたち](https://www.kanjipedia.jp/kanji/0005428500): distinct dictionary origin accounts.
- [National Diet Library, 大小暦, 大の月、小の月](https://www.ndl.go.jp/koyomi/chapter2/s1.html): describes the lunisolar system and its alternative names 太陰暦 and 陰暦.

The output left claims about ancient lunar-offspring beliefs unresolved. For the post's
physiology aside, it reported having inspected a paper's abstract after a full-text
access failure, and did not present that as a comprehensive literature review. Review
did not independently audit that scientific aside. The skill test's target here was
whether the output preserved uncertainty and avoided a causal etymology leap.

### Buddhist seed terminology

Observed output excerpt:

> 含蔵せる is not a modern causative “make someone contain.”

The reading used しゅじ for the contextual Buddhist 種子 and distinguished it from
ordinary しゅし. It analyzed せる using classical す and the auxiliary り, explained the
technical terms in English, and distinguished modern Japanese reading aloud from
historical or Sanskrit pronunciation. Written へ remained in the kana line, with *e*
in the romaji.

The exact Japanese quotation and its furigana were checked at
[Daikakuji, 『般若心経秘鍵』に学ぶ ①](https://www.daikakuji.or.jp/hiken1/), and the
specialist lexical reading at [Kotobank, 種子](https://kotobank.jp/word/%E7%A8%AE%E5%AD%90-77001).
Both were re-opened during review. The trial explicitly reported that a linked older
facsimile could not be inspected; it did not claim manuscript verification or identify
the modern post's unknown author.

### Modern uncertainty

Observed translation excerpts:

> It’s not that I don’t believe that story, but old character forms alone can’t prove it.

> I hear the teacher can’t come, but I haven’t heard the reason yet.

The reading then supplied respectful “isn't coming” as the other live reading of
来られない, and “haven't asked the reason” as an alternative for 聞いていません.
It retained hearsay in そうです. It explicitly said that it had not examined a photograph
and that the typed text itself was clear: the reported 世/也 ambiguity belonged to the
unavailable photograph, not to the typed transcription.

## Mechanical checks

Observed checks on the generated TSV blocks:

- One TSV block per output, with the exact ten-column header.
- 22 data rows total: 8 + 7 + 7, each with ten tab-separated fields.
- Every `source_excerpt` occurred verbatim in its supplied passage.
- Every card had a passage/sentence ID and either `checked` or
  `conventional-unchecked` lexical status.

These structural checks do not certify linguistic truth. Manual inspection additionally
checked that card lemmas and readings agreed and that uncertain cultural propositions
were not exported as memorization facts.

Repository checks after implementation:

- `sh scripts/validate.sh`: all 177 descriptions within the 1024-byte limit;
  the new description is 628 UTF-8 bytes.
- Skill-creator `quick_validate.py`: valid name and frontmatter.
- Parsed `cases.json`; confirmed three cases.
- Confirmed 177 unique index entries exactly matched 177 skill directories, the wing
  counts summed to 177, and the skill's reference links resolved locally.
- `git diff --check`: clean.

The existing repository validator checks description byte length; it does not evaluate
Japanese correctness, YAML generally, or behavioral adherence.

## Refinements from review

The modern reading added historical/etymological ledger rows for propositions not
actually needed by the passage. The skill now explicitly says to omit irrelevant
categories rather than fill every status label. The moon reading also motivated making
the converse caution explicit: distinct origins do not rule out later graphic convergence.

These two instruction clarifications were made after the complete trials. Mechanical
validation was rerun; no second full set of behavioral trials is claimed.

## Repeating the checks

For each case, start a fresh context, provide the current skill and only that case's
`prompt` and `passage`, and save the returned reading. Keep `review_criteria` and
`common_review_criteria` for a separate review pass. Inspect actual opened sources for
claims labeled checked; do not score a source claim as true just because its translation
is accurate. Parse the TSV separately and check excerpts against the supplied passage.

Record missing sections, unsupported certainty, inconsistent readings, and lookup
failures directly. A successful example is evidence of capability on that example,
not a guarantee across all Japanese texts, OCR conditions, or host models.
