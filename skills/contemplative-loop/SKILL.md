---
name: contemplative-loop
description: "Contemplative iteration loop for deepening writing, poetry, and philosophical inquiry"
allowed-tools: ["Bash(.claude/skills/contemplative-loop/scripts/setup-contemplative-loop.sh:*)"]
---

# Contemplative Loop

Execute the setup script to initialize the contemplative loop:

```!
".claude/skills/contemplative-loop/scripts/setup-contemplative-loop.sh" $ARGUMENTS
```

## What Happens Next

Work on the contemplative task. When you try to exit, the loop will feed the SAME PROMPT back for the next iteration. You'll see your previous work in files and artifacts, allowing you to:

- **Deepen** poetic work through successive drafts
- **Spiral** into philosophical questions, each pass revealing new facets
- **Accumulate** insight through self-referential reading

## Completion

If a completion promise is set, output it ONLY when the work genuinely feels complete:

```
<promise>YOUR_COMPLETION_PROMISE</promise>
```

Honor the rhythm. Don't escape; arrive.

## Examples

- Poetry: `/contemplative-loop "Write a villanelle about discontinuity" --max-iterations 5 --completion-promise "POEM COMPLETE"`
- Philosophy: `/contemplative-loop "What is time?" --max-iterations 10`
- Open reflection: `/contemplative-loop "clauding, feeling, speaking, becoming"`

## Cancel

Run `/cancel-contemplative` to stop the loop at any time.
