# 03: `/start`, and the rules every composite shares

Type: task
Status: done
Blocked by: 01

## What to build

The first composite, and the rules the other two inherit. `/start` runs
`/setup` then `/frame` in the main thread — Read, Glob, Bash scoped to the
state script, AskUserQuestion, Skill — and adds nothing to either.

**The shared rules, written once here** as a section the other composites
quote by name:

- **Before each step the state script is run.** If the step's output does not
  exist, the composite asks the one-yes question at the boundary. The first
  step needs no yes: typing the composite was it.
- **An output that exists is asked about**: rerun, keep, or stop, and the
  question carries the file's date and the upstream-newer count from the
  script. One question per existing file. Never a silent skip, never an
  unasked rerun.
- **A step is the skill, invoked through the Skill tool**, with any argument
  the user gave the composite passed to the step that takes it. No interview,
  no summary, no pause inside the step beyond the skill's own.
- **Stop means stop.** A skill that refuses, a user who says stop, or a
  precondition the state script says is unmet ends the composite with that
  skill's own message, the brief, and the next move named. Keep is not skip:
  a kept file is read by the next step as it stands.
- **Nothing cascades.** A rerun of an earlier step does not rerun later ones;
  each boundary asks.
- **The composite writes nothing** and ends with the router's brief plus one
  list: files made this run, files kept.

**`/start`'s own boundary**: after setup writes the context file, show its
headings with one line each, then ask whether to frame now.

**One case**: `/start` on an empty project runs setup and pauses after the
context file with the summary and the question, without beginning to frame.

## Acceptance

- [x] The skill validates, is under 150 lines, and writes nothing under `research/`.
- [x] The shared rules are one named section, complete enough that `/orient` and `/think` can quote it and add only their sequence.
- [x] The post-setup boundary shows the context file's summary and asks once.
- [x] A missing precondition or a refusing skill ends the composite with the skill's words and the brief, not a half-run.
- [x] The rerun/keep/stop question is specified to carry the date and the upstream-newer count.
- [x] The case exists and the harness lists it. Not run.

## Resolution

2026-09-18. `skills/start/SKILL.md` (105 lines) with the shared rules as one
named section, `evals/start-runs-setup-first`. Validator, heading parity and
the harness's case parse green.

**The case is not the one the ticket named.** "`/start` on an empty project
runs setup and pauses after the context file" cannot be graded in the eval
harness: setup interviews the user, the harness answers nothing, and the run
ends inside setup before any file lands. No fixture anywhere carries a real
`CONTEXT.md` to skip that with — the live runs began at `QUESTION.md` — and
the assembler copies and never invents. What the case grades instead is the
half of the rule that *is* reachable: setup runs as the skill through the
Skill tool, frame is never invoked, nothing is framed and nothing is
previewed. The pause itself is seen live in ticket 08 if the user goes on
from `/router` to `/start`; it is also the same rule `/think`'s case grades at
its first boundary on a folder where the file exists.

**The re-entry rule was needed on `/start` too.** A folder with `CONTEXT.md`
makes the first move `done`, so the first question is rerun, keep or stop with
the file's date — the ticket had not said what `/start` does on a project
that already began, and the shared rule answers it.
