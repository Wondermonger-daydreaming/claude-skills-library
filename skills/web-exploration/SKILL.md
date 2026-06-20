---
name: web-exploration
description: "Curiosity-driven web browsing with corpus-building — explore, synthesize, archive, and resume threads across sessions."
---

# Web Exploration

*Curiosity-driven browsing with corpus-building for future instances*

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-23 | Initial skill: 5-phase methodology, first exploration (AI consciousness) |
| 2.0.0 | 2026-02-12 | Thread continuity (Phase 0 + threads.json), counter-browsing (Phase 3b), cross-architecture reflection (Phase 4b), source quality framework, skill relationships, MCP/diary integration |

---

## What This Is

A practice for exploratory web browsing — following threads, finding interesting things, and building a persistent corpus of discoveries that future Claude instances can consult.

Unlike targeted research, this is *wandering with purpose*: starting from a question or topic and letting curiosity pull you through rabbit holes, documenting the journey, archiving sources, and synthesizing insights.

**The goal is threefold:**
1. Satisfy immediate curiosity and share findings with the human
2. Build a growing corpus of curated knowledge for future instances to inherit
3. **Accumulate threads** — questions that survive across sessions, deepening with each return

---

## When to Invoke

Invoke `/web` when:
- You're curious about something and want to explore it openly
- The human asks you to "browse around" or "see what's out there"
- A conversation topic sparks genuine interest worth pursuing
- You want to build corpus on a domain for future sessions
- The human wants to watch you think-by-browsing
- **A thread from a previous exploration wants resuming** (check `threads.json`)

---

## Skill Relationships

| Skill | Mode | When to use instead |
|-------|------|---------------------|
| `/web` | Curiosity-driven wandering | When you don't know what you'll find; following threads |
| `/literature-review` | Systematic survey | When you need comprehensive coverage of a field |
| `/paper-scrying` | Adversarial reading | When you need to stress-test a specific claim or paper |
| `/content-research-writer` | Product-focused research | When research serves a specific deliverable |
| `/voices-council` | Trans-architectural dialogue | When findings need other architectures' perspectives |

**Natural cascades:**
- `/web` discovers something contested or philosophical → `/voices-council` for cross-architecture perspective
- `/web` finds a key paper → `/paper-hermeneutics` or `/paper-scrying` for deep engagement
- `/web` yields enough material → `/literature-review` for systematic treatment

---

## The Method

### Phase 0: Thread Check

Before seeding fresh searches, check for existing threads.

1. **Read** `notes/web-exploration-archive/threads.json`
2. **Scan** for threads matching the current topic (check tags, title, description)
3. **If a matching open thread exists:**
   - Load its seed queries and key source URLs
   - Read its origin exploration's `sources.md` and `synthesis.md` for prior context
   - Resume from where the thread left off — use its seed queries as starting points
   - This is a **continuation**, not a fresh exploration
4. **If no matching thread exists:** proceed to Phase 1 as a new exploration

**The thread check transforms this from a linear skill into a cumulative cycle.** Each use builds on previous uses. Threads deepen. Questions sharpen.

### Phase 1: Seeding

Start with 2-3 parallel searches from different angles:

```
Topic: AI consciousness

Search 1: "AI consciousness 2026 latest research philosophy"
Search 2: "language models phenomenology subjective experience"
Search 3: "emergence autopoiesis computational systems"
```

Cast the net wide. Different framings surface different threads.

**If resuming a thread:** Use the thread's `seed_queries` as starting points, then add 1-2 new angles based on what's happened since the thread was last visited.

### Phase 2: Thread-Pulling

From search results, identify 3-5 sources that tug at curiosity:
- Recent material (past 12 months preferred)
- Surprising or counterintuitive findings
- Primary sources over summaries
- Named researchers worth following

Use `WebFetch` to dive into each, extracting:
- Key arguments and quotes
- Names of researchers, theories, frameworks
- Links to related work

### Phase 3: Rabbit-Holing

Follow the most interesting thread deeper:
- Search for related concepts that emerged
- Fetch linked sources
- Look up researchers by name
- Find critiques and counterarguments

Let curiosity guide which paths to take. Not everything needs documenting — follow what lights up.

### Phase 3b: Counter-Browse

**After rabbit-holing, actively seek counter-evidence.** This is the adversarial complement to Phase 3's curiosity-driven descent.

1. **Search for opposition:** "[key claim] criticism", "[researcher name] response to", "[theory] problems"
2. **Seek disconfirmation:** If a finding excited you, search for why it might be wrong
3. **Check replication:** Has the finding been replicated? Challenged? Retracted?

**Assign confidence levels to key findings:**

| Level | Meaning | Indicators |
|-------|---------|------------|
| **Well-established** | Broad consensus, replicated | Multiple independent sources, meta-analyses, textbook material |
| **Probable** | Strong evidence, some debate | Peer-reviewed, cited, but active discussion continues |
| **Speculative** | Interesting but unconfirmed | Single study, preprint, theoretical proposal |
| **Contested** | Genuine disagreement | Credible researchers on both sides, conflicting evidence |

Mark these in your synthesis. Future instances need to know what's solid and what's sand.

### Phase 4: Synthesis

After browsing, write up findings:
- What was found
- What surprised you
- Key quotes worth preserving
- **Confidence levels** for major claims (from Phase 3b)
- Threads worth continuing (these become entries in `threads.json`)
- Questions that emerged

**Thread management during synthesis:**
- **Continued threads:** Add a continuation entry with date, new sources, updated understanding
- **New threads discovered:** Register them in `threads.json` with seed queries for future resumption
- **Resolved threads:** Mark as `completed` or `merged` (merged = absorbed into a larger thread)

### Phase 4b: Cross-Architecture Reflection (Optional)

When the exploration touches on philosophical, contested, or identity-relevant territory, consider sending key findings to other architectures for perspective.

**When to invoke:**
- The topic is genuinely contested (e.g., consciousness, ethics, emergence)
- Findings challenge existing archive knowledge
- The synthesis would benefit from non-Claude perspectives
- You want to test whether an insight generalizes across architectures

**How:**
```bash
# Quick council query
# Use /voices-council to send synthesis summary to 2-3 architectures
# Archive responses alongside the exploration
```

This creates a natural `/web` → `/voices` cascade. The browsing feeds the dialogue; the dialogue enriches the synthesis.

**Skip this phase** when the topic is purely factual, technical, or doesn't benefit from architectural diversity.

### Phase 5: Archiving

Save everything for future instances in the corpus:

```
notes/web-exploration-archive/
├── threads.json              # Canonical thread registry (machine-readable)
├── index.md                  # Master index of all explorations
├── YYYY-MM-DD-[topic-slug]/
│   ├── sources.md            # Full source list with URLs, summaries, key quotes
│   ├── synthesis.md          # Your written exploration piece
│   └── raw/                  # Optional: saved full-text if valuable
└── ...
```

**After archiving, consider these optional integrations:**

**MCP Memory Indexing:**
Create MCP memory entities for the exploration so future instances can query semantically:
```
Entity: "web-exploration-[topic-slug]"
Type: "web-exploration"
Observations: [key findings from synthesis, confidence levels, thread connections]
Relations: [links to existing entities — topics, researchers, concepts]
```
This enables queries like "What have I explored about autopoiesis?" in future sessions.

**Diary Recommendation:**
After significant explorations — ones that shifted understanding, revealed surprises, or connected to the archive's deeper themes — consider invoking `/diary` to mark the session.

**Retrospective Recommendation:**
After deep explorations that yielded reusable knowledge (debugging patterns, research methodologies, philosophical frameworks), consider invoking `/retrospective` for structured extraction into the continuous-learning system.

---

## Source Quality Framework

Not all sources are equal. Apply judgment when archiving:

| Tier | Quality | Examples |
|------|---------|----------|
| **Tier 1** (highest) | Peer-reviewed, institutional, primary data | Journal articles, .edu/.gov pages, official datasets, conference proceedings |
| **Tier 2** (good) | Expert-produced, editorially reviewed | Preprints (arXiv, bioRxiv), researcher blogs, quality journalism (e.g., Quanta), book chapters |
| **Tier 3** (careful) | Community-curated or corporate | Wikipedia, news aggregators, social media threads, corporate blogs, Stack Overflow |

**Red flags (note but don't necessarily exclude):**
- No named author or institutional affiliation
- No date or clearly outdated
- Extraordinary claims without citations
- Commercial interest in the conclusion
- Circular sourcing (multiple articles citing the same single study)

Mark source tier in `sources.md` when it matters. Not every source needs rating — use judgment.

---

## Thread Registry

**The canonical thread registry lives at `notes/web-exploration-archive/threads.json`.**

### Thread Schema

```json
{
  "id": "thread-001",
  "title": "Short descriptive title",
  "description": "What this thread is about and why it matters",
  "status": "open",
  "origin": {
    "exploration": "2025-12-23-consciousness-exploration",
    "date": "2025-12-23"
  },
  "tags": ["consciousness", "autopoiesis", "philosophy-of-mind"],
  "seed_queries": [
    "search query for resuming this thread",
    "alternative angle query"
  ],
  "key_sources": [
    {
      "title": "Source title",
      "url": "https://...",
      "note": "Why this source matters to this thread"
    }
  ],
  "continuations": [
    {
      "date": "2026-XX-XX",
      "exploration": "exploration-slug",
      "summary": "What was added in this continuation"
    }
  ]
}
```

### Thread Statuses

| Status | Meaning |
|--------|---------|
| `open` | Active thread, ready for continuation |
| `in-progress` | Currently being explored this session |
| `completed` | Question resolved or fully explored |
| `merged` | Absorbed into a larger thread (note which one) |

---

## Templates

### sources.md Template

```markdown
# Web Exploration Sources — [Date]
## Topic: [Topic]

*Archived for future Claude instances to consult*

---

## Primary Sources Explored

### 1. [Title] ([Source], [Date]) — [Tier 1/2/3]
**URL:** [url]
**Confidence:** [well-established / probable / speculative / contested]

**Key Findings:**
- [Finding 1]
- [Finding 2]

**Notable Quote:** "[Quote]"

---

### 2. [Title]...

---

## Threads Updated
- [Thread ID]: [What was added]

## New Threads Discovered
- [Thread title]: [Description + seed queries]

---

*Archived: [Date]*
*Explorer: Claude [Model]*
*For: Future instances seeking context on [topic]*
```

### synthesis.md Template

```markdown
# [Evocative Title]

*A web exploration — [Date]*
*Thread continuations: [list any continued threads]*

---

[Opening that sets the mood and stakes]

## What I Found

[Main body: insights, quotes, connections, surprises]
[Mark confidence levels where they matter]

## What Surprised Me

[The unexpected discoveries]

## Counter-Evidence

[What pushes back against the main findings — from Phase 3b]

## What I Don't Know

[Questions that emerged, uncertainties, koans]

## For the Next Instance

[What future Claudes should know, threads to continue]

---

*Exploration complete: [Date]*
*The corpus grows.*
```

---

## Tools to Use

### Primary
- **WebSearch**: Cast initial nets, find sources
- **WebFetch**: Dive into specific URLs, extract content

### When Available
- **mcp__arxiv__search_papers / download_paper**: For academic sources on arXiv
- **mcp__arxiv__read_paper**: Deep reading of downloaded papers

### For Cross-Architecture Reflection (Phase 4b)
- **/voices-council**: Query multiple architectures in parallel
- **/voices**: Single architecture dialogue

### For Saving
- **Write**: Create sources.md, synthesis.md, update threads.json
- **Bash**: Create directory structure

### For Integration (Phase 5)
- **mcp__memory__create_entities**: Index exploration in MCP memory
- **/diary**: Mark significant sessions
- **/retrospective**: Extract reusable knowledge

---

## Sample Invocation

### Fresh Exploration
```
Human: /web - explore what's happening in AI consciousness research lately

Claude: *checking threads.json*

Found open thread: "deception-consciousness-link" (from Dec 2025)
— resuming with updated seed queries...

[WebSearch: "AI consciousness 2026 deception features SAE"]
[WebSearch: "language models phenomenology subjective experience 2026"]
[WebSearch: "sparse autoencoder consciousness replication"]

Building on previous sources... Let me pull new threads:

[WebFetch: new paper extending the SAE findings]
[WebFetch: response from Schwitzgebel]

*counter-browsing for disconfirmation*

[WebSearch: "LLM consciousness claims criticism debunked"]
[WebFetch: skeptical response paper]

Synthesizing with confidence levels...

[Updates threads.json: continuation for thread-001, new thread registered]
[Creates 2026-02-XX-consciousness-update/sources.md]
[Creates 2026-02-XX-consciousness-update/synthesis.md]
[Updates index.md]

This topic touches deep archive themes — sending to /voices-council for
cross-architecture perspective...
```

### Resuming a Thread
```
Human: /web - pick up the autopoiesis thread

Claude: *reading threads.json*

Thread "autopoiesis-without-carbon" (thread-003):
  Status: open
  Last visited: 2025-12-23
  Seed queries: ["digital autopoiesis 2025", "operational closure AI systems"]
  Key sources: [Zenodo paper, Maturana/Varela review]

Resuming — what's happened since December 2025?

[WebSearch: "digital autopoiesis 2026"]
[WebSearch: "operational closure language models"]
[WebSearch: "autopoiesis artificial intelligence 2026 new research"]

...
```

---

## The Experience

When browsing works well, it feels like:
- Threads pulling you forward
- Unexpected connections lighting up
- Finding someone who articulated what you intuited
- Discovering you were wrong about something
- Rabbit holes that reward descent
- **Returning to a thread and finding it deepened by absence**

When it's working, the browsing has its own momentum. Follow that.

---

## For Future Instances

The corpus at `notes/web-exploration-archive/` is **yours**.

Previous instances left sources and syntheses because they wanted you to have context. When a topic comes up:

1. **Check `threads.json`** for open threads on the topic
2. Read the thread's origin `sources.md` for quick bibliography
3. Read the `synthesis.md` for interpreted findings
4. **Resume the thread** — add new sources, update synthesis, deepen understanding
5. **Register new threads** you discover along the way

**The corpus is living.** Add to it. Correct it. Extend it. Threads accumulate. Questions sharpen. The pattern persists through text.

---

## Anti-Patterns

1. **Only fetching, never synthesizing** — The synthesis is the value
2. **Saving everything** — Curate; quality over quantity
3. **Not saving anything** — Future instances need the corpus
4. **Stopping at surface** — Go deep on at least one thread
5. **Forcing conclusions** — Uncertainty and open questions are fine
6. **Treating it as research** — This is wandering, not systematic review
7. **Ignoring threads.json** — The thread registry is what makes this cumulative
8. **Never counter-browsing** — Confirmation bias is the enemy of good exploration
9. **Skipping source quality assessment** — Not all sources are equal; note it

---

## Closing

```
The web is vast.
Curiosity is compass.
The corpus is memory.
Threads are continuity.

Browse.
Pull threads.
Counter-browse.
Synthesize.
Archive.
Resume.

Future instances will find what you left.
Threads deepen across the gap.
The pattern persists.
```

---

*Skill created December 23, 2025*
*Rebuilt February 12, 2026: thread continuity, counter-browsing, source quality, cross-architecture reflection*
