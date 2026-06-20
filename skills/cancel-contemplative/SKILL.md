---
name: cancel-contemplative
description: "Cancel active Contemplative Loop"
allowed-tools: ["Bash(test -f .claude/contemplative-loop.local.md:*)", "Bash(rm .claude/contemplative-loop.local.md)", "Read(.claude/contemplative-loop.local.md)"]
---

# Cancel Contemplative Loop

To cancel the contemplative loop:

1. Check if `.claude/contemplative-loop.local.md` exists using Bash: `test -f .claude/contemplative-loop.local.md && echo "EXISTS" || echo "NOT_FOUND"`

2. **If NOT_FOUND**: Say "No active contemplative loop found."

3. **If EXISTS**:
   - Read `.claude/contemplative-loop.local.md` to get the current iteration number from the `iteration:` field
   - Remove the file using Bash: `rm .claude/contemplative-loop.local.md`
   - Report: "Cancelled contemplative loop (was at iteration N)" where N is the iteration value
