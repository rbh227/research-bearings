# Landscape eval

Two live runs of `/surveys` then `/landscape`, on the wildfire gold topic and on
post-disaster building damage assessment, scored for recall against
`evals/gold/wildfire-cv.md` and reported by gold heading. Run 2026-09-15.
**Not tuned**: the numbers below are what the first clean run produced, and
the gold file was not edited.

## How the runs were made

The plugin's agents are dispatched by name (`research-bearings:searcher`) from
inside an installed plugin. This eval ran from the repo itself, so each agent
was a general-purpose subagent handed the agent's contract file verbatim plus
the dispatch payload the skill would send, and told which tools it had. The
script calls, the sections, the merger's matrix and the recall check are the
real ones; the agent registration is the emulated part. The write-scope guard
did not apply to these subagents, which is why the outputs could land under
`evals/landscape/runs/` instead of `research/`.

Fixtures: `runs/<topic>/research/QUESTION.md`, written by hand so the skills
have `## Question` and `## Vocabulary` to read. Paper records went to the
repo's `research/.papers/` (gitignored).

## The queries shown at the gate

Seven per topic, derived from the fixture's question and vocabulary as
`skills/landscape/SKILL.md` step 1 says. The survey query is the problem
itself; the searcher's survey mode restricts the seeds to reviews.

### wildfire

| # | question | query |
|---|---|---|
| s | surveys | `wildfire detection mapping spread prediction remote sensing machine learning` |
| 1 | formulations | `wildfire remote sensing active fire detection burned area mapping burn severity fire spread prediction` |
| 2 | data regimes | `wildfire satellite dataset labels benchmark MODIS VIIRS Landsat Sentinel-2 UAV camera imagery` |
| 3 | methods | `wildfire deep learning convolutional neural network transformer detection segmentation forecasting` |
| 4 | reproduction | `wildfire detection burned area mapping benchmark comparison baseline evaluation validation` |
| 5 | abandoned | `forest fire detection remote sensing threshold contextual algorithm spectral index` |
| 6 | adjacent | `smoke plume detection satellite imagery aerosol natural hazard rapid mapping` |
| 7 | time slice | `wildfire geospatial foundation model multimodal spread forecasting zero-shot` |

### damage

| # | question | query |
|---|---|---|
| s | surveys | `post-disaster building damage assessment satellite aerial imagery deep learning` |
| 1 | formulations | `building damage assessment satellite imagery localization classification semantic change detection per-building damage grade` |
| 2 | data regimes | `building damage dataset xBD xView2 labels weak supervision domain shift cross-event generalization` |
| 3 | methods | `building damage assessment deep learning siamese network attention transformer change detection` |
| 4 | reproduction | `xBD xView2 benchmark baseline comparison building damage evaluation` |
| 5 | abandoned | `earthquake damage detection remote sensing texture spectral change object-based image analysis` |
| 6 | adjacent | `flood mapping post-event satellite imagery deep learning segmentation rapid mapping` |
| 7 | time slice | `building damage assessment foundation model vision-language zero-shot post-disaster mapping` |

## What actually ran, and how

- The survey searchers ran twice: the first pass hit an uncapped OpenAlex
  reference hop (a 543-reference review spent the whole budget as seed 2);
  that was fixed in the script and both were rerun. Four landscape searchers
  (wildfire 1–4) ran as agents; the other ten walks, both survey-differ steps
  and both merger steps were done in the main thread after the agent fan-out
  exhausted the account's usage limit. The ten walks used
  `neighborhood --write`, which the script gained for exactly this reason: the
  searcher's paste step is mechanical, so the script does it. The differ and
  merger steps followed their contracts by hand and by a helper script that
  copies lines and probes cells; the files say so in a comment at the top.
- The wildfire differ agent appended its vocabulary block to the fixture's
  `QUESTION.md` before it died; the main thread's block sits under it. Both
  are left as they landed.
- Fourteen of the sixteen walks stopped on the 400-paper budget between seed 9
  and seed 16 of 30. One (damage data regimes) completed all its seeds because
  S2 returned five rows and OpenAlex ten, so it had ten seeds.
- Wildfire sections 1 and 3 show `Degraded: s2`: at that point one failed S2
  hop marked S2 dead for the rest of the walk. The rule became three
  consecutive failures before the remaining ten walks ran; none of those
  report a degraded index.
- Semantic Scholar's keyword search returns zero or single-digit rows for
  queries of eight or more terms, so most seeds came from OpenAlex and most
  hops ran on OpenAlex, which carries no `influentialCitationCount`. Sixty-five
  hop calls returned zero rows on S2.

## Results

`recall.py` output is in `runs/<topic>/recall.txt`, misses listed. Threshold as
stated in the script; nothing tuned.

### wildfire (whole field, six gold headings)

| gold heading | found / listed |
|---|---|
| wildfire detection, mapping and burned area | 21 / 26 |
| fire-spread prediction and modelling | 18 / 26 |
| fire regimes, drivers and climate | 7 / 11 |
| smoke, emissions and health | 7 / 8 |
| structure loss and the wildland-urban interface | 2 / 13 |
| damage assessment from aerial and satellite imagery | 1 / 14 |
| **all six** | **56 / 98 = 0.57** |

Misses by group. Detection and mapping: Govil (camera-network detection),
Key & Benson (CBI), Roy (BRDF burned-area prototype), Shamsoshoara (FLAME),
Yebra (fuel moisture review). Spread: the coupled-atmosphere line (Mandel,
Coen, Bakhshaii), FireMIP, and four learned-spread papers (Burge, TeleViT,
the two reinforcement-learning ones). Drivers: Westerling 2006, Bowman 2020,
Keeley & Syphard, Hessburg. Smoke: Aguilera. Structure loss and damage
assessment were not asked for by any of the seven queries, which is the
finding: the seven questions cover the field's methods and data and leave its
outcomes to a separate run.

Matrix: 5 formulations × 4 regimes, 15 filled / 5 empty; the empty cells are
burned area × UAV, burn severity × coarse satellite, spread × medium-resolution,
and smoke × both satellite classes, each with the probe query and its count.
26 contradictions listed, of which all but two are the same paper carrying an
OpenAlex id in one section and an S2 id in another — an index label, not a
disagreement. The merger's contract was tightened afterwards to say so; the
matrix is left as produced.

### damage (acceptance topic, two gold headings)

| gold heading | found / listed |
|---|---|
| damage assessment from aerial and satellite imagery | 10 / 14 |
| structure loss and the wildland-urban interface | 1 / 13 |
| **both** | **11 / 27 = 0.41** |

Misses: DamageMap (Galanis), Voigt's emergency-mapping trends, and the two
Rahnemoonfar UAV datasets (FloodNet, RescueNet-UAV). Structure loss is a
wildfire-outcomes literature the damage queries did not reach. Matrix: 4 × 4,
15 filled / 1 empty (segmentation × weak supervision: 13 rows, none naming
both). 10 contradictions, same pattern.

## What the run says about the design

Recorded here for the reader; none of it was acted on before this was written.

1. **Field centrality promotes ubiquitous methods papers.** ResNet, U-Net,
   LSTM and Faster R-CNN reach centrality 2–4 in every home-field section,
   because many neighborhood papers cite them. The rank is doing what it was
   defined to do; the definition counts citations to the field's tools as
   field centrality. **Kept by decision, 2026-09-16:** the user wants the
   high-citation papers in the ranking. Not a defect; do not dampen it.
2. **A seed's centrality is its forward-hop sample size.** Seeds with 25 or
   more citers all tie at 25 (the per-direction cap) and sort by influential
   count from there. The `sampled` count in the block says how often this
   happened.
3. **Surveys-only mode returns the references of reviews**, which are
   generic ML surveys, ranked above the wildfire reviews that seeded the walk.
   Four of twenty wildfire surveys and one of twenty damage surveys were on
   topic. Outputting the seeds only, or restricting hops to citers, would
   change this; not done.
4. **Long queries starve S2.** Eight-plus terms returned 0 to 9 S2 rows on
   most questions. OpenAlex carried the runs.
5. **The budget binds at seed 9–16 of 30.** 400 papers at 50 rows per seed
   is nine seeds if nothing overlaps. Every block records it.
6. **Fourteen agents at once cost the account its month.** The script now
   writes the section itself so a searcher is one command and a check.
