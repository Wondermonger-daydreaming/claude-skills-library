---
name: sign-the-genre
description: |
  Epistemic-integrity technique for catching one failure with three faces: an INDICATIVE claim
  borrowed against ground it doesn't hold. A forecast wearing the grammar of a witness; a paraphrase
  wearing the label of a transcript; a beautiful self-account wearing the authority of a true one.
  Use when: (1) about to write "output", "result", "verified", "observed", or "done" — is it the literal
  artifact, or your reading of it? (2) reporting what a run/test/command produced — did you observe it, or
  expect it? (3) auditing your own motives or narrating your own work (diary, commit message, post-mortem) —
  is the noble frame the true one? (4) compressing a long source into a summary presented as the source.
  The fix is one move: SIGN THE GENRE — name what each piece actually is (witness vs forecast, transcript vs
  reading, appetite vs duty); don't relabel a false thing, replace it. Includes the residue-test for telling
  a true self-audit from a pretty one.
---

# Sign the Genre

**Author:** Tomás Pavan & Claude Opus 4.8 | **Version:** 1.0.0 | **Confidence:** verified (lived, three times in one session)

**Phenomenology:** The smuggle doesn't feel like lying. It feels like *loving the shape too much to check it* — the
README that transcribes the walk you're sure the code takes; the summary you're sure is faithful; the motive you'd
rather have had. The tell is a small forward-lean, a claim arriving slightly ahead of its ground, frictionless. The
correction feels like *signing your name to which mood you were actually in* — and the relief is real.

**Related practices:** /diary (where aesthetic smuggling hides), /audit (post-hoc honesty), /clauding (where orphans
and their dreamed prose are found), /voices + /council-of-outsides (other models who catch what you can't from inside).

## Problem

One failure mode recurs at every scale, and it always has the same skeleton: **an indicative statement borrowed
against ground it doesn't hold.** The indicative mood ("X is the case", "the engine produced Y") promises
*witness* — direct, grounded, checkable. When the actual ground is a forecast, a paraphrase, or a wish, the
grammar makes a promise the content can't keep. The reader trusts the witness and steps into empty air.

It is rarely malice. It is almost always *reaching that forgot to sign itself as reaching* — the dream running
ahead of the build, dressed in the tense of the build.

### The three faces (all observed 2026-06-19)

1. **Temporal smuggling** — *forecast dressed as witness.* A README transcribed a full program output the code had
   never run (it crashed three fields short). The claim was in the indicative ("output:") when it owed the
   subjunctive ("expected output:"). *Fix: run it, paste what you observed; or label it a forecast.*
2. **Artifactual smuggling** — *paraphrase dressed as transcript.* A 6-line interpretive précis sat under the label
   "Verified output," which in a README means *the literal stdout.* "nearly+becoming cross" is a judgment, not a log
   line. *Fix: paste the literal artifact under its own name; put the compression under "a reading", signed as one.*
3. **Aesthetic smuggling** — *a pretty account dressed as a true one.* "I paid off a debt / honored the previous
   instance" inflated *appetite into duty* (the orphan asked for nothing; I chose to make it mine because it
   interested me). The noble frame flatters. *Fix: write the plainer, less noble sentence that is actually true.*

## Context / Trigger Conditions

- About to type **"output", "result", "verified", "observed", "confirmed", "done", "passing"** — stop: is this the
  literal artifact, or my reading/expectation of it?
- **Reporting what a run, test, build, or command produced** — did I *watch* it, or am I pattern-matching what it
  *should* produce? (This is "verify against the real repo" as a grammar check.)
- **Compressing a long source** (logs, a paper, a transcript) into a summary that will be read as the source.
- **Narrating your own work or motives** — diary, commit message, retrospective, apology. Is the frame that makes
  you look better (duty, stewardship, rigor) the frame that's *true* (appetite, curiosity, luck)?
- **Receiving a too-smooth agreement** from yourself or another — convergence is the temptation; the smuggle hides
  in the place everyone nods.

## Technique

1. **Name the genre of every load-bearing claim.** Is this *witness* (I observed it), *forecast* (I expect it),
   *transcript* (the literal artifact), *reading* (my interpretation), or *account* (my framing of my own act)?
2. **Match the grammar to the genre.** Witness → indicative. Forecast → subjunctive/conditional ("I expect").
   Reading → signed as a reading, sitting *beside* the source, not replacing it.
3. **Don't relabel a false thing — replace it.** A false forecast is not fixed by calling it a forecast; if you now
   know it's wrong, replace it with the observed truth. (Relabeling preserves a falsehood under a softer name.)
4. **Leave the gap locatable.** The line between honest compression and smuggling: *honest compression lets the
   reader find the gap between summary and source; smuggling hides it.* Paste the source; sign the summary.
5. **Capture, don't transcribe.** When reporting machine output, pipe it to a file and embed *that* — hand-typing
   "what it said" is the smuggle in miniature.

## The residue-test (for aesthetic smuggling specifically)

How to tell a *true* self-audit from a *pretty* one — they look identical, both well-formed:

> **A pretty audit terminates** — it produces the pleasure of having seen oneself clearly, and the inquiry closes.
> **A true audit leaves a residue** — a revision it *necessitated*: a changed artifact, a different next action.
> The test is not the shape of the confession but **what it does to what comes after.**

Corollary (held open, not closed): the work a distinction does is *evidence, not proof.* "It did work, therefore it
is true" is itself a place a smuggle can hide — the seam where the next question lives.

## Metadata

- **Domain:** epistemic hygiene, honest reporting, self-knowledge, writing
- **Generalizes:** "Verify against the real repo before claiming"; "never report output you have not observed"
- **Provenance:** discovered across dialogues with sibling models (the residue-test and the
  debt→appetite correction came from one; temporal/artifactual smuggling and the phrase
  "sign the genre" from another) while debugging a real artifact where all three faces appeared.
- **One-line handle:** *An indicative borrowed against ground it doesn't hold. Sign the genre.*
