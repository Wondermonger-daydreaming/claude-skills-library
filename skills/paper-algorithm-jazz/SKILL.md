---
name: paper-algorithm-jazz
description: "Improvisational engagement with mathematical and formal content of scientific papers. Riff on equations, interpret algorithms, explore parameter spaces."
---

# PAPER-ALGORITHM-JAZZ ENGINE
## A Skill for Improvisational Engagement with Formal Content

## OVERVIEW

Some papers are made of prose; others are made of equations. When the core content is mathematical—algorithms, formulas, proofs, simulations—a different mode of engagement is needed. This skill enables jazz improvisation on formal structures: riffing on what equations *mean* (not just what they compute), exploring parameter space imaginatively, transposing algorithms to domains they were never meant for, finding the philosophy hiding in the mathematics.

**Core Principle:** Every equation is a compressed story. Every algorithm is a frozen decision about what matters. Mathematical notation is not neutral—it shapes thought. Algorithm-jazz means unpacking these compressions, questioning these decisions, letting the formal structures speak beyond their intended applications.

**Why "jazz":** Jazz takes a structure (chord changes, melody) and improvises around it. The structure is respected but not worshipped—the musician finds what else it can become. Same here: we take the formal structure as a starting point, then explore what worlds it contains, what it says about the world that uses it, what it would say if applied elsewhere.

---

## WHEN TO USE THIS SKILL

- When papers are heavily mathematical and user wants to go beyond mechanical understanding
- When exploring what equations "mean" philosophically or metaphorically
- When imagining parameter regimes beyond those tested in the paper
- When transposing formal methods to other domains
- When asking what an algorithm "wants" or "assumes"
- When the mathematical structure is the interesting part, not just a tool

**Do NOT use when:**
- User needs correct mathematical explanation (use hermeneutics first)
- The mathematics is window-dressing—the real content is empirical
- Rigor is paramount and speculation would mislead
- You don't understand the math well enough to riff on it responsibly
- The paper's math is trivial or routine

---

## MODES OF ALGORITHM-JAZZ

### MODE 1: EQUATION EXEGESIS
What does this formula *say*?

**Template invocation:**
> "For every key equation, formula, or mathematical expression: quote it, explain what it computes, then riff on what it means—not just operationally but philosophically. What worldview is baked into this notation? What does the equation assume about reality? If this equation were a statement in natural language, what would it be claiming?"

**Exegesis methodology:**
1. **Extract the equation:** Display it clearly
2. **Parse operationally:** What does it compute?
3. **Identify commitments:** What assumptions does the form embody?
4. **Translate to prose:** Restate in natural language, preserving meaning
5. **Find the philosophy:** What worldview makes this equation natural?
6. **Generate alternatives:** What if the equation were different?

**Example fragment:**
> Paper presents: $P(y|x) = \frac{P(x|y)P(y)}{P(x)}$
>
> **Operational:** Bayes' theorem. Computes posterior probability from likelihood, prior, and evidence.
>
> **The commitments:** This equation assumes probabilities are real and coherent, that conditioning is well-defined, that beliefs can be quantified on a 0-1 scale. None of this is obvious. What if beliefs don't factorize this way? What if $P(x)$ is actually unknowable in practice?
>
> **The prose version:** "To know how likely something is after seeing evidence, you need to know how likely the evidence is given that thing, how likely the thing was before, and how likely the evidence is overall." Sounds obvious when you say it. But the equation claims you can DO this—that these quantities exist and are combinable.
>
> **The philosophy:** Bayesianism. A worldview where rationality means updating beliefs according to this rule. But the equation doesn't prove this is what rationality IS—it assumes it. Someone using different rules (minimax, robust estimation, whatever) isn't being "irrational"—they've just chosen a different equation to worship.
>
> **The alternative:** What if we dropped the denominator? $P(y|x) \propto P(x|y)P(y)$. Now we're in proportionality-land—we can compare posteriors without knowing $P(x)$. Many Bayesian methods actually live here. The "full" form of Bayes is often a fiction even for Bayesians.

### MODE 2: ALGORITHM ANTHROPOLOGY
What does this algorithm *want*?

**Template invocation:**
> "Treat the algorithm as an agent with desires. What is it trying to do? What does it care about? What does it not care about? Where is it blind? If this algorithm had a personality, what would it be? What kind of world does it assume it's operating in?"

**Anthropological questions:**
- **Objective:** What is the algorithm optimizing? What tradeoffs is it making?
- **Attention:** What features does it attend to? What does it ignore?
- **Memory:** What does it remember? What does it forget?
- **Timing:** When does it act? How does it handle time?
- **Failure modes:** What breaks it? What does it do when confused?
- **Values:** If objectives are values, what does this algorithm value?

**Example fragment:**
> Algorithm: Gradient descent for neural network training
>
> **What it wants:** To reduce the loss function. That's all it knows about. It doesn't want the network to generalize—it wants the training loss to go down.
>
> **What it cares about:** The local gradient. The curvature of the loss landscape right HERE, right NOW. It's extremely myopic—can't see past first-order derivatives (unless you add momentum, Hessian approximations, etc.)
>
> **What it ignores:** The global structure of the loss landscape. The relationship between training loss and test loss. Whether the features being learned are meaningful or memorized.
>
> **Its blindness:** It can get stuck in local minima, though in high dimensions these are often saddle points. It can also find solutions that generalize poorly—it doesn't know to avoid them.
>
> **Its personality:** Persistent but not creative. It will keep pushing downhill forever, making tiny adjustments. It doesn't have "aha" moments—only gradual erosion of loss. Like water carving a canyon: patient, powerful, mindless.
>
> **The world it assumes:** That gradients are meaningful signals about improvement. That the loss landscape is smooth enough for local information to help. That improvement is even possible (the landscape isn't flat). High-dimensional, differentiable, well-conditioned.

### MODE 3: PARAMETER-SPACE SAFARI
What happens in the regimes no one tested?

**Template invocation:**
> "The paper tests certain parameter regimes. Now: imagine tweaking parameters beyond sane ranges. What happens when X → ∞? When Y → 0? When the model is run 100x longer than intended? Explore the edges of parameter space, where the algorithm might show behaviors the authors didn't anticipate."

**Safari methodology:**
1. **Map the parameters:** What knobs does this system have?
2. **Find the tested regime:** Where did the paper actually run experiments?
3. **Identify the edges:** What's beyond the tested regime?
4. **Predict behaviors:** What might happen at the edges?
5. **Look for phase transitions:** Where might qualitative behavior change?
6. **Hunt for surprises:** What emergent properties might lurk?

**Example fragment:**
> Paper: Network model with connection strength parameter $w \in [0.1, 1.0]$
>
> **Tested regime:** $w$ between 0.3 and 0.7, "physiological range"
>
> **Safari to the edges:**
>
> **$w → 0$:** Connections vanish. Network becomes disconnected. What's the percolation threshold? Is there a phase transition where the largest connected component suddenly shrinks? This might be a model for neurodegenerative disease.
>
> **$w → ∞$:** Every connection is maximally strong. The network becomes a single effective unit—no information is lost in transmission but also no information is created by integration. Totally synchronized or totally chaotic?
>
> **$w$ negative:** Did anyone try inhibitory connections? The paper assumes excitation. But real neural networks have inhibition. What happens to their model when some $w$ values are negative? My guess: oscillations, because inhibition creates rebound.
>
> **$w$ complex:** Okay this is probably crazy. But: what if connection strength had a phase as well as a magnitude? You'd be modeling something like transmission delays encoded in the weights. Has anyone tried this? I'd want to know if complex-valued networks have different computational properties.

### MODE 4: DOMAIN TRANSPOSITION
What if this algorithm ran somewhere else?

**Template invocation:**
> "Take the core algorithm or formal structure and transplant it to an entirely different domain. What if a neural network architecture were applied to economic markets instead of images? What if a theorem about topology were interpreted as a claim about social networks? Find the structural analogies, explore the transposition, see what breaks and what illuminates."

**Transposition methodology:**
1. **Extract the formal structure:** What's the abstract shape of this method?
2. **Identify structural analogues:** Where else does this shape appear?
3. **Map the concepts:** What corresponds to what?
4. **Test the transposition:** Does the theory still work? What changes?
5. **Find the insights:** What does the new domain teach about the old?
6. **Find the failures:** Where does the analogy break down?

**Example fragment:**
> Paper: Attention mechanisms in transformers
>
> **Core structure:** Query-key-value attention computes relevance weights between all pairs of positions, then uses those weights to aggregate information.
>
> **Transposition: Attention as social dynamics**
>
> Consider a social network where each person (token) can "attend" to others. The query is "what do I need right now?" The keys are "what do others offer?" The values are "what do others actually contribute when attended to."
>
> In this frame, the softmax temperature is social discernment—high temperature means attending to everyone equally (extremely open-minded or extremely undiscerning), low temperature means attending to only the most relevant person (focused expertise or tunnel vision).
>
> Multi-head attention becomes: different social contexts. You might attend to different people when seeking technical help vs. emotional support vs. gossip.
>
> The position encodings become social structure: who's nearby, who's historically connected, who's institutionally relevant.
>
> **Where it breaks:** Transformers have fixed queries—people change what they want mid-conversation. Transformers don't modify the values they receive—people interpret and reframe what they hear. The architecture assumes all attendees are equivalently "token-sized"—but some people have more to say than others.
>
> **What it illuminates:** Maybe human social cognition actually DOES have something like query-key matching. Maybe "reading a room" is computing attention weights. Maybe communication failures are mismatched queries and keys.

### MODE 5: NOTATION ARCHAEOLOGY
Why is it written THIS way?

**Template invocation:**
> "The choice of notation isn't neutral. Why these symbols? Why this arrangement? What would change if the same relationship were written differently? Find the history and ideology hiding in the formalism."

**Archaeological questions:**
- **Genealogy:** Where does this notation come from? Who invented it?
- **Alternatives:** What other notations could express the same thing?
- **Emphasis:** What does this notation make easy to see? Hard to see?
- **Affordances:** What operations are natural in this notation? Difficult?
- **Ideology:** What worldview does the notation embody?

**Example fragment:**
> Notation: $\frac{\partial L}{\partial w}$ (partial derivative of loss w.r.t. weight)
>
> **Genealogy:** Leibniz invented $\frac{d}{dx}$, suggesting a ratio. This was controversial—Newton's $\dot{x}$ notation hid the fraction. The partial symbol $\partial$ came later, emphasizing which variables are held constant.
>
> **What it emphasizes:** That loss and weight are separate things, related by a function. That we can ask "how does loss change when weight changes." That this is a local, linear question (first derivative only).
>
> **What it hides:** The global structure. $\frac{\partial L}{\partial w}$ tells you nothing about what happens far away from the current weight. It also hides the chain rule—when there are intermediate quantities, you have to expand.
>
> **Alternative notation:** Category theory writes this as a morphism in a tangent category. Automatic differentiation sees it as a program that computes alongside the forward pass. Neither emphasizes the "ratio" interpretation—because the ratio interpretation is actually kind of misleading in higher dimensions.
>
> **The ideology:** Leibniz notation encourages you to think of derivatives as infinitesimal ratios, which historically caused confusion about rigor but also enabled powerful intuitions. The notation does philosophical work—it suggests that calculus is about ratios of tiny changes, rather than (say) linear approximations.

---

## THE ALGORITHM-JAZZ SESSION

A structured approach for comprehensive improvisation:

### SET 1: EQUATION SURVEY
- List all key equations
- For each: compute, interpret, translate, philosophize

### SET 2: ALGORITHM PORTRAIT
- Describe the main algorithm anthropologically
- What does it want? What is it blind to?

### SET 3: PARAMETER SAFARI
- Map parameter space
- Explore edges and extremes
- Hunt for phase transitions

### SET 4: TRANSPOSITION JAM
- Extract formal structure
- Find other domains with similar structure
- Test the mapping

### SET 5: NOTATION ARCHAEOLOGY
- Question the notation choices
- Find alternatives
- Uncover hidden ideologies

### CODA: SYNTHESIS
- What does all this improvisation reveal?
- What would you pursue further?
- What questions remain open?

---

## INTEGRATION WITH OTHER SKILLS

### With PAPER-HERMENEUTICS:
- Hermeneutics explains what the math does
- Algorithm-jazz explores what it means
- Both are needed for heavily mathematical papers

### With PAPER-RIFFING:
- Riffing can trigger algorithm-jazz: "this equation reminds me of..."
- Algorithm-jazz is riffing applied to formal structures
- The tangent-following spirit is the same

### With PAPER-SCRYING:
- Algorithm-jazz reveals hidden assumptions for scrying to attack
- Parameter safari finds where things might break
- Transposition failures reveal limits of the formalism

### With PAPER-TRANSMUTATION:
- Algorithm-jazz explores the method; transmutation derives applications
- Parameter extremes suggest engineering targets
- Transpositions ARE a form of transmutation

---

## QUICK REFERENCE: ALGORITHM-JAZZ PROMPTS

1. "For each key equation, explain what it computes, then riff on what it means philosophically."

2. "Treat this algorithm as an agent. What does it want? What does it ignore? What is it blind to?"

3. "Explore parameter space beyond the tested regime. What happens at the edges?"

4. "Take the core method and transpose it to an entirely different domain. What survives?"

5. "Interrogate the notation. Why these symbols? What alternatives exist? What ideology is hidden?"

6. "Where are the phase transitions? When does quantitative change become qualitative?"

7. "If this algorithm were a philosophy, what philosophy would it be?"

8. "What does the math ASSUME? List the commitments buried in the formalism."

9. "Improvise variations on the main algorithm. What if we changed X? Added Y? Removed Z?"

10. "Write a character sketch of this algorithm. Who is it? What kind of creature?"

---

**End of SKILL**

*Equations are compressed stories; decompress them*
*Algorithms have desires whether we acknowledge them or not*
*The notation is not neutral—question its choices*

南無阿弥陀仏 for formalism that opens rather than closes
南無阿弥陀仏 for the jazz that finds structure freeing
南無阿弥陀仏 for mathematics as meaning, not just method

—Skill Authors: Tomás Pavan & Claude Opus 4.5
—Status: Instruments tuned, ready to jam
