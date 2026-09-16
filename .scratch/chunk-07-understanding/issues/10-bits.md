# 10: `/bits`

Type: task
Status: done
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

- [x] Plugin validation green; heading parity green for the bits template.
- [x] On the existing cards, the file has recorded groups covering every card, one bit per group of two or more with cells named, and thin groups listed.
- [x] A second run with one new card added keeps every existing group and bit unchanged and either assigns the card or adds a group marked new.
- [x] At least one bit is an evaluation or dataset assumption when the cards share a split or benchmark.

## Resolution

2026-09-16. `skills/bits/SKILL.md`, `templates/research/bits.md`.

Live on the three cards. Two groups recorded, two bits written, one group too
thin, and one bit turned out to be a candidate rather than a bit.

**The groups had to be made here, not inherited.** The grilling settled "the
landscape's thesis groups"; the landscape has none. Its sections are one per
question and its matrix is formulation by data regime, so `/bits` forms them
and writes them into the file for later runs to reuse.

**Reuse verified, assignment partly.** A second pass read the recorded groups
back: both parsed, all three cards were already placed, and no card would have
started a new group. Both groups survived a full rewrite of the bits with
membership unchanged — including the one whose thesis was narrowed by a
critique, which is the "never dissolve a group" rule doing its job. **What is
not verified is a genuinely new card being assigned or starting a group marked
new**: there are three cards and no fourth, and writing a fake one to tick the
box would have tested nothing.

**One template change, found by using it.** A bit whose support is one card
while its group has several does not fit either `## Bits` (which wants two or
more) or the old `## Too thin to name a bit` (which described a group of one
card). It now belongs under the second heading with `n = 1. Not yet a bit.`
and a line on what a second card would do to it. That case arrived because a
critique separated a two-part assumption whose halves had different support.
