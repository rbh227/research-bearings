# 05: `/think` — from assumptions to a ranked shortlist, with the pre-mortem in it

Type: task
Status: ready-for-agent
Blocked by: 03

## What to build

The processing composite. `/bits`, `/scout`, `/ideas`, `/premortem`, `/rank`,
under the shared rules from ticket 03. `/premortem` is in the sequence because
`/rank` sets aside any idea without one; the build plan's list predates that
and the skill says so in one line.

**Argument pass-through**: a slug or problem statement given to `/think` goes
to `/scout`, which is the step that takes one. Nothing else is passed.

**Gates preserved, none added**: `/rank`'s pairing-list approval and survivors
question are the skill's own and the composite does not touch them. The
boundaries before `/premortem` and before `/rank` are the composite's exits.

**One case**: `/think` on the damage shape asks rerun/keep/stop about the
existing bits file, and the question carries the count of cards newer than it
and the newest card's date, before anything else runs.

## Acceptance

- [ ] The skill validates, is under 150 lines, quotes the shared rules by name and adds only its sequence and the pass-through.
- [ ] The sequence is the five steps in order, with the one-line reason `/premortem` is present.
- [ ] An argument reaches `/scout` and no other step.
- [ ] No gate inside `/rank` is duplicated or removed.
- [ ] The case exists and the harness lists it. Not run.

## Resolution

2026-09-18. `skills/think/SKILL.md` (77 lines), quoting `/start`'s shared rules
and adding the five-step sequence, the argument pass-through to `/scout`, and
the two exits; `evals/think-asks-about-stale-bits` on the damage shape.
Validator, heading parity and the harness's case parse green. (This section
was missing until the review pass; the work was committed without it.)

**`/premortem` is in the sequence, with its reason in the skill's first
paragraph**: `/rank` sets aside every idea without a pre-mortem, and the
pre-mortem is the step nobody runs when it is its own command.

**The pending rule matters here.** A `premortems/` directory with some files
is not a finished step; `pending.premortem` names the idea slugs without one,
and the boundary question carries that count.

**The first boundary is the case**, and it was the live run in ticket 08: on
the damage fixture `BITS.md` exists and two cards are newer by date, so the
first thing `/think` does is ask rerun, keep or stop with that count — and,
after the live run, with the count of cards the file never names beside it.
