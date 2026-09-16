# 03: `/read`, the full three-agent protocol

Type: task
Status: done
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

- [x] Plugin validation green for the skill and the three agents; heading parity green for card, prediction and reading templates.
- [x] A dry run by the implementing agent on one real paper with a matrix present produces a card that passes `check_cards`, a prediction note and a reading note beside it, a delta sentence, a prediction score and `pass: full`.
- [x] The transcript shows the proposal and the approval before any fetch, and predictor and reader dispatched in one turn with the scorer after both.
- [x] The predictor's dispatch names the intro path only; the reader's names the full path only.
- [x] Every reference line on the card carries a tag.

## Resolution

2026-09-16. `agents/predictor.md`, `agents/reader.md`, `agents/scorer.md`,
`skills/read/SKILL.md`. Heading parity green; plugin validation green.

Dry run on xBD (arXiv 1911.09296), in the damage matrix's
`per-building damage classification × paired pre/post satellite` cell.
Predictor and reader dispatched in one message, scorer after both. The card
passes `check_cards`; both notes sit beside it.

**The protocol earned its cost.** The predictor guessed an overall
classification F1 of 0.60-0.75 held back by class imbalance. The paper reports
0.2654, with the major-damage class collapsing to 0.0094, and reports
localization as IoU rather than F1 at all. Scores: method 4, main result 2,
weakest point 5. The non-obvious line came from the 2, and it is a fact about
the paper that a careful skim of the abstract would have got wrong.

Three things the run changed:

- **`pdftotext` runs in reading order, not `-layout`.** With `-layout`, both
  columns of a two-column paper land on one line, so "2. Related Work" is
  never at the end of its line and every two-column paper silently fell back
  to a page cut. Measured on xBD, which went from a page cut at 11,872
  characters to a heading cut at 3,745.
- **IEEE small caps are normalised before matching.** `pdftotext` renders a
  small-caps heading as "II. R ELATED W ORK". Measured on BDANet, which page-cut
  until a capital-space-capitals rule was applied per line.
- **The pass appears in exactly one place.** The first card written said
  `pass full` under `## Identity` and `Pass stopped at: 1` under
  `## Prediction score`, both looking authoritative. The card template no
  longer repeats it, and the scorer is told the dispatcher owns that value.
