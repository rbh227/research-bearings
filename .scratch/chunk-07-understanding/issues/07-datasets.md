# 07: `/datasets` and `dataset-scout`

Type: task
Status: ready-for-agent
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

- [ ] Offline cases: a Hugging Face hit and a GitHub hit; both empty. Shape and state names only.
- [ ] Plugin validation green; heading parity green for the datasets template.
- [ ] On the existing cards, the ledger has one row per dataset named, with the license and link from a host or a `could not determine` line naming the hosts checked, and "who uses it" listing card slugs.
- [ ] The guard denies `dataset-scout` a `gh` command and allows the retrieval script (case added in ticket 12; verified here by hand).
