# 09: `/audit` and `leakage-auditor`

Type: task
Status: done
Blocked by: 03

## What to build

`leakage-auditor` (Read, Edit): fills one card's leakage section with the
Kapoor and Narayanan taxonomy: no held-out test set, preprocessing or feature
selection fitted on the union, duplicates across splits, temporal leakage,
spatial leakage (tile or scene overlap), group leakage, illegitimate features,
test set not representative of deployment. Each flag carries a quoted passage
from the fetched text or the dataset row, or a `could not determine, checked
<sections>` line. Flags and evidence only; no score, no verdict.

`/audit <slug>` (Read, Glob, Bash, Agent): exactly one card; runs `fetch` to
ensure the text is present; finds the dataset row if the ledger exists;
dispatches the auditor with card path, full-text path and row.

## Acceptance

- [x] Plugin validation green.
- [x] On a real card, the leakage section lists every taxonomy type with either a quoted passage or a `could not determine` line naming what was checked; nothing else on the card changes; `check_cards` green.
- [x] With no datasets ledger, the run still completes and the section says the row was absent.
- [x] `/audit` with no argument or two arguments refuses and says so.

## Resolution

2026-09-16. `agents/leakage-auditor.md`, `skills/audit/SKILL.md`.

Live on `gupta-2019-xbd`. Eight types written, one PRESENT, four not found,
three could not determine. Only the card's `## Leakage` section changed;
`check_cards` green. The datasets ledger did not exist when it ran, and the
closing line says so — which is the no-ledger path exercised for free.

**It found a real one, with the quote.** Preprocessing on the union: the
image-shift registration correction is fit from a sample of a disaster event's
own imagery — "we sampled many random image tiles from the post-disaster
CatID and calculated the average pixelwise shift" — and then "applied to all
post-disaster images within that disaster event uniformly", without regard to
which split each image later falls into.

The three `could not determine` lines are the honest ones and all have the
same cause: the paper never says whether the 19 disaster events are held out
whole or pooled across the splits, and Table 2 gives only pooled counts. That
is exactly the case the rule was written for — silence in a paper is not
absence of leakage.
