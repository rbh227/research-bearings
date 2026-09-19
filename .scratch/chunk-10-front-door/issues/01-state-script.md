# 01: The state script — the loop written down as data

Type: task
Status: done
Blocked by: —

## What to build

The one seam this chunk adds. A plugin script that reads a `research/` folder
and prints, as JSON, what exists, what is stale, and what comes next. The
router and the three composites read it and nothing else; a grader can check
the router's words against it.

**Standard library only**, JSON on stdout, in the shape of the run ingester: a
module docstring saying what each field is for, a `main()` over one directory
path (default: the current project's `research/`), and `--selftest`.

**The dependency table is the whole program.** One table, in the loop's order,
from each contract file to the skill that writes it, the files it reads, and
its precondition in one sentence. Every loop command is a row: setup, frame,
surveys, landscape, scout, read, datasets, groups, bits, brainstorm, ideas,
premortem, rank, spec, baseline, design, log, result. The on-demand skills
(verify, audit, critique, reviews, replicate) are rows flagged on-demand so the
router can find them by stated goal and never names them as the next move.

**Per contract file it reports**: present or absent; the date; for a present
file, whether the template's required headings are all there
(`present-but-malformed` when not, never `absent`); for a derived file, the
count and newest date of upstream files newer than it. Counts for the
directory-shaped outputs: cards, analog pages, idea pages, pre-mortems,
experiment pages, results.

**Next moves**: every command whose preconditions are met, in the loop's
order, each carrying the precondition named and whether its output already
exists. A fork is two or more rows at the same stage. No `research/` folder is
the empty state and routes to setup.

**States, not errors.** A file whose date cannot be read reports `unknown`. A
template that cannot be found reports so and the file is checked for presence
only. Nothing here guesses.

**Never writes.** Not to the folder it reads, not anywhere.

## Acceptance

- [x] `python3 scripts/state.py --selftest` is green over fixture folders built in a temp dir: empty; context only; framed; framed with a landscape; the damage shape (cards, landscape, a bits file older than the cards); a present-but-malformed file; a folder with an unreadable date.
- [x] The selftest asserts the JSON shape, the next-moves list and the staleness counts, never internals.
- [x] The damage shape yields a fork (read and bits at least) and a positive upstream-newer count on the bits file with the newest card's date.
- [x] A file missing a required heading reports `present-but-malformed`, and the next-moves list names the skill that writes it as a repair, not a rerun.
- [x] The selftest snapshots the fixture tree before and after and asserts no write.
- [x] The script runs on a folder named as its argument, so the eval scaffold and the chunk's live run can point it at fixtures.
- [x] The static-checks verb and the guard selftest still pass; the guard admits the new script for any agent that might one day call it, as it admits the ingester, with no other fence change.

## Resolution

2026-09-18. `scripts/state.py`, 27 selftest cases green; one guard case added
(134 green); the toolchain's one-test-file verb now runs the state selftest.

**The table has six statuses, not the four the spec sketched.** `ready`,
`stale`, `done` and `blocked` were planned. Two more turned out to be needed on
the first fixture: **`repeat`**, for a command whose output is a directory that
grows — `read` with three cards is not done, it is repeatable, and calling it
`done` would have hidden the loop's most common move — and **`skipped`**, for a
required upstream file that is absent while a later stage has output. The
damage fixtures have no `CONTEXT.md` and a full processing stage; without
`skipped`, `setup` would have been the recommended move on a folder three
stages past it. Skipped files go under `repairs` as `missing upstream`, beside
the malformed ones.

**A malformed file satisfies presence.** `present-but-malformed` counts as
present for every precondition, so a hand-written `QUESTION.md` with two of
eleven headings lets `surveys` run, and the file is listed under `repairs`
with the skill that writes it. The alternative — treating it as absent — would
route to a rerun of `frame` over a file someone wrote on purpose.

**Pre-mortems are pending per idea.** `premortem` stays `ready` while any idea
page has no `premortems/<slug>-*.md`, and `pending.premortem` names the slugs.
A directory-shaped output that "exists" said nothing useful here.

**First contact with the real damage fixtures found a scaffold rule, not a
script bug.** Copying the fixtures with `cp` gave every file the same minute,
so `BITS.md` had zero newer cards and `matrix.md` was stale behind a
`surveys.md` copied after it. Git keeps no dates, so any date on a checked-out
fixture is an artifact of checkout order. The scaffold in ticket 02 must set
dates deliberately and say so. On the assembled folder the script reported
`stage_reached: processing`, one repair (`CONTEXT.md` missing upstream), three
cards, and recommended landscape, scout, read, brainstorm, ideas, baseline —
every one a defensible move, which is why the router (ticket 02) prefers the
stage reached and takes the first three.
