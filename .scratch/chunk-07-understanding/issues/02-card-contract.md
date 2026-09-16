# 02: The card contract

Type: task
Status: done
Blocked by: None (can start immediately)

## What to build

The file shapes every later ticket writes or reads. A card template with fixed
headings carrying exactly the build plan's paper-card fields: identity (slug,
title, authors, year, venue, arXiv or DOI, code link and whether it runs),
matrix position (formulation, data regime, or `unplaced`), the delta sentence,
the bit it flips if any, what it did not compare against, the kill experiment
and whether it was run, dataset and split, reimplementable in an afternoon,
what to steal, reproduction status, prediction score, pass stopped at, and
three sections later skills fill: reviews, leakage, same-cell comparison, each
holding a fixed `not run` marker until filled. Reference lines use the
landscape line shape and end in `verified`, the candidate marker, or the new
`not found` tag. Two small note templates: prediction and reading.

`check_cards`: a structural checker over the papers directory in the shape of
the landscape and analogs checkers, failing on a missing heading, an empty
delta section that is not the explicit cannot-write statement, a missing pass
value, a matrix position that is neither a cell nor `unplaced`, and a reference
line with no tag. Register the three templates with the heading checker, naming
the writers (the `/read` skill and the scorer for the card; predictor and
reader for the notes; those skill and agent files may not exist yet, so the
registration lands with a note and is verified green in ticket 03). Add the
reading terms to the glossary: card, pass, intro text, full text, unplaced,
tag, review notes, leakage flag, group, thesis group, bit, critique.

## Acceptance

- [x] A hand-written card from the template passes `check_cards`.
- [x] Each of the five failure kinds is caught by its own case; the checker prints the file and the reason.
- [x] The glossary has the reading section with one meaning per term.
- [x] Heading-checker entries exist for the three templates.

## Resolution

2026-09-16. `templates/research/card.md` (16 headings), `prediction.md` (5),
`reading.md` (11), `scripts/check_cards.py` (13 cases), heading-checker
registration, and the glossary's reading section (11 terms).

Two shapes decided inside the ticket:

- **A section a later skill owns carries `_not run_`, never nothing.** An empty
  `## Reviews` and an unrun one look identical to a reader and to a grep, and
  the difference matters: one means nobody looked, the other means OpenReview
  had no record. The checker fails an empty one.
- **A full read must carry a prediction score.** If `## Prediction score` says
  `_not run_` while `## Identity` says `pass full`, either the scorer did not
  run or the pass is really 1. Both are worth failing on, because the card is
  claiming a protocol it did not go through.

Heading parity is red on purpose until ticket 03: the three registered
consumers (`agents/scorer.md`, `agents/predictor.md`, `agents/reader.md`,
`skills/read/SKILL.md`) do not exist yet. The checker names each one as a
MISSING line rather than tracebacking, which is the case its own comment was
written for.
