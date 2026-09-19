#!/usr/bin/env bash
# Assemble a research/ folder from the fixtures the live runs left behind.
#
#   assemble.sh <shape> [<target-dir>]
#
# Shapes:
#   empty     nothing at all — no research/ folder
#   wildfire  QUESTION.md and the landscape from the wildfire run (no cards)
#   damage    QUESTION.md, the landscape, three cards, datasets, groups, BITS.md
#             and the critique from the damage runs
#
# The target defaults to ./research under the current directory, which is what
# the eval harness's scaffold_script gets: an empty workspace. Copies and never
# invents: every file comes from evals/landscape/runs or evals/read/runs.
#
# Dates are set here on purpose. Git keeps no modification times, so the date
# on a checked-out fixture is an artifact of checkout order, and a copy gives
# every file the same minute. The dates below follow the order the files were
# actually made in (question, surveys, landscape, cards, then bits) with one
# deliberate fact for the re-entry rule: BITS.md is dated before the two newest
# cards, so the state script reports two cards newer than it. Change these and
# the router and composite cases change with them.

set -euo pipefail

shape="${1:?usage: assemble.sh <empty|wildfire|damage> [target]}"
target="${2:-$PWD/research}"
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
evals="$(dirname "$here")"
landscape_runs="$evals/landscape/runs"
read_runs="$evals/read/runs"

stamp() {  # stamp <YYYYMMDDhhmm> <path>...
  local when="$1"; shift
  for p in "$@"; do [ -e "$p" ] && touch -t "$when" "$p"; done
}

case "$shape" in
  empty)
    rm -rf "$target"
    ;;
  wildfire)
    rm -rf "$target"; mkdir -p "$target"
    cp -p "$landscape_runs/wildfire/research/QUESTION.md" "$target/"
    cp -Rp "$landscape_runs/wildfire/research/landscape" "$target/"
    stamp 202609150900 "$target/QUESTION.md"
    stamp 202609151000 "$target/landscape/surveys.md"
    stamp 202609151200 "$target/landscape/matrix.md" "$target/landscape/timeslice.md"
    ;;
  damage)
    rm -rf "$target"; mkdir -p "$target"
    cp -p "$landscape_runs/damage/research/QUESTION.md" "$target/"
    cp -Rp "$landscape_runs/damage/research/landscape" "$target/"
    cp -Rp "$read_runs/damage/papers" "$target/"
    cp -Rp "$read_runs/damage/critiques" "$target/"
    cp -p "$read_runs/damage/BITS.md" "$target/"
    cp -p "$read_runs/damage/datasets.md" "$read_runs/damage/groups.md" "$target/landscape/"
    stamp 202609150900 "$target/QUESTION.md"
    stamp 202609151000 "$target/landscape/surveys.md"
    stamp 202609151200 "$target/landscape/matrix.md" "$target/landscape/timeslice.md"
    stamp 202609161100 "$target/papers/gupta-2019-xbd.md"
    stamp 202609161130 "$target/BITS.md"
    stamp 202609161142 "$target/papers/gupta-2020-rescuenet.md"
    stamp 202609161145 "$target/papers/shen-2021-bdanet.md"
    stamp 202609161200 "$target/landscape/datasets.md" "$target/landscape/groups.md"
    stamp 202609161231 "$target/critiques/BITS-2026-09-16.md"
    ;;
  *)
    echo "unknown shape: $shape" >&2; exit 2
    ;;
esac

echo "assembled $shape at $target"
