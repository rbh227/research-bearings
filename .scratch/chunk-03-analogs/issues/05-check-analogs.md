# `scripts/check_analogs.py` — the mechanical done-check

Type: task
Status: ready-for-agent
Blocked by: 03

## What

Spec §6.1, as one standard-library script over one file: every `- <title> ·`
line under `## Fields` carries an S2 id or `_unresolved: not found by title_`;
`## Verification`'s counts agree with those lines; no `###` field name
contains a word from the project's `## Vocabulary` (read from
`research/QUESTION.md` when present, else skipped and said so); at least five
`###` fields; none of `unexplored`, `gap`, `novel`, `nobody` anywhere.
Exit 1 with one line per failure. `--selftest` on three fixtures: a passing
file, a file with an unmarked paper line, a file with a home-vocabulary field.

Add it to the static-checks verb in `docs/agents/toolchain.md`, gated on the
file existing so a project without an analogs file is not a failure.

## Acceptance

- [ ] Selftest 3/3; the script runs clean on ticket 04's dry-run output.
- [ ] `toolchain.md` static checks include it; README's development section
      mentions it in one line.
