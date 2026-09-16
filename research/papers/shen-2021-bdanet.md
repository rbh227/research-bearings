# BDANet: Multiscale Convolutional Neural Network With Cross-Directional Attention for Building Damage Assessment From Satellite Images

## Identity

- Slug: shen-2021-bdanet
- Authors: Yu Shen, Sijie Zhu, Taojiannan Yang, Chen Chen, Delu Pan, Jianyu
  Chen, Liang Xiao, Qian Du
- Year: 2021
- Venue: IEEE Transactions on Geoscience and Remote Sensing (TGRS)
- Ids: arXiv `2105.07364` · DOI `10.1109/TGRS.2021.3080580` · S2
  `013ec50cdd6524f78bb0f575f5b51a498c669fcb`
- Code: https://github.com/ShaneShen/BDANet-BuildingDamage-Assessment — runs:
  not tried
- Read: 2026-09-16 · pass full · text: fetched
- Fetched from: https://arxiv.org/pdf/2105.07364

## Matrix position

- Formulation: per-building damage classification
- Data regime: paired pre/post satellite (xBD, xView2)
- Cell: `per-building damage classification × paired pre/post satellite (xBD, xView2)` — research/landscape/matrix.md

## Delta

Compared to RescueNet (Gupta and Shah [14], 2021) and Weber and Kané's
multi-temporal fusion method ([12], 2020) — both of which fuse pre- and
post-disaster features by a single fixed operation (RescueNet takes the
*difference* of pre/post features; Weber's method *concatenates* them) and
which the paper says represent the standard practice of "simply
concatenat[ing] pre- and post-disaster images... without considering their
correlations" — this paper adds a two-stage framework (Stage 1: U-Net
building segmentation from pre-disaster images only; Stage 2: a two-branch
multi-scale U-Net with a cross-directional attention (CDA) module that
aggregates pre/post features channel-wise and spatial-wise in both
directions) plus a data-augmentation strategy that applies CutMix only to
the two hardest classes (minor and major damage), and gets a higher overall
score on xBD: F1s 0.806 vs. 0.741 (RescueNet) and 0.770 (Weber et al.), and
F1d 0.782 vs. 0.697 (RescueNet) and 0.740 (Weber et al.).

## Bit flipped

The assumption that pre/post-disaster feature fusion for damage assessment
can be handled by a single fixed operation — concatenation (Weber et al.
[12]) or subtraction (RescueNet [14]) — applied once. The paper's stated
premise is that "[m]ost existing works simply concatenate pre- and
post-disaster images as input of a deep neural network without considering
their correlations," and its CDA module instead computes bidirectional
channel- and spatial-attention terms between the two branches at multiple
decoder depths. A second, narrower assumption also gets flipped by the
ablation: that CutMix, as a generic augmentation, helps uniformly across
classes — Table XI shows CutMix applied to *all* classes gives almost no
gain (F1s 0.789 → 0.790) and only pays off when restricted to the difficult
classes (minor + major damage: 0.789 → 0.802).

## Not compared against

- Gupta et al.'s own xBD baseline classifier (the paper this dataset comes
  from, [18]) — the paper cites it only for the dataset and metric
  definition, never places its reported numbers in the results tables
  (Table V) alongside RescueNet, Weber et al., WNet, U-Net++, FCN, SegNet,
  and DeepLabv3. This matters because that baseline's headline classifier
  number (weighted F1 0.2654, per the sibling card) is far below every
  number in this paper's Table V, and the paper never explains why it left
  the dataset's own reference baseline out of the comparison.
- Ordinal-regression-based damage classifiers ([5] Ci et al., [6] Nex et
  al.), which the related-work section (§II-A) explicitly names as prior
  work that differentiates damage *levels* (not just binary damaged/
  undamaged) — the same problem this paper addresses — but neither is run
  as a baseline in Table V.
- A cross-disaster (held-out-event) generalization test — Table III reports
  only a Train/Test split by image count (18336/1866), with no experiment
  training on a subset of the 19 disaster events and testing on an unseen
  one, despite the paper's own motivation (§I) being "fast and effective
  responses... when a natural disaster strikes," which implies performance
  on disasters not seen during training.

## Kill experiment

The central claims are (a) that the CDA/MFF modules extract fusion
information that naive concatenation/difference misses, and (b) that
class-targeted CutMix beats generic CutMix. Both are directly tested and
both experiments were run: Table VII/IX/X isolate CDA and MFF against a
"vanilla" two-stage network with neither (only +0.5-0.6% F1s each, and CDA
beats the SE-module ablation it was built from by the same margin), and
Table XI isolates CutMix-on-all-classes (+0.1%) against CutMix-on-
difficult-classes-only (+1.3%), confirming the paper's specific claim about
where CutMix should be targeted. The claim that is *not* isolated with an
equivalent experiment is the higher-level architectural choice of a
two-stage pipeline itself: the paper's only comparison against single-stage,
one-network approaches is against WNet and U-Net++ (Table V), which differ
from BDANet in far more than "one stage vs. two" (different backbones,
different loss designs), so that comparison is confounded and does not
isolate whether the two-stage design itself is what is doing the work.

## Data and split

Dataset: xBD [18], 19 disasters (hurricanes, floods, wildfire, earthquakes),
"more than 800,000 building annotations," image pairs of 1024×1024 pixels,
three-band RGB, 0.8 m/pixel, sourced from the DigitalGlobe Open Data
Program.

Split: the paper gives no split-protocol prose beyond a table caption.
Table III ("The xBD dataset splits and annotation numbers"), quoted in full:
Train — 18336 images, 632228 polygons; Test — 1866 images, 109724 polygons.
No holdout split, and no third partition, is mentioned anywhere in the
paper.

Damage-level distribution (Table IV): No damage 313003 (76.04%), Minor
36860 (8.98%), Major 29904 (7.29%), Destroyed 31560 (7.69%).

Metric: F1b for building segmentation (standard pixel-wise F1: 2TP /
(2TP+FP+FN)); F1d for damage classification, defined explicitly as the
*harmonic mean* of per-class F1 scores, "F1d = n / Σ(1/F1_Ci)"; and an
overall score "F1s = 0.3 × F1b + 0.7 × F1d" (Eq. 10), attributed to the
original xBD/xView2 challenge scoring [18]. No seeds, no repeated runs, and
no variance are reported anywhere — every number in Tables V–XIII is a
single-run point estimate. Hardware: Intel i9-9920X CPU, two NVIDIA
TITAN-V GPUs; Stage 1 trained 120 epochs at lr 0.00015, Stage 2 trained 25
epochs at lr 0.0002.

## Reproduction

Self-reported, single run, by the paper's own authors — not an independent
reproduction, and no other group's number for BDANet appears anywhere in
the paper. Evidence: Table V (F1s 0.806, F1b 0.864, F1d 0.782) and the
per-class confusion matrix in Table VI. Code is released
(https://github.com/ShaneShen/BDANet-BuildingDamage-Assessment) but the
paper does not state whether it has been verified to run.

Reimplementable in an afternoon: the architecture (two ResNet-50-backboned
U-Nets sharing weights across stages, plus the MFF module described as
three resolution streams and the CDA module described as two matrix
operations, Eqs. 4–7) is fully specified and not exotic — a reasonable
afternoon build for someone who already has a U-Net baseline. Reproducing
the *reported numbers*, however, requires the full 632,228-polygon training
set and the paper does not report training wall-clock time on its two-GPU
setup, so matching the exact point estimates is not an afternoon task even
though the code itself is.

## What to steal

The cross-directional attention (CDA) module: a cheap (<1M extra
parameters, 107.6 vs. 92.9 GFLOPs) bidirectional channel-then-spatial
attention block (Eqs. 4–7) that fuses two co-registered feature branches
without a non-local-style full attention map, applicable to any paired
pre/post (or multi-branch) imagery pipeline, not just damage assessment.
Also worth taking: the finding in Table XI that CutMix should be applied
selectively to the classes a baseline confusion matrix (Table I) already
shows are hardest, rather than uniformly across all classes — a cheap,
model-agnostic augmentation-targeting recipe.

## Same-cell comparison

Sibling `gupta-2019-xbd.md`: **incompatible.** Two conflicts. (1) Headline
numbers on the same dataset are not comparable as reported: Gupta's own
xBD-baseline classifier gets overall weighted F1 0.2654 (per-class F1
0.6631/0.1435/0.0094/0.4657 for no/minor/major/destroyed, with "major
damage" collapsing to F1 0.0094), while every method in this paper's Table
V — including RescueNet and Weber et al., which this paper does *not*
identify as reproductions of Gupta's baseline — scores F1d in the 0.70-0.78
range. This paper never places Gupta's own reported baseline number in its
comparison table at all, so the two cards' headline numbers sit in
different tables with no stated bridge between them, and it is not
possible from either paper alone to tell whether the gap is model
improvement, a different F1 formula, or something else. (2) The split
tables partially disagree: this paper's Table III reports only a
Train/Test partition (18336/632228 and 1866/109724 — the counts match
Gupta's Train and Test exactly) and never mentions the Holdout partition
(1866 images/108784 polygons) that Gupta's paper reports as a third,
purposefully-withheld split; this paper does not say which of Gupta's Test
or Holdout sets (or some other split) its "Test" numbers correspond to.

## Prediction score

- Method: 5 — confirmed in every specific detail the prediction committed
  to (MFF inside the encoder, a bidirectional channel-and-spatial CDA
  module between the pre/post branches rather than self-attention within
  one branch, Stage-1-to-Stage-2 weight reuse, and CutMix restricted to the
  minor/major-damage pair per Table XI), with nothing in the reading that
  contradicts it.
- Main result: 4 — the numeric range (80-84) and the margin over the
  strongest cited prior baseline (2-5 points) both landed, matching F1s
  0.806 against Weber et al.'s 0.770, but the prediction's framing of the
  comparison set — "prior CNN baselines such as RescueNet and a ResNet-50/
  attention baseline" — names a baseline shape ("ResNet-50/attention")
  that does not match any of the methods actually in Table V (RescueNet,
  Weber et al., WNet, U-Net++, FCN, SegNet, DeepLabv3).
- Weakest point: 3 — the first half (standard xBD train/test split, no
  held-out-event generalization test) is exactly what the reading found;
  the second half is wrong: the prediction guessed the CDA/MFF/CutMix gains
  would lack "a clean ablation isolating each component's contribution,"
  but Tables VII, IX, X, and XI do exactly that, isolating each component
  against a vanilla two-stage baseline.

## What was non-obvious

A careful first reading, having flagged the plausible risk that BDANet's
CDA, MFF, and CutMix gains might be entangled without a clean isolating
ablation, would still be wrong: Tables VII, IX, X, and XI isolate each
component separately against a vanilla two-stage baseline, so the
entanglement it predicted is not what the paper's own ablations show.

## Reviews

_not run_

## Leakage

_not run_

## References

- Building damage detection in satellite imagery using convolutional neural
  networks (Xu, Lu, Li, Khaitan, and Zaytseva, NeurIPS-HADR Workshop 2019)
- Building disaster damage assessment in satellite imagery with
  multi-temporal fusion (Weber and Kané, ICLR-AI for Earth Sciences
  Workshop 2020)
- An attention-based system for damage assessment using satellite imagery
  (Hao, Baireddy, Bartusiak, Konz, LaTourette, Gribbons, Chan, Comer, and
  Delp, arXiv 2020)
- RescueNet: Joint building segmentation and damage assessment from
  satellite imagery (Gupta and Shah, ICPR 2021)
- xBD: A dataset for assessing building damage from satellite imagery
  (Gupta, Hosfelt, Sajeev, Patel, Goodman, Doshi, Heim, Choset, and Gaston,
  CVPRW 2019)
- CutMix: Regularization strategy to train strong classifiers with
  localizable features (Yun, Han, Oh, Chun, Choe, and Yoo, ICCV 2019)
- U-Net: Convolutional networks for biomedical image segmentation
  (Ronneberger, Fischer, and Brox, MICCAI 2015)
- MSNet: A multilevel instance segmentation network for natural disaster
  damage assessment in aerial videos (Zhu, Liang, and Hauptmann, WACV 2021)
- From W-Net to CDGAN: Bitemporal change detection via deep learning
  techniques (Hou, Liu, Wang, and Wang, TGRS 2020)
- Recalibrating Fully Convolutional Networks With Spatial and Channel
  "Squeeze and Excitation" Blocks (Roy, Navab, and Wachinger, IEEE TMI 2018)
- End-to-end change detection for high resolution satellite images using
  improved UNet++ (Peng, Zhang, and Guan, Remote Sensing 2019)
- Fully convolutional networks for semantic segmentation (Long, Shelhamer,
  and Darrell, CVPR 2015)
- SegNet: A deep convolutional encoder-decoder architecture for image
  segmentation (Badrinarayanan, Kendall, and Cipolla, TPAMI 2017)
- Encoder-decoder with atrous separable convolution for semantic image
  segmentation (Chen, Zhu, Schroff, and Adam, ECCV 2018)
- A spatial-temporal attention-based method and a new dataset for remote
  sensing image change detection (Chen and Shi, Remote Sensing 2020)
- Non-local neural networks (Wang, Girshick, Gupta, and He, CVPR 2018)
- Structural Building Damage Detection with Deep Learning: Assessment of a
  State-of-the-Art CNN in Operational Conditions (Nex, Duarte, Tonolo, and
  Kerle, Remote Sensing 2019)
- Assessment of the degree of building damage caused by disaster using
  convolutional neural networks in combination with ordinal regression
  (Ci, Liu, and Wang, Remote Sensing 2019)
- Assessing building damage by learning the deep feature correspondence of
  before and after aerial images (Presa-Reyes and Chen, MIPR 2020)
- mixup: Beyond empirical risk minimization (Zhang, Cisse, Dauphin, and
  Lopez-Paz, ICLR 2018)
- Deep residual learning for image recognition (He, Zhang, Ren, and Sun,
  CVPR 2016)

## Status

Read 2026-09-16 by /read. Reviews: not run. Leakage: not run.
