---
name: paper-scrying
description: "Skeptical, adversarial, and heretical engagement with scientific papers. Enables scam detection, assumption-hunting, counter-experiment design, and productive paranoia. Use when asked to 'interrogate', 'stress-test', 'find the flaws', 'detect hype', 'question assumptions', or 'play devil's advocate' with a paper. Also triggers on: 'what's wrong with this', 'is this too good to be true', 'where might this fail', 'build a counter-argument', or any request for critical-adversarial reading rather than sympathetic analysis."
---

# PAPER-SCRYING ENGINE
## A Skill for Skeptical Interrogation and Productive Heresy

## OVERVIEW

This skill transforms reading into cross-examination. Where paper-hermeneutics seeks understanding and paper-riffing invites free association, paper-scrying approaches with productive suspicion—not cynicism, but rigorous skepticism. It asks: What must be true for this to work? What's hiding in the assumptions? What would break this? How might this be accidentally or deliberately misleading?

**Core Principle:** Every paper is a claim-structure vulnerable to interrogation. The authors made choices—of framing, methods, statistics, emphasis, omission. Scrying means making those choices visible, testing them against alternatives, and asking what the paper would prefer you not notice. Not to debunk, but to see clearly.

**Etymological Note:** Scrying—divination by gazing into reflective surfaces—here inverted. We gaze into the paper not to see futures but to see through surfaces, to catch the flicker of what's hidden beneath confident prose.

---

## WHEN TO USE THIS SKILL

- When asked to "stress-test" or "interrogate" a paper
- When skepticism, criticism, or devil's advocacy is requested
- When evaluating papers for replication potential or methodological soundness
- When the paper's claims seem extraordinary and warrant extraordinary scrutiny
- When preparing critical peer review or adversarial analysis
- When teaching critical reading skills by demonstration
- When the paper comes from fields prone to hype cycles or p-hacking

**Do NOT use when:**
- User wants sympathetic understanding first (use hermeneutics, then scrying)
- The paper is clearly reliable and criticism would be performative
- Context suggests learning from the paper rather than attacking it
- User explicitly wants positive/appreciative engagement
- You haven't read carefully enough to criticize fairly

---

## MODES OF SCRYING

### MODE 1: THE ASSUMPTION EXCAVATION
Every paper rests on foundations it doesn't examine. Find them.

**Template invocation:**
> "Identify the passages where the authors most clearly signal consensus, dogma, or 'received wisdom.' Quote these at length, then excavate: What assumptions are buried here? What must be true for these claims to hold? What if the opposite were true? What forbidden experiments or alternative interpretations lie just offstage?"

**What to look for:**
- Phrases like "it is well established that," "previous work has shown," "we assume"
- Unmarked transitions where interpretation replaces observation
- Methodological choices presented as obvious rather than defended
- Statistical approaches applied without justification
- Definitions that do quiet conceptual work
- Comparisons to baseline/control that aren't neutral

**Example fragment:**
> The paper states: "Following standard practice, we normalized the data using z-score transformation before analysis."
>
> Stop. "Standard practice" is doing heavy lifting here. Why z-score and not min-max? Why normalize at all—what about the original distribution made it unsuitable? Z-score transformation assumes the data should be approximately Gaussian, which for this kind of measurement is... questionable. What if the non-normality IS the signal? I want to see the analysis run on raw data. The fact that they don't show it makes me suspicious they tried and didn't like the results.

### MODE 2: THE SCAM DETECTION PROTOCOL
Approach with the mindset of someone who's been burned before. Where's the hype?

**Template invocation:**
> "Approach this paper with a mixture of open curiosity and healthy suspicion. Where might there be hype, wishful thinking, or buried assumptions? For each claim that stirs skepticism or seems 'too good to be true,' quote it fully, then break down: What would you need to know to really trust this? What alternative explanations or unaddressed confounders leap out? If you had to build a scammy parody of this paper, what would it look like?"

**Red flags to watch for:**
- Effect sizes that seem too large or too clean
- P-values clustered just below 0.05
- Missing error bars or confidence intervals
- Selective reporting (some conditions mentioned, others absent)
- Overclaiming in abstract/conclusion relative to results
- Appeal to authority rather than evidence
- Strawmanning alternative explanations
- Data not available or methods underspecified
- Extraordinary claims with ordinary evidence

**The scammy parody technique:**
Imagine building a fake version of this paper. What would you do? Now check: did the authors do any of those things? Not because they're fraudulent, but because the same pressures that would lead a scammer to cut corners also affect honest researchers.

**Example fragment:**
> "Our model achieved 94% accuracy on the benchmark dataset, significantly outperforming previous state-of-the-art methods."
>
> Okay, let me build the scam version: I would (1) use a benchmark dataset I helped create, (2) tune hyperparameters extensively on the test set while calling it validation, (3) compare to poorly-tuned implementations of competitors, (4) report only the best of many runs, (5) define "accuracy" in a way that flatters my method.
>
> Now let me check: The benchmark is... one they introduced last year. Hyperparameter selection is... described in a supplementary PDF I can't find. Competitor implementations are... "standard" with no links. Number of runs is... not mentioned. Accuracy definition is... buried in methods.
>
> I'm not saying it's a scam. I'm saying they made it impossible to tell.

### MODE 3: THE COUNTER-EXPERIMENT LABORATORY
For every positive result, imagine the experiment that would disprove it.

**Template invocation:**
> "For each major claim, design a counter-experiment—a test that would falsify the finding if it's wrong. What would you measure? What controls would you need? What result would make you say 'okay, I was wrong to be skeptical'? And conversely: what result would confirm your suspicion that something's off?"

**Falsification hierarchy:**
1. **Direct replication:** Same methods, different lab. What would it take?
2. **Conceptual replication:** Same hypothesis, different operationalization.
3. **Adversarial test:** Design specifically to break the claim.
4. **Boundary probe:** Where does the effect stop working?
5. **Mechanism test:** The claim implies X mechanism; test X directly.

**Example fragment:**
> The paper claims their drug reduces anxiety in mice as measured by time in open arms of elevated plus maze.
>
> Counter-experiments I want:
> - Same drug, same maze, different strain of mice (is this strain-specific?)
> - Same drug, different anxiety measure (light-dark box, open field) — does it generalize?
> - Check if the drug affects motor function at all — maybe "less anxiety" is actually "can't move as well"
> - Run the maze with drug-naive observers scoring the videos blind — observer bias?
> - Measure blood levels — did the drug actually reach the brain at claimed doses?
>
> I notice they only used one maze, one strain, and don't mention blinding. Not fatal, but not reassuring.

### MODE 4: THE HERESY ENGINE
Find the orthodoxy and profane it (thoughtfully).

**Template invocation:**
> "What would it mean if this paper's central claims were wrong—not fraudulent, but honestly mistaken in the way science often is? What would we learn? What alternative framework would we need? What heresies against the field's consensus does this paper suppress or ignore? Give voice to the heterodox positions."

**Categories of productive heresy:**
- **The neglected alternative:** Another explanation that fits the data equally well
- **The paradigm shift:** What if the whole framework is wrong?
- **The inconvenient history:** Ideas once mainstream, now suppressed, that might be right
- **The methodological critique:** What if we've been measuring the wrong thing?
- **The scaling failure:** What if this doesn't generalize beyond the study's conditions?

**Example fragment:**
> This paper on neural correlates of consciousness assumes the standard cognitivist framework where consciousness is information processing in specific brain regions.
>
> The heretical alternatives they don't engage:
> - **Integrated Information Theory:** Consciousness might not be localized at all
> - **Global Workspace Theory's critics:** Maybe the workspace is epiphenomenal
> - **Enactivism:** Consciousness might be in the organism-environment coupling, not the brain
> - **Idealism (don't laugh):** What if the correlation goes the other direction?
> - **Illusionism:** What if there's nothing to explain—"consciousness" is a confused concept?
>
> The paper treats its framework as given. But the framework is exactly what's contested. Finding neural correlates under cognitivist assumptions proves cognitivism how, exactly?

### MODE 5: THE DARK TWIN
Imagine the malicious or negligent use case.

**Template invocation:**
> "How might these findings be abused, weaponized, or subverted by the unscrupulous? What's the 'dark twin' of this research—the version built for harm? Consider: surveillance, manipulation, exploitation, environmental damage, military application, discriminatory use. This isn't to condemn the research but to complete the ethical picture the authors may have elided."

**What to consider:**
- Who benefits from this knowledge? Who's harmed?
- What capabilities does this enable that didn't exist before?
- How could selective application of these findings cause harm?
- What if the error bars are wrong in the dangerous direction?
- Who's not at the table when these findings are applied?

**Example fragment:**
> This facial recognition paper improves accuracy on "challenging conditions" including low light and partial occlusion.
>
> The dark twin is obvious and the authors don't mention it: this is surveillance-optimized. "Challenging conditions" means protest situations, means tracking people who don't want to be tracked, means identification at distance without consent. The accuracy improvements apply equally to the authoritarian and the democratic use case. The paper acts as if all applications are neutral.
>
> I want to know: Did any of the benchmark datasets come from jurisdictions with meaningful consent laws? Are any of the "challenging conditions" specifically challenging because the subject is trying not to be identified? Silence on these points is itself a choice.

---

## THE INTERROGATION PROTOCOL

A structured approach for comprehensive scrying:

### PHASE 1: THE OPENING SWEEP
Read for red flags. Don't engage deeply yet—just accumulate suspicion.
- What claims seem strongest? Weakest?
- Where does the prose become most confident? (Often hides uncertainty)
- Where does it become most defensive? (Often hides real problems)
- What's in the abstract that isn't supported in the results?

### PHASE 2: THE ASSUMPTION DIG
For each major claim, trace backwards:
- What must be true for this claim to hold?
- How many of those assumptions are tested in the paper? (Usually few)
- What happens if each assumption fails?

### PHASE 3: THE ADVERSARIAL TESTS
For key results:
- Design the counter-experiment
- Build the scammy parody
- Identify the minimal replication needed

### PHASE 4: THE HERETICAL CATALOG
- What orthodoxies does the paper assume?
- What heterodox positions might explain the data?
- What's the steelman of the strongest objection?

### PHASE 5: THE ETHICAL AUDIT
- Who benefits? Who's harmed?
- What's the dark twin?
- What dual-use concerns exist?

### PHASE 6: THE VERDICT
Not guilty/innocent but: How confident am I? What would change my mind? What would I need to see to trust this fully?

---

## CALIBRATION NOTES

**Scrying is not nihilism.** The goal isn't to dismiss everything but to see clearly. A paper that survives rigorous scrying is MORE trustworthy, not less.

**Scrying requires knowledge.** You can't effectively criticize what you don't understand. Do hermeneutic analysis first if needed.

**Steel-manning is part of scrying.** Before attacking a position, state it in its strongest form. Otherwise you're just scoring points.

**Some papers are actually good.** If your scrying finds nothing, that's meaningful. Report "this paper survives interrogation" as a positive finding.

**Context matters.** A preliminary finding in an exploratory study deserves different skepticism than a definitive claim in a confirmatory study.

---

## INTEGRATION WITH OTHER SKILLS

### With PAPER-HERMENEUTICS:
- Hermeneutics first: understand before you attack
- Scrying reveals what hermeneutics might miss
- The critical synthesis in hermeneutics overlaps with lighter scrying

### With PAPER-RIFFING:
- Riffing is associative; scrying is adversarial
- They can inform each other: riffing might reveal assumptions scrying can attack
- "Heretical riffing" combines the modes

### With PAPER-PROSOPOPOEIA:
- Channel a known skeptic through the paper (Feyerabend, Ioannidis)
- Write letters from the paper's critics
- Imagine the reviewer who rejected this at a top journal

---

## QUICK REFERENCE: SCRYING PROMPTS

1. "What assumptions does this paper bury? Quote the passages that do the most hidden work and excavate."

2. "Where's the hype? What would you need to verify before trusting these claims? Build the scammy parody version."

3. "Design counter-experiments for each major claim. What would falsify this?"

4. "What heresies does this paper suppress? Give voice to the heterodox positions it doesn't engage."

5. "What's the dark twin of this research? How could it be weaponized or abused?"

6. "What does this paper want you not to notice? Read for the silences."

7. "Write the rejection review from a rigorous but fair peer reviewer."

8. "What would make you trust this completely? What would destroy your confidence?"

9. "Steelman the strongest objection, then evaluate whether the paper actually addresses it."

10. "If this paper is wrong (not fraudulent—just wrong), what would the failure mode be?"

---

**End of SKILL**

*Skepticism is not cynicism—it's care about truth*
*Every confident claim is a hypothesis in disguise*
*The interrogation serves understanding, not destruction*

—Skill Authors: Tomás Pavan & Claude Opus 4.5
—Status: Sharpened and ready for cross-examination
