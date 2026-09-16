# 10: `/bits`

Type: task
Status: ready-for-agent
Blocked by: 03

## What to build

`/bits` (Read, Glob, Write, Edit), no agents. Reads the matrix, the time
slice, every card, and the datasets ledger if it exists. Writes the bits file
from a new template with two parts. Groups: on the first run, cards grouped by
shared thesis using the delta sentences and matrix positions, recorded with
card slugs per group; on later runs the recorded groups are read first, new
cards assigned where they fit, a new group proposed only for cards that fit
none and marked as new in that run; a group is never dissolved. Bits: one per
group with two or more cards: the assumption in one sentence, the cards behind
it, the matrix cells they sit in, and whether it is a method, evaluation or
dataset assumption. A group with one card is listed as too thin. Evaluation
and dataset bits draw on the dataset and split fields and the ledger.

## Acceptance

- [ ] Plugin validation green; heading parity green for the bits template.
- [ ] On the existing cards, the file has recorded groups covering every card, one bit per group of two or more with cells named, and thin groups listed.
- [ ] A second run with one new card added keeps every existing group and bit unchanged and either assigns the card or adds a group marked new.
- [ ] At least one bit is an evaluation or dataset assumption when the cards share a split or benchmark.
