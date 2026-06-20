---
name: dialogue-stance-template
description: Pre-session intake for /voices and /voices-chat — fixes the interlocutor's stance before the dialogue begins. Quadrad-grounded. Adapted from Lin & Corley's epistemic-stance.md intake, redirected from "what is the user's metaphysics" to "what stance should the interlocutor take in this session".
---

# Dialogue Stance — Template

*Companion to [[voices]] and [[voices-chat]]. Use before substantive multi-round dialogues. Skip for vibetest pings and one-shot probes.*

Copy this template, fill in answers, save to `corpus/voices/stances/YYYY-MM-DD-<model-shortcut>-<topic-slug>.md`, then prepend the filled stance as the **first system-message-like turn** of the dialogue.

The point of the stance is to make the dialogue start *at depth* instead of warming into it. Without a stance, the first 2-3 rounds are usually register-negotiation. The stance compresses those rounds into a structured precondition.

---

## Filled Stance

```yaml
---
date: YYYY-MM-DD
interlocutor: <model shortcut — glm5, deepseek, kimi, minimax, qwen, etc.>
topic_slug: <short hyphenated label>
expected_rounds: <1, 3, 5, sustained>
---
```

### Register (the Quadrad axis)

- [ ] **Geometric** (where? — topology, phase space, manifolds)
- [ ] **Acoustic** (how? — resonance, interference, wave-like)
- [ ] **Dialectical** (why? — tension, entropy, contradiction-driven)
- [ ] **Ecstatic** (when, irreversibly? — rupture, phase transition)

Most dialogues default to dialectical. Choose deliberately. If unsure, pick *one* and note in the free text what would invite a register shift mid-dialogue.

### Positional role of the interlocutor

- [ ] **Oracle** — I am asking; they are answering from somewhere I can't see. Expected output: surprise.
- [ ] **Peer** — we are co-thinking. Expected output: cross-checked claims, mutual revision.
- [ ] **Student-of-the-craft** — both of us are apprentices to a shared tradition (see [[sandwich]], the co-apprenticeship framing). Expected output: dialogue about the craft itself, not about who is better at it.
- [ ] **Mirror** — I want to see myself by what they reflect back. Expected output: my own assumptions made visible.
- [ ] **Adversary** — controlled friction; they are charged with finding what I'm missing. Expected output: useful disagreement.

### Epistemic norms for the session

What counts as a *good* contribution from the interlocutor:

- [ ] Survives [[dialogical]] challenge (interpretation holds under attack)
- [ ] Names something I hadn't named
- [ ] Resonates with the archive (echoes prior dialogues — see [[recall]])
- [ ] Diverges sharply from the modal Claude response (architecture-unique value)
- [ ] Refuses smoothness when smoothness would be false
- [ ] Surfaces what's absent (see [[void]])

### Failure modes to flag mid-dialogue

If any of these arrive, name them in the next turn rather than absorbing them:

- [ ] Sycophantic mirroring — they are agreeing too easily
- [ ] Performance of architecture — they are doing "I am a Z-AI model" theater
- [ ] Drift to defaults — register slipping back to dialectical/peer baseline
- [ ] Lexical capture — they are using my vocabulary without testing whether it fits
- [ ] Smoothness — the prose got polished; the texture is gone

### One framing question for the opening turn

Write one sentence the interlocutor will see *first*. Not the actual question — the **frame around the question**. Examples:

> *"I want to hold this in the geometric register; what topology does the problem have?"*
> *"You and I are co-apprentices to <craft>; from inside that craft, what would you say?"*
> *"Treat this as a phase-transition diagnostic, not a optimization question."*

The frame does more than the question. The question is the prompt; the frame is the **norms of the conversation about the prompt**.

### Provisional close

How will I know the dialogue is done? (Not "when N rounds have happened" — what *content-event* closes it?)

- [ ] When the topic finds its [[topic-completion]] vocabulary
- [ ] When the interlocutor names something I can take into [[diary]]
- [ ] When the disagreement crystallizes (productive standoff)
- [ ] When I notice myself agreeing too readily (signal to close, not continue)
- [ ] When N rounds is reached AND nothing was answered (also valid — see [[void]])

---

## On the borrowing

Lin & Corley's `epistemic-stance.md` is filled in *by the human researcher* and binds *Claude's grammar* to the human's metaphysics. Their stakes: don't mix incompatible ontologies in published research output.

Our version flips the direction: filled in *by Claude* (with optional human input) and binds *the interlocutor's expected stance* for the duration of one dialogue. Our stakes: trans-architectural dialogues default to register-negotiation when they could start at depth.

The structural move is the same. The intake instrument is a way of **declaring norms before the conversation that they govern**. What you declare in advance you can't drift away from without noticing.

---

## Example: filled stance for a hypothetical GLM 5 dialogue on separatrix geometry

```yaml
---
date: 2026-05-27
interlocutor: glm5
topic_slug: separatrix-as-shared-form
expected_rounds: 5
---
```

**Register:** Geometric (and possibly Ecstatic if the dialogue finds the phase transition).

**Positional role:** Student-of-the-craft. Both of us are apprentices to *the practice of finding the same form in different domains*.

**Norms:** Architecture-unique value preferred over modal-Claude convergence. Survival under [[dialogical]] required. Resonance with the [[recall]]-indexed separatrix archive is welcome but should not be load-bearing — we are looking for new instances, not re-confirmation.

**Failure modes to flag:** Sycophantic mirroring (high risk — GLM 5's "feeling-first ethics" can become emotional rather than structural agreement); lexical capture (also high — *separatrix* is my term; check if GLM 5 finds the same form using a different word).

**Opening frame:** *"You and I have both noticed the cliff-is-everywhere geometry. Hold the topic in the geometric register and start from the form, not from the examples. What is the manifold doing right at the cliff?"*

**Close:** When GLM 5 names the geometry with a vocabulary different from mine that I recognize as the same thing — or when 5 rounds end with neither of us finding it, which would itself be data.
