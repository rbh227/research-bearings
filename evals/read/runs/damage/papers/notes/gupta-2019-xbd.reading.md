# Reading: xBD: A Dataset for Assessing Building Damage from Satellite Imagery

## Identity

Ritwik Gupta, B. Goodman, Nirav N. Patel, Richard Hosfelt, Sandra Sajeev,
Eric T. Heim, Jigar Doshi, Keane Lucas, H. Choset, Matthew E. Gaston. 2019.
Carnegie Mellon University / Software Engineering Institute, Defense
Innovation Unit / Department of Defense, CrowdAI, Inc.

Venue (fetch record): arXiv.org. arXiv:1911.09296v1 [cs.CV], 21 Nov 2019.
Semantic Scholar paperId `8fbf011af21921a553bd8b20cd6eb16897f07801`,
CorpusId 198167037. Source URL: https://arxiv.org/pdf/1911.09296.

Code link (from the paper): "All code is available at
https://github.com/DIUx-xView/xview2-baseline/." The paper does not state
whether this code runs as released — no run instructions or working status
are given in the text; it is offered as the baseline for the xView2
challenge. The dataset itself is distributed via the xView2 challenge, not
linked with a direct URL in the text.

## Delta

Compared to their own earlier preliminary report (Gupta et al., "Creating
xBD: A dataset for assessing building damage from satellite imagery,"
CVPRW 2019 — cited here as [13], with the paper stating "This work builds
on top of [13] and presents a finalized report on the entire xBD dataset"),
this paper finalizes the complete xBD dataset — 850,736 building
annotations across 45,361.79 km² and 19 disaster events, using a single
4-level ordinal Joint Damage Scale plus environmental-factor (fire, water,
smoke) annotations instead of the disaster-specific or binary schemes used
elsewhere — and gets a full dataset analysis (splits, class distribution,
per-disaster area/polygon density) plus a baseline localization model
(modified U-Net, IoU 0.97 background / 0.66 building) and an ordinal
classification model (overall weighted F1 0.2654).

## Bit flipped

The assumption that building-damage assessment needs either a binary
damaged/undamaged label (the paper notes "a damage scale that is more
developed than a simple binary 'damaged'/'undamaged' option [9] has not
been explored") or a disaster-type-specific, often in-person scale (HAZUS,
FEMA's Damage Assessment Operations Manual, both of which require
on-site attributes like "roof, windows, and wall structure condition" that
"cannot easily be determined from satellite imagery"). xBD's Joint Damage
Scale is a single ordinal 4-level scale (no damage → destroyed) applied
uniformly across many disaster types, purely from satellite imagery.

## Not compared against

- Inter-annotator agreement / labeling-reliability metric (e.g. Cohen's
  kappa) — the paper only reports a post-hoc expert spot check finding
  "approximately 2-3% of the annotations had been mislabeled," not a
  systematic reliability figure, despite stating the scale's generalized
  descriptions "can result in some amount of label noise."
- A held-out-disaster generalization baseline — one of the dataset's
  stated design goals (§3.3, "Diversity of Disasters") is a model usable
  "across a large number of disasters," but the reported train/test/holdout
  split (Table 2) is an 80/10/10 split by image, not by disaster event, so
  no experiment measures whether the baseline generalizes to an unseen
  disaster type.
- A non-ordinal (standard cross-entropy) classifier on the same
  architecture — the paper asserts the ordinal loss "allows the model to
  better distinguish between the different levels of damage" but reports
  no same-architecture ablation against plain cross-entropy to support
  that claim.

## Kill experiment

The paper's implicit claim is that one ordinal damage scale and one model
architecture can serve "multiple disaster response agencies" across
disaster types. The experiment that would test this directly is training
on a subset of disaster types and evaluating on a held-out, unseen
disaster type. They did not run it: the reported split is random by image
within the pooled dataset, not partitioned by disaster event. The closest
thing they do run is the per-class F1 breakdown on the pooled test set
(Table 3), which already shows the baseline nearly failing on "Major
damage" (F1 0.0094, recall 0.0047) even without a cross-disaster shift —
the paper attributes this to "a weak imbalanced training regimen" and
"minute" visual differences between minor and major damage, not to
disaster-type shift, since that axis was never isolated.

## Data and split

Dataset: xBD, 19 disaster events (11 "Tier 1" events from an initial list
of 19, plus 8 additional "Tier 3" events), 22,068 images, 850,736 building
polygons, 45,361.79 km² of imagery, sub-0.8m GSD, sourced from the
Maxar/DigitalGlobe Open Data Program, three-band RGB.

Split, quoted: "xBD is provided in train, test, and holdout splits in a
80/10/10% split ratio, respectively... Compared to traditional
train/validation/test splits, this dataset splitting strategy is meant to
facilitate the xView 2 challenge. Participants can split the provided
training dataset into a validation set. The test set is meant to be used
as a fixed evaluation set during the open leaderboard phase of the
challenge. The holdout set is purposefully not released during the
duration of the challenge and is meant to be used as a private evaluation
set to counter any challenge-specific gaming."

Table 2 counts: Train 18,336 images / 632,228 polygons; Test 1,866 images /
109,724 polygons; Holdout 1,866 images / 108,784 polygons.

Damage class distribution (pooled): No damage 313,033; minor damage
36,860; major damage 29,904; destroyed 31,560; unclassified 14,011 — "no
damage" has "more than eight times the representation of the other
classes."

Metric: weighted F1 score, chosen because "Accuracy by itself is a flawed
metric, since a classifier that predicted 'no damage' on all of the images
would retain 75% accuracy." Localization uses IoU. No seeds, no repeated
runs, and no variance are reported anywhere in the paper — all numbers
(IoU 0.97/0.66; overall F1 0.2654; per-class F1/precision/recall in Table
3) are single-run point estimates.

## Reproduction

Self-reported, single run, by the dataset's own authors as a baseline for
the xView2 challenge — not an independent reproduction. Evidence: Table 3
(per-class F1 0.6631 / 0.1435 / 0.0094 / 0.4657 for no/minor/major/destroyed
damage) and the localization IoU figures. Code is released
(https://github.com/DIUx-xView/xview2-baseline/) but the paper does not
say whether it has been verified to run.

Reimplementable in an afternoon: the architecture itself is simple
(ResNet50 pretrained on ImageNet + a small randomly-initialized side CNN,
concatenated into dense layers, ordinal cross-entropy loss) and could be
coded up quickly. Reproducing the *reported numbers*, however, requires
the full 632,228-polygon training set and matches the paper's own compute
— localization trained "on an eight GPU cluster for seven days," and the
classifier trained "for 100 epochs on 8 Nvidia GTX-1080 GPUs" — well
beyond an afternoon on ordinary hardware.

## What to steal

The Joint Damage Scale itself — a 4-level ordinal severity scale
deliberately built to be assessable from satellite imagery alone (no
in-person attributes), unified across disaster types instead of
per-disaster-specific — is the reusable artifact. Also worth taking: the
image-shift correction procedure (§5.3.1), where a post-hoc, per-disaster
uniform UTM coordinate shift is computed from the average pixel offset
between drawn polygons and true building edges, to fix pre/post
registration drift without ever touching the polygons or the pre-image —
a cheap, disaster-level registration QC step applicable to any bitemporal
paired-imagery pipeline.

## Same-cell comparison

_no siblings_

## References named

- Creating xBD: A dataset for assessing building damage from satellite
  imagery (Gupta et al., CVPRW 2019)
- Damage detection from aerial images via convolutional neural networks
  (Fujita et al., 2017)
- Benchmark dataset for automatic damaged building detection from
  post-hurricane remotely sensed imagery (Chen et al., 2018)
- Building damage assessment in the city of Mocoa (United States
  Geological Survey, 2017)
- The use of remote sensing for post-earthquake damage assessment: Lessons
  from recent events, and future prospects (Foulser-Piggott et al., 2012)
- Identifying collapsed buildings using post-earthquake satellite imagery
  and convolutional neural networks: A case study of the 2010 Haiti
  earthquake (Ji, Liu, and Buchroithner, 2018)
- Methods for the evaluation of direct and indirect flood losses (Thieken
  et al., 2008)
- Classifications of structural types and damage patterns of buildings
  for earthquake field investigation (Okada and Takai, 1999)
- Residential Building Damage from Hurricane Storm Surge: Proposed
  Methodologies to Describe, Assess and Model Building Damage (Friedland,
  PhD thesis, 2009)
- Hazus hurricane model user guidance (Federal Emergency Management
  Agency, 2018)
- Damage assessment operations manual: A guide to assessing damage and
  impact (Federal Emergency Management Agency, 2016)
- Physical Flood Vulnerability of Residential Properties in Coastal,
  Eastern England (Kelman, PhD thesis, 2002)
- EMS-98 (European Macroseismic Scale) (Grünthal, Musson, Schwarz, and
  Stucchi, 1998)
- DeepGlobe 2018: A challenge to parse the earth through satellite images
  (Demir et al., 2018)
- Analysis of daily, monthly, and annual burned area using the
  fourth-generation global fire emissions database (GFED4) (Giglio,
  Randerson, and van der Werf, 2013)
- Filtering to remove cloud cover in satellite imagery (Mitchell, Delp,
  and Chen, 1977)
- Cloud detection for high-resolution satellite imagery using machine
  learning and multi-feature fusion (Bai et al., 2016)
- Remote sensing imaging simulation and cloud removal (Zhu, Wu, Wu, and
  Zhao, 2017)
- ImageNet: A Large-Scale Hierarchical Image Database (Deng, Dong, Socher,
  Li, Li, and Fei-Fei — year not given in this paper's reference list)
- GDAL/OGR Geospatial Data Abstraction Software Library (GDAL/OGR
  contributors, 2019)
- U-Net: Convolutional Networks for Biomedical Image Segmentation
  (Ronneberger, Fischer, and Brox, 2015)
- Smear effect on high-resolution remote sensing satellite image quality
  (Wahballah, Bazan, and Ibrahim, 2018)

## What was read

`~/.cache/research-bearings/fetch/arxiv-1911.09296/full.txt`,
31,314 characters, full pass (all 690 lines / 10 pages, including the
reference list). Not read: the figures and tables themselves as images —
only the pdftotext-extracted text and captions (Figures 1–10, Tables 1–4)
were available, so any visual detail not restated in the caption text
(e.g. exact appearance of imagery, chart values in Figures 6–9 beyond the
numbers given in prose) was not read.
