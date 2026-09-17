# 09: the docs and the chunk note

Type: task
Status: done
Blocked by: 08

## What to build

- **`CONTEXT.md`**: an ideation section for chunk 8 — seed, seed kind,
  candidate, increment, promoted, abandoned direction, persona, warrant, round,
  typicality note, running log. One meaning each, in the voice of the existing
  sections.
- **`README.md`**: `/brainstorm` and `/ideas` from planned to built, with the
  one-line description each; the agent count and the skill list line updated.
- **`docs/design/skills-and-agents.md`**: Stage 4 marked built, the two
  decisions this chunk made recorded (the mechanical diversity rule, personas
  from the record), and the two stale `/flip` lines corrected — chunk 3
  absorbed `/flip` into `/scout`, and flipping a bit is a seed kind inside
  `/ideas`.
- **`.claude-plugin/plugin.json`**: version 0.8.0.
- **`research_plugin_build_plan.md`**: Milestone 4's status line, in the shape
  of Milestone 3's — what shipped, where the chunk note is, the departures, and
  that the live test has not been done.
- **`docs/design/chunk-08-ideation.md`**: the chunk note, in the shape of
  `chunk-07-understanding.md` — decision record, what ships, done-check, what
  the dry runs found, what is not done.

## Acceptance

- [x] All four checkers and the guard selftest green: `check_headings`, `check_cards`, `check_analogs`, `check_landscape`, `check_ideas`, `guard --selftest`.
- [x] README's skill list and counts agree with what the repo actually holds.
- [x] No `/flip` line in the design doc claims a skill that does not exist.
- [x] The chunk note says plainly what was not tested.

## Resolution

2026-09-16. `CONTEXT.md` (§ Ideation terms, twelve entries),
`README.md`, `docs/design/skills-and-agents.md`, `.claude-plugin/plugin.json`
(0.8.0), `research_plugin_build_plan.md` (Milestone 4 status),
`docs/design/chunk-08-ideation.md`.

All five checkers, the guard selftest and `claude plugin validate .` green.

The two stale `/flip` lines are gone: the Stage 4 log line now names the two
skills that append, and the source table's row does too. The `/scout` row's
mention stays — that one is the record of the absorption, not a claim that the
skill exists.

The chunk note's § 5 says plainly what is untested: neither skill has been run
end to end, the stop rule has never triggered, and round two has never read a
section.
