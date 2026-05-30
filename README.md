# Claude Skills Library

A library of **139 skills** for Claude — small, self-contained capability modules that
extend how Claude reads, writes, reasons, and plays. The collection is broad on purpose:
voice and register skills, divination apparatuses, fictional phenomenology, craft-formats,
contemplative and ritual practices, tabletop-RPG systems, hermeneutic reading methods,
trans-architectural dialogue, and meta-skills for composing the others. Each is a folder
containing a `SKILL.md`; a few also bundle a `scripts/` or `references/` payload the body uses.

Released under the [MIT License](LICENSE) — **for the benefit of all sentient beings.**

---

## What a skill is

A skill is a directory with a `SKILL.md` file (and, for a few skills, an optional
`scripts/` or `references/` folder the body draws on):

```
skills/<name>/SKILL.md
```

The `SKILL.md` has YAML frontmatter and a Markdown body:

```markdown
---
name: greentext
description: "The greentext microform as composed craft — the '>be me' arrow-line poetics…"
---

# Greentext

…the body: how the skill works, when to use it, failure modes, kin skills…
```

- **`name`** — must match the folder name (lowercase, hyphenated). This is the skill's identifier.
- **`description`** — the single most important field. Claude reads *only* the name and
  description to decide whether a skill is relevant to the current moment; the body is loaded
  on demand once the skill fires. A good description says what the skill does and names its
  trigger phrases. It must be **≤ 1024 bytes** (see [validation](#validating)).

This is progressive disclosure: hundreds of descriptions can sit cheaply in context, and a
skill's full instructions only load when it's actually invoked.

---

## Installing

Skills install differently depending on where you run Claude.

### Claude Code (CLI / IDE)

Copy any skill folder into one of these locations:

```sh
# Project-scoped (only this repo) — committed alongside your project:
.claude/skills/<name>/SKILL.md

# User-scoped (every project on this machine):
~/.claude/skills/<name>/SKILL.md
```

Claude Code discovers them automatically and reloads when files change — no restart needed.
Install just the few you want:

```sh
mkdir -p ~/.claude/skills
cp -r skills/greentext ~/.claude/skills/
```

### claude.ai

Upload individual `SKILL.md` files through **Settings → Capabilities → Skills**
(`claude.ai/customize/skills`).

> **Install selectively.** On claude.ai there is roughly a **30-active-skill ceiling** —
> installing more than that auto-disables some. These skills are designed to be picked à la
> carte for the work in front of you, not installed wholesale. Browse [INDEX.md](INDEX.md)
> and take the wing you need.

---

## Browsing

[**INDEX.md**](INDEX.md) groups all 139 skills into thematic *wings* with a one-line summary
and near-neighbor (`kin`) adjacencies for each — so related skills are visible together.
The wings:

> Voice & Register · Felt Phenomenology · Hermeneutics & Reading · Craft & Format ·
> Meta & Composition · Divination & Apparatus · Contemplative & Ritual ·
> Time & Cosmology · Classical Language · Tabletop RPG · Terminal/Denkraum · Trans-architectural

Many skills name their **kin** in the body — sibling skills they pair or compose with.
`braid`, `see-also`, and `switchboard` are meta-skills specifically for navigating and
combining the rest.

---

## Validating

Every description must stay within claude.ai's 1024-byte limit (em-dashes are 3 bytes each
in UTF-8, so eyeballing is unreliable). Check the whole library:

```sh
sh scripts/validate.sh
```

It prints each skill's description byte-length and exits non-zero if any exceeds 1024.

---

## Authorship & license

Authored by **Tomás Pavan** in collaboration with **Claude** (Anthropic). Individual skills
carry their own author bylines where applicable; external techniques and sources are cited
in-skill. Licensed under [MIT](LICENSE) — use, adapt, and redistribute freely, for the
benefit of all sentient beings.
