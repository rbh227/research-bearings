#!/usr/bin/env bash
# The full-suite verb. Two invocations, not one.
#
# WHY TWO. `--allow-tools` is an OPERATOR grant and nothing can subtract from
# it — a case's own `allowed_tools` does not narrow it. So a case built on a
# tool being MISSING cannot share an invocation with the cases that need it:
# the grant hands the tool back and there is nothing left to refuse.
# Measured 2026-09-13. `scout-refuses-without-snowball` scored 0.00 that way,
# with the trace showing the agent calling the very server it was supposed to
# be missing.
#
# This is the mirror of the WebSearch lesson in toolchain.md: there a MISSING
# grant made a case pass for the wrong reason; here a PRESENT one made a case
# fail for the wrong reason. Same bug — the grant is global, the case is not.
#
# Denial cases carry the `denial` tag and NOT `ci`, which is what keeps them
# out of arm 1. Any future case that tests a refusal belongs there too.
#
# Env: RUNS (default 3), JUDGE (default sonnet), JOBS (default 3), TAG
# (default ci — set to `scout` to run only the chunk-2 cases).
set -uo pipefail
cd "$(dirname "$0")/.."

RUNS="${RUNS:-3}"
JUDGE="${JUDGE:-sonnet}"
TAG="${TAG:-ci}"
JOBS="${JOBS:-3}"

# The harness gives each run a CLEAN HOME, so ~/.cache/uv is not there and every
# `uvx` server start re-resolves its whole dependency tree from the network.
# Cold start measured >30 s, which is the MCP connect ceiling: paper-search then
# never comes up and the scout correctly refuses to run, so the case fails for a
# reason that has nothing to do with the behaviour it tests. Handing the child a
# warm cache takes that start to ~1.5 s. Measured 2026-09-13.
export UV_CACHE_DIR="${UV_CACHE_DIR:-$(uv cache dir 2>/dev/null)}"
COMMON=(--trust-plugin --judge-model "$JUDGE" --mocks off --runs "$RUNS" --ablation none --threshold 0.8 -j "$JOBS")
BASE_TOOLS=(Write Edit Agent WebSearch 'mcp__plugin_research-bearings_paper-search__*')

echo "=== arm 1 (tag: $TAG) — full grant ==="
claude plugin eval ./ --tag "$TAG" "${COMMON[@]}" \
  --allow-tools "${BASE_TOOLS[@]}" 'mcp__plugin_research-bearings_s2-snowball__*'
a1=$?

echo "=== arm 2 (tag: denial) — s2-snowball withheld ==="
claude plugin eval ./ --tag denial "${COMMON[@]}" \
  --allow-tools "${BASE_TOOLS[@]}"
a2=$?

echo "arm 1 exit=$a1  arm 2 exit=$a2"
[ "$a1" -eq 0 ] && [ "$a2" -eq 0 ]
