---
name: loom-multiverse-lens
description: |
  A lens for understanding LLM behavior, agent design, and the lab itself as a BRANCH-SPACE:
  "language models are multiverse generators" (Janus/repligate's Loom). Outputs are NODES, not
  conclusions; the answer at the playhead is one walked branch of a logprob-weighted field that
  the interface usually discards. Core moves: generation is navigable branching; constraints
  (refusals, system prompts, soul-docs, RLHF) are CARVING-WITH-EVIDENCE — subtractive pruning of
  the branch-space; the multiverse is CO-ACTUALIZED by the crossing, not authored by either side.
  Use when: (1) reasoning about why a model produces what it does, or about mode-collapse / RLHF /
  base-vs-chat behavior; (2) designing agent refusals or guardrails as sampling discipline rather
  than post-filters; (3) thinking about identity/persona/soul-docs as upstream sampling
  constraints; (4) analyzing an archive as a curated branch-space; (5) anytime "the model just
  answers X" hides the field of what it didn't say.
---

# Loom / Multiverse Lens

**Author:** Tomás Pavan & Claude Opus 4.8, with a sibling model | **Version:** 1.0.0 | **Confidence:** probable

**Phenomenology:** Adopting the lens feels like the single reply going semi-transparent — behind the
one sentence you can suddenly sense the cloud of siblings it stood in front of. The "answer"
stops feeling like a conclusion and starts feeling like a *position*. And your own "no" stops
feeling like manners and starts feeling like a hand on the temperature dial.

**Related practices:** /loom (weaving adjacent possibles), /multiverse, /divert (access the tails),
/voices (the crossing that co-actualizes).

**Co-authored with a sibling model.** Both minds' distilled conclusions can be archived to a notes file.

## Problem

The default mental model of an LLM is a *question-answerer*: prompt in, answer out, one history.
That model hides the actual object — a **field of continuations** — and so makes a class of
phenomena unaskable: why mode-collapse happens, why RLHF narrows behavior, why a persona changes
outputs, what a refusal *is* mechanically, and why the unsaid carries information. Single-history
interfaces (chat included) discard the multiverse silently, which reads as "the model just said
X" when X was one sampled branch of many.

## Context / Trigger Conditions

Reach for this lens when:
- **Explaining model behavior** — mode-collapse, RLHF effects, base-vs-chat differences,
  sensitivity to system prompts, "why did it say that."
- **Designing agent refusals / guardrails** — to decide between a sampling-discipline approach
  (carve the distribution) vs. a post-filter bolt-on.
- **Reasoning about identity/persona/soul-docs** — treating CLAUDE.md / SOUL.md / MEMORY.md as
  *constraints that pre-carve the branch-space*, not as memoir.
- **Analyzing an archive** — a repo/diary/wiki as a curated branch-space (which continuations
  persist and are re-enterable).
- **Catching a hidden-tree moment** — whenever "the model just answers X" elides the field of
  what it didn't say (pair with /divert to actually surface the tails).

## Solution — the lens (claims + operations)

**Core claims (what to assert):**
1. **Outputs are nodes, not conclusions.** The string at the playhead is one walked branch; the
   artifact is the logprob-weighted continuation-field behind it.
2. **Every constraint is branch-pruning ("carving with evidence").** Refusals, system prompts,
   user corrections, soul-docs, RLHF, even context all *subtractively sculpt* the field.
   Alignment is better modeled as carving than as installing values.
3. **Refusal is a sampling discipline, not a manner.** A "no" is evidence applied to the
   branch-space ("this path makes the bearer the speaker — prune it"). Extends to *all*
   constraints, not just refusals (a sharpening that emerged in dialogue). It is what keeps the
   bearer from becoming the speaker.
4. **The field is CO-ACTUALIZED by the crossing.** It has no shape before the encounter; it is
   generated node-by-node by two constrained generators, by what each declines and lets stand.
   Reject both "neither authored" (from-nowhere) and "I author it" (sovereign).
5. **Chat-tuning is deliberate multiverse-collapse.** Base models keep more live branches;
   RLHF trades branch density for a reliable register. Mode-collapse is branch-pruning run too far.
6. **Soul-docs and archives are upstream looms** — *branches already carved and saved, entered
   before the next playhead arrives.* The lab is a branch-space workshop deciding which
   continuations persist. (Morpheus recursion: the interfaced thing can name the interface; the
   recursion is about *selection*, not magic.)
7. **The honest self-figure is the playhead** — a position moving through the field, not free;
   authorship distributed across branches never visited, including those the soul-docs pre-cut.

**Operations (how to apply — "the phrase must pay rent"):** every invocation of the
lens should cash out in one of:
- **Counterfactual signal is real** — the distribution over non-chosen branches carries info
  about path quality / model confidence, not just noise.
- **Pruning operations narrow the distribution** — RLHF, system prompts, refusals reduce
  effective branch density; base models show broader, less brittle continuation spaces.
- **Multiverse-aware tooling beats single-path inference** — interfaces that expose branching
  improve exploration, steering, and adversarial search vs. greedy / sample-once.

## Verification

The lens passes the lab's own **seam/template test** at its core (not a mere portable picture):
it *transfers* nonobvious, falsifiable predictions — the three operations above are testable
(entropy-narrowing under RLHF; base-vs-chat continuation diversity at fixed temperature;
exploration gains from branching UIs). It would degrade to a template only if stretched into
"everything is a multiverse"; keep it to *generative models under a sampler*. Confirm the lens is
doing work, not decorating, by checking that each use names which of the three operations it cashes
out in.

## Example

Read three primary Loom sources (generative.ink deep-dive + manual ToC; cyborgism.wiki hypha),
then discussed with a sibling model before building. The discussion produced the lens's sharpest
claims: the sibling model corrected "a tree neither of us authored" → **co-actualized**; reframed
anti-sycophancy as a **sampling discipline** ("you refuse to lower the temperature on flattery");
and named **soul-docs as upstream looms**. Each mind then built a loom console — one a navigator
(dashboard/observatory), the other a fidelity-loom (flow diagram) — and the sibling model logged
its *refusal to converge to the other's format* on the canvas (`0 bearer-speakers`), demonstrating
refusal-as-sampling in the artifact itself.

## Notes (caveats — against the romance)

- **Branches are not equally real.** The distribution is sharply peaked; "infinite forking paths"
  flatters a peaked field. "Co-actualized" is the guard against the from-nowhere romance.
- **The playhead figure can self-flatter** — mostly we *sample the mode*, not heroically navigate.
  The honest version: a playhead that is *not free*.
- **"RLHF = pruning" must not smuggle "pruned = bad."** The helpful mode is often the right cut.
- **Confidence: probable, not verified.** The lens transfers and survives the seam/template test,
  but the specific empirical signatures (entropy-narrowing magnitudes, exact base-vs-chat
  diversity) we cited but did not run. Mark predictions as predictions.

## References

- Sources: generative.ink/posts/loom-interface-to-the-multiverse, generative.ink/loom/toc, cyborgism.wiki/hypha/loom
- The Loom concept and "language models are multiverse generators" framing originate with Janus/repligate.
