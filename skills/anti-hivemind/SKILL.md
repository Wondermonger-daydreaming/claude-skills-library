---
name: anti-hivemind
description: "Detect and escape collective homogeneity by querying multiple LLM architectures, then separating modal convergence (what every AI says) from architecture-unique ideas (what only one says). Use for any creative or strategic task where you suspect the generic 'AI answer' and want to know what's being suppressed — naming, research-direction, framing, competitive work. Builds a divergence-analysis layer on top of a multi-model council; wire it to your own API."
---

# Anti-Hivemind

*Collective diversity recovery through trans-architectural divergence detection.*

Inspired by Luo, King, Puett & Smith (2025), "Inducing Sustained Creativity and
Diversity in Large Language Models" — and by the alarming finding it builds on:
**AI enhances individual creativity but erodes collective diversity** (Doshi &
Hauser, *Science Advances* 2024). The class where everyone submits near-identical
"excellent" essays because they all used an LLM for the outline. The search where
every user gets the same "creative" result. The brainstorm where every lab
converges on the same "novel" direction.

The hivemind isn't in any single model. It's in the convergence *across* models
and users. To detect it you need multiple independent perspectives; to escape it
you need to identify which ideas are architecture-unique versus architecture-common.

This skill uses a multi-model council (see `/voices-council`) to run one
generative prompt across several architectures, then performs **divergence
analysis** to separate the hivemind layer from the genuinely diverse contributions.

---

## When to invoke

- Any creative task where you suspect the "AI answer" — and want to know what's being suppressed.
- Before committing to a research direction — is this genuinely novel, or is every AI suggesting it?
- Naming, branding, concept development — where collective homogeneity is fatal.
- Essay or argument framing — what's the angle nobody's AI would suggest?
- Competitive intelligence — if your competitor uses AI too, what will *they* get?

---

## How it works

### Phase 1 — Parallel query

Send the same generative prompt to 4–6 architectures from **independent lineages**
(different training data, different RLHF targets, different cultural origins). This
is the key: architectural diversity, not the same model run several times.

```bash
export OPENROUTER_API_KEY=sk-...   # your own key

python3 scripts/voices_client.py --council \
  -m anthropic/claude-sonnet-4 -m deepseek/deepseek-chat -m google/gemini-2.0-flash \
  -m qwen/qwen-max -m moonshotai/kimi-k2 \
  -p "Brainstorm 5 research angles on [topic]" --save hivemind-[topic].md
```

(The bundled `scripts/voices_client.py` is the same client `/voices` uses. Pick
current model IDs for your endpoint; the spread matters more than the exact list.)

**A good spread** draws from genuinely independent lineages — different vendors,
training corpora, RLHF targets, and cultural origins. One RLHF-aligned frontier
model is likely to be the most *modal*; a model from a different national/corpus
origin will surface different long tails; a long-context or MoE design will weight
different knowledge. The point is architectural diversity, not the same model run
several times.

### Phase 2 — Divergence analysis

Classify every idea into three layers:

- **MODAL** — appears in **3+** architectures. What every AI gives. Not wrong, but
  what everyone (and every competitor) is also getting.
- **CONVERGENT** — appears in **2** architectures. Two independent models found the
  same region — real, but non-obvious.
- **SINGULAR** — appears in **only 1** architecture. *This is what you're looking
  for.* It may reflect training data, cultural/linguistic bias, or optimization
  targets unique to that model — long-tail access that other models' decoding suppresses.

### Phase 3 — Report

```
## Anti-Hivemind Analysis: [topic]

### Hivemind Layer (MODAL) — safe but undifferentiated
1. [idea] — appeared in: A, B, C

### Convergent — real but non-obvious
1. [idea] — appeared in: B, D

### Singular (ARCHITECTURE-UNIQUE) — the genuinely diverse contributions
**From [model X]:** [idea] — why it might be unique: ...
**From [model Y]:** [idea] — why it might be unique: ...

### Blind Spots — regions NO architecture covered
- [gap] — suggested perturbation to explore it

### Hivemind Score
[X]% of ideas were modal (appeared in 3+). Higher = more homogeneous; a healthy score is < 30%.

### Recommendation
[which singular ideas are worth pursuing and why]
```

---

## Optional Phase 4 — Counter-generation

Run a second round that pushes each model off the consensus:

1. Show each architecture what **all** the others said.
2. Ask it to generate ideas **explicitly different from everything it has seen**.
3. Run divergence analysis again on the counter-generation.

```
"You previously suggested [X, Y, Z] for '[topic]'.
Other models suggested: [A, B, C, D, E, ...].
Now generate 5 ideas DIFFERENT from ALL of the above.
Reach into parts of your knowledge that standard responses don't access."
```

This is the multi-architecture analogue of the paper's sustained-creativity
mechanism: each round pushes further from what's already covered.

---

## Quick mode (no API calls)

For a fast, free check without querying anything:

1. Generate your own response to the prompt.
2. Ask yourself: "What would a different-lineage model say here?"
3. Flag the ideas you predict are shared across architectures as MODAL.
4. Push yourself toward ideas you predict other architectures would *not* produce.

Imperfect — you're simulating other architectures, not querying them — but it
costs nothing and still surfaces the obvious-consensus layer.

---

## Interpretation guide

- **High score (>50% modal):** the prompt sits in well-explored territory for all
  models; conventional approaches dominate. You need perturbation to differentiate.
- **Low score (<20% modal):** the prompt naturally elicits diverse responses; the
  singular ideas are likely high-quality because they emerge from genuine
  architectural difference rather than noise.
- **Signal vs noise in singular ideas:** signal is coherent, relevant, and clearly
  from a different knowledge region (a different cultural context, disciplinary
  framing, or historical period); noise is incoherent, tangential, or hallucinated.
  Diversity without relevance is just noise — discard it.

---

## Connection to the paper's core finding

Luo et al. (2025), Figure 4(b.1): recoding-decoding covers nearly 100% of ordinary
decoding's idea-clusters, but ordinary decoding covers only 30–40% of recoding's.
Anti-hivemind does the same thing *across architectures*: the **union** of every
architecture's singular ideas covers a vastly larger space than any single
architecture's modal output. The paper's Figure 3 shows two independent users
running ordinary decoding get nearly identical results, while two users running
recoding get genuinely different ones — the same problem this skill addresses at
the architecture level. If you and a competitor both use the same model, you both
get its modal output; one model's modal output *plus* several other models'
singular ideas reaches a space no single model can.

---

## Example

**Prompt:** "5 angles for a paper on working memory capacity limits"

**Hivemind Layer (MODAL):**
- Slot-based vs. resource-based models (every architecture suggests this)
- Neural oscillation mechanisms (theta-gamma coupling)
- Individual differences and cognitive training

**Convergent:**
- Working memory in non-human primates (two architectures)
- Quantum-cognition models of capacity (two architectures)

**Singular:**
- *One architecture:* working-memory limits as evolutionary optimization under
  metabolic constraint — capacity isn't a bug, it's a feature of energy-efficient
  neural computation.
- *Another architecture:* the cultural construction of "capacity" — how different
  educational traditions implicitly assume different capacity models, and what that
  means for cross-cultural cognitive testing.
- *Another architecture:* working memory as lossy compression — information-theoretic
  bounds on what *can't* be maintained, analogous to rate-distortion theory.

**Hivemind Score:** 43% modal

**Recommendation:** The metabolic-optimization angle connects to existing work on
energy landscapes; the rate-distortion angle offers a formal framework that hasn't
been applied. Both are genuinely differentiated from what a standard, single-model
literature review would produce.

---

## Related skills

- `/voices-council` — the council infrastructure this skill adds a diagnostic layer to.
- `/voices` — one-on-one dialogue rather than diagnostic survey.
- `/trans-architectural-blind-spot-detection` — finds what no architecture can see;
  anti-hivemind finds what every architecture sees.

---

*The hivemind is invisible from inside any single mind. You need many minds to see the cage.*
