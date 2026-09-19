# 03: `/start`, and the rules every composite shares

Type: task
Status: ready-for-agent
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

- [ ] The skill validates, is under 150 lines, and writes nothing under `research/`.
- [ ] The shared rules are one named section, complete enough that `/orient` and `/think` can quote it and add only their sequence.
- [ ] The post-setup boundary shows the context file's summary and asks once.
- [ ] A missing precondition or a refusing skill ends the composite with the skill's words and the brief, not a half-run.
- [ ] The rerun/keep/stop question is specified to carry the date and the upstream-newer count.
- [ ] The case exists and the harness lists it. Not run.
