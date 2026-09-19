# 02: `/router` — the doorman, and the fixtures the cases stand on

Type: task
Status: done
Blocked by: 01

## What to build

The front door. A skill in the main thread — Read, Glob, Bash scoped to the
plugin's state script, AskUserQuestion, Skill — that runs the state script,
prints the one-screen brief, names the next move with the precondition it
checked, asks once, and on yes invokes that skill through the Skill tool with
any argument the user gave.

**Three rules, in order.** A stated goal is matched to a skill and its
precondition checked; a single next move is named with its precondition; a
fork is offered as two or three options with one reason each. One
AskUserQuestion, never more.

**A goal that cannot be met gets the precondition first.** The message names
the missing file, the skill that writes it, and offers that skill instead. It
does not preview what the refusing skill would have asked — the same rule
`/frame` applies to `/setup`.

**The on-demand skills are reachable by stated goal only.** The loop's next
move never names them.

**The description is the natural-language trigger.** It names the phrases
("what next", "where am I", "what should I do with this project") and the
condition (a `research/` folder in the project). Typed invocation unchanged.

**The brief** is one screen: what exists with dates, the counts, what is
stale, and the next move. Written here as one routine the composites will
reuse — a named section of the skill they quote, not a second copy.

**The eval scaffold.** A short shell script under the eval directory that
assembles a temp project's `research/` folder from the existing fixtures: the
damage run (question, landscape, three cards, bits, datasets, groups) and the
wildfire run (question, landscape). Cases name it; it runs only under the
harness's scaffold flag. It copies and never invents.

**Four router cases**, prompt plus graders in the existing case shape: an
empty project routes to `/start`; the wildfire shape routes to `/read` with
the matrix named as the precondition; the damage shape offers a fork and asks
once; "I want ideas" on the wildfire shape gets the precondition and the
nearest step. Router graders compare the transcript's named command against
the state script's next-moves list for the same fixture.

## Acceptance

- [x] The skill validates, is under 150 lines, and writes nothing under `research/`.
- [x] Its description names the trigger phrases and the `research/` condition.
- [x] The three rules are written in order and the skill asks exactly once before invoking.
- [x] A stated goal whose precondition is unmet produces the precondition, the writing skill and the offer, and no preview of that skill's questions.
- [x] The brief is a named routine the composites can quote.
- [x] The scaffold script assembles both fixture shapes and the state script, pointed at each, reports the expected next moves.
- [x] Four cases exist, the harness lists them, and each grader checks against the state script's output for its fixture. Not run.

## Resolution

2026-09-18. `skills/router/SKILL.md` (118 lines), `evals/fixtures/assemble.sh`
with its README, four cases under `evals/router-*`, each with a `case.yaml`
naming a `scaffold.sh` that calls the assembler. Validator and heading parity
green; the assembled damage folder was checked by hand.

**The wildfire shape is a fork, not `/read`.** The ticket said the wildfire
folder routes to `/read`. On first contact the state script reported `scout`
as `ready` at the stage reached (gathering) and `read` as `ready` at the next
— both honest moves, and the ticket's single answer was mine, not the
folder's. The rule is now written as: candidates are the recommended moves at
the stage reached, stale first, the rest in loop order, cap three, plus the
first ready move of the next stage when there is room. Wildfire gives scout
and read; damage gives bits (stale, two cards newer), read, brainstorm. The
case asserts the fork.

**"I want ideas" is not the blocked case on this fixture.** The matrix's
contradictions are a seed source, so `ideas` is `ready` on a folder with a
landscape and no cards, and the router would rightly route to it. The
precondition-first case is "rank my ideas" instead: `rank` is blocked on
pre-mortems, `premortem` on idea pages, and the router walks back to `ideas`
and names the chain. That walk-back is one added line in rule 1.

**Dates are set by the scaffold, on purpose.** Git keeps no modification
times and `cp` gives every file the same minute, so the assembler stamps each
file in the order it was made, with `BITS.md` before the two newest cards. The
script's header says so and the fixtures README says where the graders'
expected numbers came from.

**Bash needs a grant at run time.** The router reads the state through the
plugin script, which is Bash, and the harness removes Bash unless granted; the
README gives the one-line run command. Written, not run.
