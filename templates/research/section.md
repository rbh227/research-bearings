# <the question, as a title>

<!-- Written by the paper-scout agent, dispatched by /research-bearings:scout.
     One question, one file, four headings, never edited by the skill that
     dispatched it. This is the record of one crawl. -->

## Question

<!-- The question exactly as the scout received it, then the mode on its own
     line: "Anchored to research/QUESTION.md" or "Unanchored — run on the
     question as typed, with no scope boundaries or vocabulary from a question
     file." -->

## Status

<!-- Date. Stop reason — one of `saturation`, `budget`, `depth` — with the
     counts behind it: papers touched, papers kept, hops, unresolvable rows.
     `budget` means the section is INCOMPLETE; say so in those words.

     Then any degradation stamps, each on its own line, or "No degradation."
       - No Semantic Scholar API key: hops rate-limited, coverage reduced.
       - This question is not retrieval-shaped: <why>. What follows is what
         search returned, which is not an answer to it.
     Console warnings scroll away. This file gets read weeks later. -->

## Papers

<!-- 25-35 cards, grouped by thesis where a grouping is visible, with a `###`
     per card and a **bold line** per group - never a heading, so that every
     `###` is a paper. Fewer is fine and honest; padding is not. One worked card:

### Building Damage Detection in Satellite Imagery Using Convolutional Neural Networks

- Joseph Z. Xu, Wenhan Lu, Zebo Li, Pranav Khaitan, Valeriya Zaytseva · 2019 · arXiv.org
- S2 `51e8e21e0e172c32719648a9282517612588d13a` · arXiv `1910.06444`
- Cited as: "Xu et al. quantified how well the models will generalize to future
  disasters by training and testing models on different disaster events, and found
  that the AUC reduces for cross-region results." — DeepDamageNet [background]
- Kept because: the cross-region generalization result is the one this question turns on.
- Missing: doi

     Line by line: title; authors, year, venue (`_no venue_` when absent);
     identifiers, omitting whichever are absent; one `contextsWithIntent`
     sentence with its citing paper and intent tag; `Kept because` — the ONLY
     scout-authored prose on a card; `Missing:` only when something is.

     The context line has two forms, and the edge's `describes` field decides
     which. `describes: this_paper` (a backward hop) is the seed's prose about
     this paper — `Cited as:`, above. `describes: origin_paper` (a forward hop)
     is this paper's prose about the seed, and reads:

- Cites DeepDamageNet as: "<sentence>" [methodology]

     A row with no Semantic Scholar record is a title-only card, marked
     `_grey literature, no S2 record — not hopped from_`. -->

## What was searched

<!-- The log the reader draws their own conclusions from, because the scout is
     not permitted to draw them (chunk-2 spec 4.11).

     - Queries run, each with its result count.
     - Seed papers, by id and title.
     - Hops: how many rounds, from how many seeds, in which directions.
     - Papers touched, papers kept, unresolvable rows.

     A query that returned zero rows belongs here too. That is a fact about the
     search. "No published work combines X and Y" is not, and does not. -->
