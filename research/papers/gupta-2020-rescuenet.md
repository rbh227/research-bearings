# RescueNet: Joint Building Segmentation and Damage Assessment from Satellite Imagery

## Identity

- Slug: gupta-2020-rescuenet
- Authors: Rohit Gupta, Mubarak Shah (Center for Research in Computer Vision, University of Central Florida)
- Year: 2020
- Venue: International Conference on Pattern Recognition — from the fetch record, not from the introduction
- Ids: arXiv `2004.07312` · DOI `10.1109/ICPR48806.2021.9412295` · S2 `0c433390c7d5c10441ccc45af60f597446f18f64`
- Code: not read — no repository link appears in the introduction
- Read: 2026-09-16 · pass 1 · text: fetched
- Fetched from: https://arxiv.org/pdf/2004.07312

## Matrix position

- Formulation: per-building damage classification
- Data regime: paired pre/post satellite (xBD, xView2)
- Cell: `per-building damage classification × paired pre/post satellite (xBD, xView2)` — research/landscape/matrix.md
- Placed by `/read --place` on 2026-09-16, after the card was written. The
  same-cell comparison below stays `_no matrix_`: placing is a lookup, and
  comparing needs the paper open. Re-read to fill it.

## Delta

Compared to the two-stage pipelines used by prior damage-detection methods
(cited as [10] and [1] in the introduction: building detection on pre-disaster
imagery, then a separate classification stage comparing pre and post imagery,
not end-to-end trainable), this changes to a single end-to-end trainable
pixel-level segmentation model that jointly segments buildings and classifies
per-building damage using multi-scale temporal features and a
localization-aware loss, and gets improved performance on xBD, claimed as
largest on damage classification.

## Bit flipped

That building localization and damage classification are separate problems to
be solved by separate stages. The introduction argues the two-stage design is
what limits damage classification, and makes the joint model the contribution.

## Not compared against

_not read_ — the introduction names two prior methods as the comparison but
the baseline set is in Section V.

## Kill experiment

- Experiment: whether the joint model beats the two-stage pipeline on damage
  classification specifically, rather than on localization.
- Run: _not read_ — claimed in the introduction, shown in Section V.

## Data and split

- Dataset: xBD
- Split: _not read_ — the introduction names the dataset, not the protocol.
- Seeds and variance: _not read_
- Metric: _not read_

## Reproduction

- Status: unknown
- Evidence: _not read_
- Reimplementable in an afternoon: _not read_

## What to steal

The localization-aware loss: binary cross-entropy for the building mask plus a
foreground-only categorical cross-entropy for damage, so the damage head is
never trained on background pixels. Stated in the introduction as the
mechanism behind the joint model's gain.

## Same-cell comparison

_no matrix_

## Prediction score

_not run_

## What was non-obvious

_not run_

## Reviews

_not run_

## Leakage

_not run_

## References

- Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery · 2019 · S2 `ec58b5946c57f7d4d4a3cff0566941bb93291c95` · verified

## Status

Read 2026-09-16 by /read --skim. Five card fields are `not read` because a
skim reads the introduction only. Reviews: not run. Leakage: not run.
Placed 2026-09-16 by /read --place.
