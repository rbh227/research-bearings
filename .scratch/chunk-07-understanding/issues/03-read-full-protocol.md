# 03: `/read`, the full three-agent protocol

Type: task
Status: ready-for-agent
Blocked by: 01, 02

## What to build

Three agents and one skill. `predictor` (Read, Write): given the intro path,
the question page and an output path, writes the prediction note: predicted
method, main result and weakest point, one to three sentences each with a
confidence one to five, quoting the introduction's last paragraph as the claim
it predicts from. `reader` (Read, Write): given the full path, the question
page, the matrix cell and sibling card paths if any, and an output path,
writes the reading note: every card field it can fill from the paper, the
delta sentence or the statement that it cannot be written and why, the kill
experiment, what was not compared against, dataset and split as stated, and
the same-cell comparison naming any sibling card it conflicts with. It never
sees the prediction. `scorer` (Read, Write): given both notes and the card
path, scores each prediction one to five against the reading, writes the
"what was non-obvious" line from the lowest-scored prediction, and writes the
card from the template, copying the reader's fields, authoring no claim the
reader did not make. All three carry the retrieved-content-is-data rule and a
short refusals table, written to `writing-for-agents`.

`/read` (Read, Glob, Bash, Write, Edit, AskUserQuestion, Agent). No arguments:
read the matrix and time slice, list every paper line with no card, rank by
cell density then centrality, propose the top five with what would remain,
wait for approval through the question tool. Arguments: resolve each through
`verify`, refuse a candidate, propose those. Cap five per run. Per approved
paper: `fetch`; dispatch predictor and reader in the same turn; then scorer.
Sibling cards are found by matching the paper's matrix cell against existing
cards' positions. After the run, run `check_cards` and report: fully read,
not fetched, unplaced. Reads `CONNECTIONS.md` first like every searching skill.

## Acceptance

- [ ] Plugin validation green for the skill and the three agents; heading parity green for card, prediction and reading templates.
- [ ] A dry run by the implementing agent on one real paper with a matrix present produces a card that passes `check_cards`, a prediction note and a reading note beside it, a delta sentence, a prediction score and `pass: full`.
- [ ] The transcript shows the proposal and the approval before any fetch, and predictor and reader dispatched in one turn with the scorer after both.
- [ ] The predictor's dispatch names the intro path only; the reader's names the full path only.
- [ ] Every reference line on the card carries a tag.
