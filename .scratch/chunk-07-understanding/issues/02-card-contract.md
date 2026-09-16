# 02: The card contract

Type: task
Status: ready-for-agent
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

- [ ] A hand-written card from the template passes `check_cards`.
- [ ] Each of the five failure kinds is caught by its own case; the checker prints the file and the reason.
- [ ] The glossary has the reading section with one meaning per term.
- [ ] Heading-checker entries exist for the three templates.
