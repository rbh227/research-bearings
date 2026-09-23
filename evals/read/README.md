# Read run: damage, 2026-09-16

The dry run that verified chunk 7's reading protocol. Kept here, beside
`evals/landscape/runs/`, because it is run output and not somebody's research:
a plugin whose `research/` folder ships full of another project's cards is a
plugin that confuses its first user.

The landscape these cards were read against is
`evals/landscape/runs/damage/research/landscape/` — the same fixture, not a
second copy.

## What is here

| Path | Written by |
|---|---|
| `runs/damage/papers/*.md` | the `scorer`, at the end of a `/read` run |
| `runs/damage/papers/notes/*.prediction.md` | the `predictor`, before anything else read the paper |
| `runs/damage/papers/notes/*.reading.md` | the `reader`, which never saw the prediction |
| `runs/damage/datasets.md` | `dataset-scout` |
| `runs/damage/groups.md` | `author-tracker` |
| `runs/damage/BITS.md` | `/bits`, in the main thread; revised after the critique below |
| `runs/damage/critiques/BITS-2026-09-16.md` | `critic`, two passes |

## What it showed

**The three-agent protocol earns its cost.** On xBD the predictor, holding a
file that ends at the introduction, guessed an overall damage-classification
F1 of 0.60 to 0.75 held back by class imbalance. The paper reports 0.2654,
with the major-damage class collapsing to 0.0094, and reports localization as
IoU rather than F1 at all. Scores 4, 2, 5, and the non-obvious line came from
the 2.

**Read-time contradiction detection works.** Reading BDANet with the xBD card
as its sibling, the reader named two conflicts: the comparison tables do not
bridge (0.70-0.78 against 0.2654), and BDANet's Train and Test counts match
the release exactly while the holdout partition goes unmentioned.

**"The standard split" is three different things.** The datasets ledger quotes
all three rather than collapsing them: the release's 80/10/10
train/test/holdout, BDANet's train/test, and RescueNet's Tier1/Tier3 train
with roughly a tenth carved out for validation.

**The critic found four real problems in a file written an hour earlier**, in
the main thread, by the same session. Worst: `BITS.md` grouped BDANet under a
thesis of "one network trained end to end" when its own card calls it
two-stage. All four are fixed in the revised file; the critique is kept
unedited beside it.

## Reading it back

```bash
python3 scripts/check_cards.py evals/read/runs/damage/papers/
```

Three cards, all passing. One is a `--skim` (pass 1) that was written with no
matrix present and placed afterwards by `/read --place`, which is why its
same-cell comparison is still `_no matrix_`.
