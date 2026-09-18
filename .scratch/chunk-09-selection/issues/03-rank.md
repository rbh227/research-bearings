# 03: `/rank` and `tournament-judge`

Type: task
Status: done
Blocked by: 02

## What to build

The bounded tournament, the Alon plot, and the cheapest-kill order.

**`templates/research/ranking.md`** — comment-only, for `research/RANKING.md`.
Headings for the pairing list and its bound, the tournament result, the Alon
grid, the cheapest-kill order, `## Set aside` (ideas whose pre-mortem said not
executable), `## Surviving` (the user's words), `## Status`, and
`## Previous orders`.

**`agents/tournament-judge.md`** — Read, Write. One pairing per dispatch. Sees
both idea pages and both pre-mortems and **nothing about who wrote them or how
they were generated**. Writes one comparison file: the winner, the single
sentence that decided it, each idea's feasibility and interest scored one to
five with the evidence line behind each score, and what would flip the result.

**`skills/rank/SKILL.md`** — Read, Glob, Write, Edit, AskUserQuestion, Agent.

**The bound is shown before anything runs.** Ideas with a pre-mortem verdict of
`not executable as written` are set aside, not ranked. Of the rest: five or
fewer get a full round robin, at most ten pairings; more than five, each idea
meets three others chosen to span different seed kinds, capped at **twelve
pairings total**. The pairing list is shown with its count and the user approves
it before any judge runs. Judges are dispatched at most six per message.

**The order is by cheapest kill, not by wins.** Wins and the Alon plot are both
written; the ordering rule is the experiment most likely to end the project
first. `RANKING.md` states the cost of each kill, orders on it, puts the
tournament result beside it, and **says plainly where the two disagree**.

The Alon plot is a five-by-five text grid, feasibility against interest, with
the hard-but-feasible region marked, drawn from the judges' scores.

**A human gate.** The skill proposes an order and asks which ideas survive; what
the user says goes under `## Surviving` in their words.

**Re-running after a result**: the previous order moves to `## Previous orders`
with its date, and `## Status` says what moved and why. `RANKING.md` is the one
file in this chunk that is overwritten, and it carries its own history inside
itself.

## Acceptance

- [x] The pairing count is shown and approved before the first judge is dispatched.
- [x] Twelve pairings is a hard cap; five or fewer ideas get a round robin.
- [x] A judge's prompt contains no seed kind, no generator, and no authorship.
- [x] Every pairing yields a winner and the one sentence that decided it.
- [x] Ideas set aside are listed separately and never ranked.
- [x] The file states the cheapest-kill order, the tournament order, and where they disagree.
- [x] A second run moves the previous order into `## Previous orders` and writes what changed.
- [x] Nothing proceeds past the ranking without the user naming survivors.

## Resolution

2026-09-18. `templates/research/ranking.md`, `agents/tournament-judge.md`,
`skills/rank/SKILL.md`. Heading parity green.

**The judge is never told the seed kind, and its contract says why.** An idea's
`## Seed` says where it came from, not what it is worth. A judge that learns a
candidate came from a persona question rather than a bit is ranking the
generator, so the skill's dispatch step lists what is withheld and the agent's
refusals table has an entry for inferring it from the page anyway.

**A tie is refused outright.** A judge that declines to pick has cost a call and
bought nothing, so closeness goes in the deciding sentence and the winner is
still named. That is also why `## What decided it` is capped at one sentence:
three reasons is a judge that has not decided which difference mattered.

**Scores are written before they are numbered.** The contract requires the
evidence line first and the one-to-five second, with the file and heading it
came from. Nothing is computed, and the grid is integers because a decimal would
be a lie about where the numbers came from — the same decision that struck
`similarity.py` in chunk 3.

**Where the two orders disagree is its own line, and it is never omitted.** When
they agree the line says they agree. Its absence and its emptiness are different
findings, and the disagreement is the whole reason both orders are written: an
idea the judges loved whose kill costs three months is the trap.

**A re-run re-runs the tournament rather than reusing it.** Only `## Order` is
preserved, into `## Previous orders`. A judge's opinion formed before a result
landed is an opinion about a different world.

**An idea with no cost line is placed last and says so.** The alternative is
inventing a cost, which puts a made-up number at the top of the thing that
decides what gets run next.
