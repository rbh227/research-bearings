# 07: `/datasets` and `dataset-scout`

Type: task
Status: done
Blocked by: 03

## What to build

The `datasets` verb: given a dataset name, query the Hugging Face hub datasets
search and the GitHub REST search, and return per host: name, link, license,
size or file count, split files found, stars or downloads, last update. A host
returning nothing is named as such. GitHub through the REST API, never the
`gh` command; optional `GITHUB_TOKEN`; unauthenticated search paced to ten per
minute. Existing `HF_TOKEN` used when present. Cached 30 days.

`dataset-scout` (Read, Bash, Write; Bash for the retrieval scripts only, no
web tools): reads the verb outputs, the cards, and the fetched full texts, and
writes the datasets ledger from a new template with the build plan's
dataset-row fields: name, size, modality, resolution and scale, geography,
annotation type, split protocol, license, who uses it (card slugs), known
flaws, leakage assessment of the standard split, link. Facts come from the
host record or a quoted passage; otherwise `could not determine, checked
<hosts>`.

`/datasets` (Read, Glob, Bash, Write, Agent): collects names from every card's
dataset field and from the experiments section of each carded paper's full
text; runs the verb per name; dispatches the scout once.

## Acceptance

- [x] Offline cases: a Hugging Face hit and a GitHub hit; both empty. Shape and state names only.
- [x] Plugin validation green; heading parity green for the datasets template.
- [x] On the existing cards, the ledger has one row per dataset named, with the license and link from a host or a `could not determine` line naming the hosts checked, and "who uses it" listing card slugs.
- [x] The guard denies `dataset-scout` a `gh` command and allows the retrieval script (case added in ticket 12; verified here by hand).

## Resolution

2026-09-16. The `datasets` verb, `agents/dataset-scout.md`,
`skills/datasets/SKILL.md`, `templates/research/datasets.md`.

Live on the three cards. One dataset named (xBD), rows from both hosts, and
the licence and authoritative host recorded as `could not determine` because
both hosts returned only mirrors and downstream code, which the scout declined
to present as the dataset's own record.

**The run justified the "quote the split" rule outright.** The three cards
report three different protocols for the same nominal standard xBD split: the
release's own 80/10/10 train/test/holdout; BDANet's train/test with the
holdout unmentioned and counts matching the release exactly; and RescueNet's
Tier1/Tier3 train with about 10 per cent carved out for validation, built
because the official test annotations were not public at the time. All three
are quoted separately rather than collapsed into "the standard split".

`--context` was added after a bare "xBD" returned an Xbox diagnostic tool
above the xView2 solution on GitHub; it is appended to the GitHub query only.
GitHub is reached over REST and the guard's selftest carries the case denying
`dataset-scout` the `gh` command.
