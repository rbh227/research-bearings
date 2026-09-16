# Bits: post-disaster building damage assessment from aerial and satellite imagery

## Groups

- Joint pre/post modelling on one benchmark — the thesis that damage is read from a pre/post image pair by one network trained end to end on xBD: gupta-2020-rescuenet, shen-2021-bdanet (since 2026-09-16)
- The benchmark itself — the thesis that the field's problem is a labelling and dataset problem before it is a modelling one: gupta-2019-xbd (since 2026-09-16)

## Bits

### Damage is a property of a pre/post image pair that one network can be trained end to end to read

- Kind: method
- Group: Joint pre/post modelling on one benchmark
- Cards: gupta-2020-rescuenet, shen-2021-bdanet
- Cells: `per-building damage classification × paired pre/post satellite (xBD, xView2)` (both)
- Evidence:
  - gupta-2020-rescuenet — its delta replaces "two-stage pipelines… not end-to-end trainable" with "a single end-to-end trainable pixel-level segmentation model that jointly segments buildings and classifies per-building damage".
  - shen-2021-bdanet — its delta keeps the pair and the end-to-end frame and argues only about *how* the two images are combined: "a single fixed operation… concatenation or subtraction" against cross-directional attention.
- Flipped by: nothing in these cards. Both flip something inside the assumption (how to fuse, how many stages); neither questions that the pair is the input or that one network is the answer.

### What a model is measured on is the standard split of one dataset, and which partition that is need not be stated

- Kind: evaluation
- Group: Joint pre/post modelling on one benchmark
- Cards: gupta-2020-rescuenet, shen-2021-bdanet, gupta-2019-xbd
- Cells: `per-building damage classification × paired pre/post satellite (xBD, xView2)` (all three)
- Evidence:
  - gupta-2019-xbd — defines the split and says what it is for: "xBD is provided in train, test, and holdout splits in a 80/10/10% split ratio… meant to facilitate the xView 2 challenge."
  - shen-2021-bdanet — reports Train and Test only, no holdout, "no split-protocol prose beyond a table caption", and does not say which of the benchmark's partitions its Test is.
  - gupta-2020-rescuenet — `_not read_`: the card is a skim, and the introduction names the dataset without the protocol. That it is *unremarkable* for an introduction to omit the protocol is itself the assumption in force.
- Flipped by: nothing in these cards. The same-cell comparison on shen-2021-bdanet names the consequence directly: two papers' headline numbers on the same dataset "sit in different tables with no stated bridge between them".

## Too thin to name a bit

- The benchmark itself — gupta-2019-xbd. Its bit, if a second card supported it, would be: *a single ordinal damage scale can be applied across disaster types from imagery alone*, replacing binary labels and the in-person, disaster-specific scales (HAZUS, FEMA's manual) that "require on-site attributes… that cannot easily be determined from satellite imagery". One card is the paper's design choice; a second card adopting or contesting the Joint Damage Scale would make it the field's assumption.

## Status

2026-09-16. Cards read 3. Groups 2 (2 new this run, 0 existing — this is the
first run and it records the grouping for later runs to reuse). Bits written
2. Groups too thin 1.

Both bits come from a group of two cards, which is the minimum. The second bit
reaches across both groups for its evidence because all three cards report on
xBD; it is filed under the group whose cards *depend* on the split for a
headline number.

No group needs splitting. `/read --place` placed gupta-2020-rescuenet after it
was written, so its same-cell comparison is `_no matrix_` and its evidence
line here is thinner than the other two.
