# <title>

<!-- Written by the scorer agent at the end of a /research-bearings:read run,
     from the reader's and the predictor's notes. One paper, one file, at
     research/papers/<slug>.md. Twelve headings, fixed.

     Everything here is the reader's, copied: the scorer scores predictions and
     writes ## What was non-obvious, and authors no claim about the paper that
     the reader did not make. Sections a later skill fills carry `_not run_`
     until it runs, so the heading is always present and its absence is never
     mistaken for a finding. -->

## Identity

<!-- One line each, every line present even when the value is unknown:

     - Slug: <first-author-year-firstword>
     - Authors: <all, or first three and "et al.">
     - Year: <YYYY>
     - Venue: <as the index has it, or _preprint_>
     - Ids: arXiv `<id>` · DOI `<doi>` · S2 `<id>`      (those it has)
     - Code: <url> — runs: yes | no | not tried | none found
     - Read: <date> · pass <1|full> · text: fetched | abstract only
     - Fetched from: <url the text came from, or _no open-access text_> -->

## Matrix position

<!-- - Formulation: <the row it sits in>
     - Data regime: <the column>
     - Cell: `<formulation> × <data regime>` — research/landscape/matrix.md

     Or the single line `_unplaced_` and why: no matrix when this was read, or
     the paper appears in no cell. /read --place fills it later. Never guessed
     by the reader from the paper alone: a card that disagrees with the
     landscape is worse than one that admits it does not know. -->

## Delta

<!-- One sentence, the Mensh and Kording form, and nothing else:

     Compared to <nearest prior work>, this changes <X> and gets <Y>.

     If that sentence cannot be written from the paper, this section says
     `_cannot be written_` and one sentence on what is missing. That is a
     finding: a paper whose delta cannot be stated is not understood, and the
     card says so rather than papering over it. -->

## Bit flipped

<!-- The assumption this paper's cluster shares that this paper breaks, in one
     sentence, or `_none_` — most papers flip nothing, and saying so is the
     honest answer. Ré's bit. /bits reads this. -->

## Not compared against

<!-- One line per baseline a reader would expect and did not find, with one
     clause on why it matters. `_nothing obvious_` when the comparison set is
     complete. This is the section reviewers write and authors do not. -->

## Kill experiment

<!-- The experiment that would have falsified the paper's central claim, and
     whether the authors ran it:

     - Experiment: <what it is>
     - Run: yes — <what it showed> | no | partly — <what was missing>

     If the paper's own ablation is the kill experiment, say so. -->

## Data and split

<!-- - Dataset: <name(s)>
     - Split: <the protocol as stated, in the paper's words>
     - Seeds and variance: <how many seeds, what spread, or _single seed_ / _not stated_>
     - Metric: <the headline metric and what it is computed over>

     Copied from the paper, not judged here. /audit judges it. -->

## Reproduction

<!-- - Status: reproduced | self-reported | contested | unknown
     - Evidence: <who reproduced it and where, or what makes it contested>
     - Reimplementable in an afternoon: yes | no — <one clause> -->

## What to steal

<!-- The one thing worth taking into your own work: a trick, a loss, an
     evaluation protocol, a way of framing the problem. One or two sentences.
     `_nothing_` is allowed and is a real answer. -->

## Same-cell comparison

<!-- The reader's check against the other cards in this cell, one line per
     sibling card:

     - <sibling slug> — compatible | incompatible: <what conflicts, in one clause>

     `_no matrix_` when the card is unplaced, `_no siblings_` when the cell
     holds only this card, `_not run_` for a skim. An incompatibility is a
     finding, not an error to resolve here: PaperQA2's contradiction detection,
     at read time, while the reader already has the cell. -->

## Prediction score

<!-- Written by the scorer, from the prediction note, three lines and a fourth:

     - Method: <1-5> — <what the prediction got wrong, in one clause>
     - Main result: <1-5> — <same>
     - Weakest point: <1-5> — <same>

     `_not run_` for a skim, which commits no predictions. Scores are the
     scorer's judgment, the way the concession ladder scores a rebuttal.

     The pass is NOT repeated here. It lives on the `- Read:` line under
     ## Identity and nowhere else. Measured 2026-09-16: with the pass in two
     places, the first card written said `pass full` in one and
     `Pass stopped at: 1` in the other, and both looked authoritative. -->

## What was non-obvious

<!-- One sentence, from the lowest-scored prediction: the thing a careful
     first reading would have got wrong. This is the line the three-agent
     protocol exists to produce, and it is the reason the predictor never
     sees past the introduction.

     `_not run_` for a skim. -->

## Reviews

<!-- Filled by /research-bearings:reviews. `_not run_` until it does.
     Ratings, the objections that recur across reviewers, what the authors
     conceded, the decision, the venue and the date probed. A paper with no
     OpenReview record gets one dated line saying so. -->

## Leakage

<!-- Filled by /research-bearings:audit. `_not run_` until it does. One line
     per Kapoor and Narayanan leakage type, each with a quoted passage or
     "could not determine, checked <what>". -->

## References

<!-- Every paper this card names, one per line, in the landscape line shape,
     each carrying the tag /verify wrote:

     - <title> · <year> · S2 `<id>` · verified
     - <title> · <year> · _candidate: prefix match only, <nearest title> (S2 `<id>`)_
     - <title> · <year> · _not found: checked s2, openalex, crossref_

     A reference with no tag is a check_cards failure. The tag is how a
     fabricated citation is caught before /bits or /ideas builds on it. -->

## Status

<!-- Date, the run that wrote it, and what has not been run. The pass is on
     the `- Read:` line under ## Identity; do not restate it here.
     Read <date> by /read. Reviews: not run. Leakage: not run. -->
