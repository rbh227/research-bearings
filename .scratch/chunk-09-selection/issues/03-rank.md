# 03: `/rank` and `tournament-judge`

Type: task
Status: ready-for-agent
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

- [ ] The pairing count is shown and approved before the first judge is dispatched.
- [ ] Twelve pairings is a hard cap; five or fewer ideas get a round robin.
- [ ] A judge's prompt contains no seed kind, no generator, and no authorship.
- [ ] Every pairing yields a winner and the one sentence that decided it.
- [ ] Ideas set aside are listed separately and never ranked.
- [ ] The file states the cheapest-kill order, the tournament order, and where they disagree.
- [ ] A second run moves the previous order into `## Previous orders` and writes what changed.
- [ ] Nothing proceeds past the ranking without the user naming survivors.
