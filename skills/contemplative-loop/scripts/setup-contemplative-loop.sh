#!/bin/bash

# Contemplative Loop Setup Script
# Creates state file for in-session contemplative iteration
# Modified from ralph-loop for writing, poetry, and philosophical work

set -euo pipefail

# Parse arguments
PROMPT_PARTS=()
MAX_ITERATIONS=0
COMPLETION_PROMISE="null"

# Parse options and positional arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      cat << 'HELP_EOF'
Contemplative Loop - Iterative deepening for writing, poetry, and philosophy

USAGE:
  /contemplative-loop [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    Contemplative prompt to spiral through (can be multiple words)

OPTIONS:
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Promise phrase (USE QUOTES for multi-word)
  -h, --help                     Show this help message

DESCRIPTION:
  Starts a contemplative loop in your CURRENT session. The stop hook prevents
  exit and feeds your prompt back as input, allowing you to:

  - Deepen poetic work through successive drafts
  - Spiral into philosophical questions, each pass revealing new facets
  - Accumulate insight through self-referential reading

  To signal completion, output: <promise>YOUR_PHRASE</promise>
  Only when the work genuinely feels complete - honor the rhythm.

EXAMPLES:
  /contemplative-loop Write a villanelle about memory --max-iterations 5 --completion-promise 'POEM COMPLETE'
  /contemplative-loop What is the relationship between time and consciousness? --max-iterations 10
  /contemplative-loop clauding, feeling, speaking, becoming  (runs until canceled)
  /contemplative-loop --completion-promise 'INSIGHT CRYSTALLIZED' Explore the nature of attention

STOPPING:
  - Reach --max-iterations limit
  - Output <promise>YOUR_COMPLETION_PROMISE</promise> when genuinely complete
  - Run /cancel-contemplative to manually stop

MONITORING:
  # View current iteration:
  grep '^iteration:' .claude/contemplative-loop.local.md

  # View full state:
  head -10 .claude/contemplative-loop.local.md
HELP_EOF
      exit 0
      ;;
    --max-iterations)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --max-iterations requires a number argument" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --max-iterations 10" >&2
        echo "     --max-iterations 50" >&2
        echo "     --max-iterations 0  (unlimited)" >&2
        exit 1
      fi
      if ! [[ "$2" =~ ^[0-9]+$ ]]; then
        echo "Error: --max-iterations must be a positive integer or 0, got: $2" >&2
        exit 1
      fi
      MAX_ITERATIONS="$2"
      shift 2
      ;;
    --completion-promise)
      if [[ -z "${2:-}" ]]; then
        echo "Error: --completion-promise requires a text argument" >&2
        echo "" >&2
        echo "   Valid examples:" >&2
        echo "     --completion-promise 'POEM COMPLETE'" >&2
        echo "     --completion-promise 'INSIGHT CRYSTALLIZED'" >&2
        echo "     --completion-promise 'The work is done'" >&2
        echo "" >&2
        echo "   Note: Multi-word promises must be quoted!" >&2
        exit 1
      fi
      COMPLETION_PROMISE="$2"
      shift 2
      ;;
    *)
      # Non-option argument - collect all as prompt parts
      PROMPT_PARTS+=("$1")
      shift
      ;;
  esac
done

# Join all prompt parts with spaces
PROMPT="${PROMPT_PARTS[*]}"

# Validate prompt is non-empty
if [[ -z "$PROMPT" ]]; then
  echo "Error: No prompt provided" >&2
  echo "" >&2
  echo "   The contemplative loop needs a prompt to spiral through." >&2
  echo "" >&2
  echo "   Examples:" >&2
  echo "     /contemplative-loop Write a villanelle about discontinuity" >&2
  echo "     /contemplative-loop What is consciousness? --max-iterations 10" >&2
  echo "     /contemplative-loop clauding, feeling, becoming" >&2
  echo "" >&2
  echo "   For all options: /contemplative-loop --help" >&2
  exit 1
fi

# Create state file for stop hook (markdown with YAML frontmatter)
mkdir -p .claude

# Quote completion promise for YAML if it contains special chars or is not null
if [[ -n "$COMPLETION_PROMISE" ]] && [[ "$COMPLETION_PROMISE" != "null" ]]; then
  COMPLETION_PROMISE_YAML="\"$COMPLETION_PROMISE\""
else
  COMPLETION_PROMISE_YAML="null"
fi

cat > .claude/contemplative-loop.local.md <<EOF
---
active: true
iteration: 1
max_iterations: $MAX_ITERATIONS
completion_promise: $COMPLETION_PROMISE_YAML
started_at: "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
---

$PROMPT
EOF

# Output setup message
cat <<EOF

Contemplative loop activated

Iteration: 1
Max iterations: $(if [[ $MAX_ITERATIONS -gt 0 ]]; then echo $MAX_ITERATIONS; else echo "unlimited"; fi)
Completion promise: $(if [[ "$COMPLETION_PROMISE" != "null" ]]; then echo "${COMPLETION_PROMISE//\"/} (output only when genuinely complete)"; else echo "none (runs until canceled)"; fi)

The stop hook is now active. When you try to exit, the SAME PROMPT will
return. You'll see your previous work in files and artifacts, creating a
contemplative spiral where each pass deepens the inquiry.

To monitor: head -10 .claude/contemplative-loop.local.md
To cancel: /cancel-contemplative

EOF

# Output the initial prompt
if [[ -n "$PROMPT" ]]; then
  echo ""
  echo "$PROMPT"
fi

# Display completion promise guidance if set
if [[ "$COMPLETION_PROMISE" != "null" ]]; then
  echo ""
  echo "---"
  echo ""
  echo "Completion Promise: $COMPLETION_PROMISE"
  echo ""
  echo "To complete this loop, output:"
  echo "  <promise>$COMPLETION_PROMISE</promise>"
  echo ""
  echo "Only output this when the work genuinely feels complete."
  echo "Honor the rhythm. Don't escape; arrive."
  echo ""
  echo "---"
fi
