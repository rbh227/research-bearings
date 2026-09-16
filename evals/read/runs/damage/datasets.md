# Datasets: what is actually in the data this field trains on?

## Datasets

### xBD (xView2)

- Size: 850,736 building polygons, 22,068 images, 45,361.79 km² of imagery,
  19 disaster events — gupta-2019-xbd §6 (Dataset Analysis)
- Modality: three-band RGB satellite imagery, paired pre-/post-disaster —
  gupta-2019-xbd §5.1; shen-2021-bdanet §IV.A
- Resolution and scale: sub-0.8 m GSD (gupta-2019-xbd §5.3.3); BDANet states
  it as "a resolution of 0.8 meter per pixel," image pairs "of size 1024 ×
  1024 pixels" — shen-2021-bdanet §IV.A
- Geography: 19 disaster events, Table 1, spanning the United States
  (Hurricane Michael, Hurricane Florence, Midwest US Floods, Hurricane
  Harvey, Hurricane Matthew, Moore OK Tornado, Tuscaloosa AL Tornado, Joplin
  MO Tornado, Carr Wildfire, Woolsey Fire, Pinery Fire, Santa Rosa Wildfires,
  Lower Puna volcanic eruption), Guatemala (Fuego volcano), Mexico (Mexico
  City earthquake), Indonesia (tsunami, Sunda Strait tsunami), Nepal/India/
  Bangladesh (monsoon), and Portugal (wildfires) — gupta-2019-xbd §5.1,
  Table 1
- Annotation: "Annotation followed a multi-step process that created
  polygons and damage classifications with a web-based annotation tool that
  was developed in-house by CrowdAI" (§5.2); the first annotation round was
  followed by "a round of review to ensure consistency," then experts from
  "the California Air National Guard, NASA, and FEMA" spot-checked a random
  sample and "found that approximately 2-3% of the annotations had been
  mislabeled," which they then corrected themselves — gupta-2019-xbd §5.2,
  §5.2.3
- Split protocol: three different protocols are reported across the cards
  that use this dataset, and they disagree with each other on what counts
  as "the" split:
  - The dataset's own release, quoted: "xBD is provided in train, test, and
    holdout splits in a 80/10/10% split ratio, respectively... The test set
    is meant to be used as a fixed evaluation set during the open
    leaderboard phase of the challenge. The holdout set is purposefully not
    released during the duration of the challenge and is meant to be used
    as a private evaluation set to counter any challenge-specific gaming."
    Table 2 counts: Train 18,336 images / 632,228 polygons; Test 1,866
    images / 109,724 polygons; Holdout 1,866 images / 108,784 polygons —
    gupta-2019-xbd §6.1
  - BDANet quotes only a Train/Test partition (Table III: 18,336 images /
    632,228 polygons; 1,866 images / 109,724 polygons — matching Gupta's
    Train and Test counts exactly) and states "No holdout split, and no
    third partition, is mentioned anywhere in the paper" — shen-2021-bdanet
    §Data and split (card), citing its Table III
  - RescueNet uses neither of the above: "We use the train split of xBD to
    train and test our method as the test set annotations are not publicly
    available yet... The training data is divided by the original authors
    into Tier1 and Tier3 data... We split off about 10% of the Tier1 data
    into a validation set using stratified sampling across disaster events
    to ensure a representative sample. Our models are trained on the Tier 1
    and Tier3 Train set and tested on the Tier1 validation set." Table I
    sizes: Tier1 Train 2,495 image pairs; Tier3 Train 6,369; Tier1
    Validation 304 — gupta-2020-rescuenet §IV (arxiv-2004.07312 full text;
    the card marks this section "not read" from a skim pass, so this quote
    comes from the fetched full text directly, not from the card)
- License: could not determine, checked huggingface, github
- Host: could not determine, checked huggingface, github — both hosts
  return only third-party mirrors and downstream code repositories, not the
  dataset's own release page. Sampled rows: GitHub `michal2409/xView2` (61
  stars, MIT, last updated 2023-10-03) and `prs-eth/xbd-s12` (26 stars, MIT,
  last updated 2026-04-22) are code built on top of xBD, not the dataset
  itself; Hugging Face `aryananand/xBD` (563 downloads, no license field)
  and `DrNerd/xBD-Training-Data` (65 downloads, license field says
  `apache-2.0`) are unofficial re-uploads by accounts unrelated to the
  paper's authors or to Maxar/DigitalGlobe, so their license fields are not
  treated as the dataset's own license here
- Who uses it: gupta-2019-xbd, shen-2021-bdanet, gupta-2020-rescuenet
- Known flaws:
  - Severe class imbalance: pooled damage-class counts are No damage
    313,003-313,033 (the two papers' counts differ by 30 in the low digits),
    Minor 36,860, Major 29,904, Destroyed 31,560; "no damage" has "more than
    eight times the representation of the other classes" — gupta-2019-xbd
    §Data and split; shen-2021-bdanet Table IV
  - Approximately 2-3% of annotations were found mislabeled on post-hoc
    expert review (see Annotation, above) — gupta-2019-xbd §5.2.3
  - At the time RescueNet was written, the official Test split's
    annotations were not public ("the test set annotations are not
    publicly available yet"), which forced that paper to build its own
    validation split out of Train rather than use Gupta's Test/Holdout —
    gupta-2020-rescuenet §IV
- Leakage of the standard split: not assessed — /audit a card that uses it

## Named but not found

None. The only dataset name the three cards carry is xBD (also called
xView2); both hosts returned rows for it, so nothing in this run falls into
this bucket. This is not the same as saying xBD has a canonical host record
on either service — see the Host line above.

## What was searched

- `xBD`, context `building damage satellite`, run 2026-09-16: GitHub
  returned 25 total rows (5 sampled in the response); Hugging Face returned
  5 rows. All rows were read; none was dropped as an obviously different
  project (unlike the field's own worked example of an Xbox diagnostic tool
  named "XbDiag" for a bare "xBD" query — this run's `--context` avoided
  that).
- Key states: `HF_TOKEN` not present, `GITHUB_TOKEN` not present (checked
  via the shell environment and confirmed by the verb's own `"keyed":
  false` field on both host responses). Unauthenticated GitHub search runs
  at 60 requests/hour rather than 5,000/hour with a token; this run made one
  GitHub call and did not approach that limit.

## Status

Date: 2026-09-16. Cards read: 3 (gupta-2019-xbd, shen-2021-bdanet,
gupta-2020-rescuenet). Datasets named: 1 (xBD / xView2). Rows written: 1.
Rows with at least one `could not determine` line: 1 (License and Host on
xBD). Web search was not used and is not available to this agent.
