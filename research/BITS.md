# Bits: post-disaster building damage assessment from aerial and satellite imagery

## Groups

- Joint pre/post modelling on one benchmark — the thesis that damage is read from a pre/post image pair, and that the contested design question is how the two captures are brought together: gupta-2020-rescuenet, shen-2021-bdanet (since 2026-09-16; thesis narrowed 2026-09-16 after critique, which found the earlier wording "one network trained end to end" contradicted shen-2021-bdanet's own card)
- The benchmark itself — the thesis that the field's problem is a labelling and dataset problem before it is a modelling one: gupta-2019-xbd (since 2026-09-16)

## Bits

### Damage is read from a pre/post image pair, and what is argued about is how the two captures are brought together

- Kind: method
- Group: Joint pre/post modelling on one benchmark
- Cards: gupta-2020-rescuenet, shen-2021-bdanet
- Cells: `per-building damage classification × paired pre/post satellite (xBD, xView2)` (both)
- Evidence:
  - gupta-2020-rescuenet — its delta argues about the number of stages: "two-stage pipelines… not end-to-end trainable" replaced by "a single end-to-end trainable pixel-level segmentation model that jointly segments buildings and classifies per-building damage".
  - shen-2021-bdanet — its delta argues about the fusion operation, attributing each to its paper: "a single fixed operation — concatenation (Weber et al. [12]) or subtraction (RescueNet [14])" replaced by cross-directional attention. **BDANet is itself two-stage**, by its own card, so the two papers do not share an architecture; what they share is the pre/post pair as the input and a disagreement about how it is combined.
- Flipped by: nothing in these cards. One argues about stages and one about fusion; neither questions that a pre/post pair is the thing a model reads.

### What a model is measured on is the standard split of one dataset

- Kind: evaluation
- Group: Joint pre/post modelling on one benchmark
- Cards: gupta-2019-xbd, shen-2021-bdanet, gupta-2020-rescuenet
- Cells: `per-building damage classification × paired pre/post satellite (xBD, xView2)` (all three)
- Evidence:
  - gupta-2019-xbd — defines the split and says what it is for: "xBD is provided in train, test, and holdout splits in a 80/10/10% split ratio… meant to facilitate the xView 2 challenge."
  - shen-2021-bdanet — reports Train and Test only, with counts matching the release's exactly, and never mentions the holdout partition.
  - gupta-2020-rescuenet — names xBD and trains on it. Its split field is `_not read_` (the card is a skim), so it supports this bit only as far as "measured on xBD"; it says nothing about the partition either way.
- Flipped by: nothing in these cards. The same-cell comparison on shen-2021-bdanet names the consequence directly: two papers' headline numbers on the same dataset "sit in different tables with no stated bridge between them".

## Too thin to name a bit

### Which partition of the standard split a number came from need not be stated

- Kind: evaluation
- Group: Joint pre/post modelling on one benchmark
- Cards: shen-2021-bdanet
- Cells: `per-building damage classification × paired pre/post satellite (xBD, xView2)`
- Evidence:
  - shen-2021-bdanet — Table III gives Train and Test counts that match the release's Train and Test exactly, the holdout partition goes unmentioned, and the paper never says which of the release's partitions its "Test" is.
- Flipped by: nothing in these cards.
- **n = 1. Not yet a bit.** It is carried by one card, which by this file's own rule is a paper's habit and not the field's assumption. It is written out here rather than folded into the bit above, because the two claims were one sentence until a critique separated them, and `gupta-2019-xbd` states its partition in full — the opposite case. A second card omitting its partition would promote this; a second card stating it would kill it.

- The benchmark itself — gupta-2019-xbd. Its bit, if a second card supported it, would be: *a single ordinal damage scale can be applied across disaster types from imagery alone*, replacing binary labels and the in-person, disaster-specific scales (HAZUS, FEMA's manual) that "require on-site attributes… that cannot easily be determined from satellite imagery". One card is the paper's design choice; a second card adopting or contesting the Joint Damage Scale would make it the field's assumption.

## Status

2026-09-16. Cards read 3. Groups 2 (2 new this run, 0 existing — this is the
first run and it records the grouping for later runs to reuse). Bits written
2. Groups too thin 1.

The two bits above come from a group of two or more cards, which is the
minimum. The second reaches across both groups for its evidence because all
three cards report on xBD; it is filed under the group whose cards *depend* on
the split for a headline number. A third candidate is written out at n = 1 and
is explicitly not a bit yet.

Revised 2026-09-16 against `research/critiques/BITS-2026-09-16.md`, four
findings, two adjudicated and two conceded before the ladder. The first
version claimed shen-2021-bdanet as an instance of single-network end-to-end
training, which its own card contradicts; claimed a card marked `_not read_`
as evidence about what a paper does not state; carried a two-part assumption
in one sentence whose second half rested on one card; and quoted an ellipsis
that lost which paper concatenates and which subtracts. All four are fixed
above. Groups and their membership did not change.

No group needs splitting. `/read --place` placed gupta-2020-rescuenet after it
was written, so its same-cell comparison is `_no matrix_` and its evidence
line here is thinner than the other two.
