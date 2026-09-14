#!/usr/bin/env bash
# The full-suite verb. One invocation.
#
# Nothing here needs a network, a key, or a Bash grant. The scout's agent cases
# hand paper-scout a saved crawl (scripts/retrieval/fixtures/crawl-dmg/) and judge only what
# it writes; the one skill-level case withholds Bash so the script cannot run and
# the precondition has to refuse. Bash is gated and this machine cannot grant it
# inside the harness (chunk 1 spec §9) - so it is simply never granted, and
# every case is built to hold under that.
#
# The crawl itself is covered by `scripts/retrieval/snowball.py --selftest`, the
# fences by `hooks/guard.py --selftest`, and finding things by the gold set.
#
# Env: RUNS (default 3), JUDGE (default sonnet), TAG (default ci - set to
# `scout` to run only the chunk-2 cases), CASE (a name glob, one case at a
# time).
#
# Concurrency is pinned at 1, not left to the CLI default: two Claude children
# OOM this machine. One long invocation walking the whole suite does too - the
# 2026-09-14 full-suite run was killed for memory three cases in - which is what
# CASE is for. The suite still runs in one invocation; on this machine it
# survives better as nine, and a kill then costs one case rather than nine.
set -uo pipefail
cd "$(dirname "$0")/.."

RUNS="${RUNS:-3}"
JUDGE="${JUDGE:-sonnet}"
TAG="${TAG:-ci}"
CASE="${CASE:-}"

claude plugin eval ./ --tag "$TAG" --trust-plugin --judge-model "$JUDGE" \
  ${CASE:+--case "$CASE"} -j 1 \
  --runs "$RUNS" --ablation none --threshold 0.8 \
  --allow-tools Write Edit Agent WebSearch
