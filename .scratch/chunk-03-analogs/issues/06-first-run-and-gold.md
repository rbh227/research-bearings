# First real run, the user's read, and the breadth heading in the gold set

Type: task
Status: ready-for-human
Blocked by: 04, 05

## What

Spec §6.2–6.3. Outside this repo, on the acceptance topic, with the user's
key: `/setup` if needed, `/frame` or not (both paths are valid; note which),
then `/scout`. The user reads `research/analogs/<slug>.md` cold and answers
two questions in writing, appended to this ticket: did an analog of the
farming-from-the-air kind show up, and are the transfer arguments worth
anything. `check_analogs.py` runs on the file first.

Before the run, `evals/gold/wildfire-cv.md` gains a heading — *Work from
another field that turned out to matter to me* — and the user fills it from
memory. After the run, the count of those entries whose field appears in the
file is recorded in the chunk 3 spec as the first breadth-recall number.

## Acceptance

- [ ] The gold set has the heading, filled before the run, untouched after.
- [ ] `check_analogs.py` green on the output.
- [ ] The user's two answers are on this ticket, dated.
- [ ] The breadth-recall number is in the spec, with the run's slug and date.
- [ ] Map updated: chunk 3's state, and what the read says to change.
