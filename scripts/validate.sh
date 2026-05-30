#!/usr/bin/env sh
# validate.sh — check every skill's frontmatter `description` is <= 1024 bytes.
#
# Claude.ai's skill upload form rejects descriptions longer than 1024 bytes.
# Note that em-dashes (—) are 3 bytes each in UTF-8, so a description that
# "looks" short can still be over. This script measures actual byte length.
#
# Usage:  sh scripts/validate.sh        (run from the repo root)
# Exit:   0 if all pass, 1 if any description exceeds the limit.

set -eu
LIMIT=1024
status=0
count=0

for f in skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  count=$((count + 1))
  name=$(basename "$(dirname "$f")")

  # Extract the value of the first `description:` line in the frontmatter.
  desc=$(awk '/^description:[[:space:]]/{sub(/^description:[[:space:]]*/,""); print; exit}' "$f")
  # Strip one layer of surrounding double quotes, if present.
  desc=${desc#\"}
  desc=${desc%\"}

  bytes=$(printf '%s' "$desc" | wc -c | tr -d ' ')
  if [ "$bytes" -gt "$LIMIT" ]; then
    printf 'FAIL  %5s  %s\n' "$bytes" "$name"
    status=1
  else
    printf 'ok    %5s  %s\n' "$bytes" "$name"
  fi
done

echo "----"
echo "Checked $count skills (limit ${LIMIT} bytes)."
if [ "$status" -eq 0 ]; then
  echo "All descriptions within limit."
else
  echo "Some descriptions exceed the limit — trim them before uploading to claude.ai."
fi
exit "$status"
