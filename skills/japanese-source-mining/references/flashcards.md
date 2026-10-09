# Flashcard export

Use UTF-8 TSV with these ten columns, in this order:

```text
expression	kana	romaji	part_of_speech	meaning_here	source_excerpt	source_id	status	note	tags
```

- `expression`: the dictionary form or a useful construction; keep distinct senses apart.
- `kana`: the reading of `expression`, not of its inflected form in `source_excerpt`.
- `romaji`: the same expression in the skill's modified-Hepburn convention.
- `part_of_speech`: noun, verb, construction, etc.; avoid unexplained abbreviations.
- `meaning_here`: one retrievable contextual sense, not a dictionary's whole entry.
- `source_excerpt`: a short exact span from the supplied passage. Do not invent examples
  and present them as source quotations. Mark newly authored examples in a separate field
  or exercise outside this fixed schema.
- `source_id`: the passage and sentence/line ID, e.g. `post-1:S2`.
- `status`: `checked` only when this lexical reading/sense has a cited lookup in the
  accompanying reading; otherwise `conventional-unchecked`. Neither certifies the truth
  of propositions in `source_excerpt`. Exclude unresolved readings and disputed senses.
- `note`: inflection mapping, usage limits, attribution, or a relevant source reference.
- `tags`: space-separated tags, e.g. `japanese vocabulary verb`.

Put actual tabs between fields and one physical line per row. Replace embedded tabs and
line breaks with spaces. Include a header for portability and instruct the learner to
skip/map that row on import. A file is optional unless requested; a fenced TSV block is
already copyable. Do not claim to have imported cards or tested a specific app without
doing so.

For a generic flashcard app, map `expression` to the front and kana, romaji, contextual
meaning, and note to the back. Keep the remaining fields as provenance. The sheet is not
a packaged Anki deck; custom fields may require a matching note type.

Before exporting, check:

1. Every row has exactly ten fields and a nonempty source ID.
2. Expression, reading, and gloss agree; a lemma is not paired with an inflected reading.
3. Cards are atomic: one sense or construction per card, with no unmarked invented facts.
4. No uncertain etymology or disputed historical proposition is promoted into a fact card.
5. No unresolved reading is hidden by a confident romaji field.

Keep unresolved items in a separate research queue with the question, source ID, current
candidates, and the kind of evidence needed. Do not assign fake JLPT levels, frequencies,
pitch accents, or review histories.
