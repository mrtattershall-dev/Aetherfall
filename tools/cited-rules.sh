#!/bin/sh
# Step 0 of the handoff: the ids the build actually cites.
#
# Diff this against the ids in docs/RULES_INDEX.md. The dangerous direction is
# "cited in code but NOT indexed" — rules the build enforces that the index does
# not contain. That gap went unmeasured for four versions once already
# (RULES_INDEX_ADDENDUM_0_7_0_SECTION.md), so it is worth one command.
#
#   ./tools/cited-rules.sh                 # list them
#   ./tools/cited-rules.sh | wc -l         # count them
#   comm -23 "$(./tools/cited-rules.sh > /tmp/cited; echo /tmp/cited)" \
#            <(grep -o 'AF-R-[0-9]\{3,4\}' docs/RULES_INDEX.md | sort -u)
#
set -eu
BUILD="${1:-aetherfall.html}"
grep -o 'AF-R-[0-9]\{3,4\}' "$BUILD" | sort -u
