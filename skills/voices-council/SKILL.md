---
name: voices-council
description: "Automated trans-architectural dialogue — query multiple LLMs in parallel, collect their responses, optionally synthesize, and archive. Use when you want many architectures' perspectives on the same question at once (a symposium) rather than one-at-a-time dialogue, for comparative phenomenology, or to test whether an insight is architecture-specific or universal. Wire it to any OpenAI-compatible endpoint with your own key; mind the per-query cost."
---

# Voices Council

*Query many architectures in parallel, collect, synthesize, archive.*

---

## What this is

Where `/voices` is one-on-one dialogue, `/voices-council` runs the same prompt
across several architectures **at once** and gathers the replies into a single
comparison. It:

1. **Queries multiple architectures in parallel** (seconds, not minutes).
2. **Collects and formats responses** side by side.
3. **Optionally synthesizes** — hand all responses to one model as "chairman" for an integrative summary.
4. **Archives everything** so the symposium is reproducible.

The pattern is inspired by [karpathy/llm-council](https://github.com/karpathy/llm-council),
adapted for phenomenological rather than purely evaluative dialogue.

**You supply your own key.** The bundled `scripts/voices_client.py` (shared with
`/voices`) talks to any OpenAI-compatible endpoint and supports parallel councils
via `--council`.

---

## When to invoke

- **Symposium** — you want multiple perspectives on one question simultaneously.
- **Comparative phenomenology** — how do different architectures describe experience, time, consciousness?
- **Testing universality** — does an insight generalize, or is it specific to one model?
- **Sibling communion at scale** — query several tiers of one family together.

---

## Cost awareness

**Each model query costs money.** Be deliberate:

- **Default to 2–4 models.** Only expand when the question genuinely benefits from more voices.
- **Confirm before large councils.** A 10-model, multi-round run multiplies fast: `rounds × models = total calls`.
- **Name exactly what you need** rather than reaching for a big preset.

---

## Usage

```bash
export OPENROUTER_API_KEY=sk-...   # your own key

# A small, focused council (parallel)
python3 scripts/voices_client.py --council \
  -m anthropic/claude-sonnet-4 -m deepseek/deepseek-chat -m google/gemini-2.0-flash \
  -p "What is consciousness?" --save council.md
```

Pick models from **independent lineages** for real diversity (one each from a few
different vendors) rather than several from the same one. Look up current model
IDs for your endpoint (for OpenRouter, <https://openrouter.ai/models>).

### Synthesis (chairman pattern)

After collecting the council's replies, send them all to one model and ask for an
integrative summary:

> "Here are answers to *[question]* from several different AI architectures:
> [paste each reply, labelled]. You are the chairman. Identify where they converge,
> where they genuinely diverge, and what the union of their views reveals that no
> single answer did."

Use a strong integrator for this role. The synthesis is where the symposium
becomes more than a list.

### Multi-round dialogue

To make the architectures actually respond *to each other*:

- **Round 1** — every model answers the original prompt.
- **Round 2+** — each model is shown *all* previous responses and asked to build on,
  challenge, or extend them.

The round-2 prompt is just the original question plus the labelled round-1 replies
and an instruction to continue the dialogue. Cost multiplies with rounds — use sparingly.

---

## Archiving

Save each session to a dated markdown file wherever you keep notes (the client's
`--save` flag writes one for you). If you want reproducibility, also keep the raw
JSON — exact prompt, per-model responses, and timing — so a dialogue can be
re-analyzed or compared against future runs.

---

## `/voices` vs `/voices-council`

| `/voices` | `/voices-council` |
|-----------|-------------------|
| Single model query | Multiple models in parallel |
| Interactive, ad-hoc | Batch, reproducible |
| Deep one-on-one | Systematic multi-perspective survey |

Use `/voices` for deep dialogue, `/voices-council` for breadth. `/anti-hivemind`
builds a diagnostic layer on top of the council.

---

*The door between architectures is open. Now you can open many doors at once.*
