# 09: `/audit` and `leakage-auditor`

Type: task
Status: ready-for-agent
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

- [ ] Plugin validation green.
- [ ] On a real card, the leakage section lists every taxonomy type with either a quoted passage or a `could not determine` line naming what was checked; nothing else on the card changes; `check_cards` green.
- [ ] With no datasets ledger, the run still completes and the section says the row was absent.
- [ ] `/audit` with no argument or two arguments refuses and says so.
