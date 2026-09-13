# A saved crawl, for the agent cases

Four files, one per script call, in the order a scout would make them. Real
Semantic Scholar responses (captured 2026-09-13), shaped exactly as
`scripts/retrieval/snowball.py` prints them, with a budget of 25.

| File | What it is | What it lets a grader see |
|---|---|---|
| `00-search.json` | 5 seeds for "building damage assessment satellite imagery" | seeds are not cards; search does not charge the budget |
| `01-references-ARXIV-2405.04800.json` | backward hop: 22 resolved, 3 unresolvable | grey literature stays title-only; half the rows have no abstract to mark `Missing:` |
| `02-citations-ARXIV-2405.04800.json` | forward hop, clamped to the 3 the budget left, `truncated: true` | a truncated hop forbids `saturation`; `describes: origin_paper` flips the quote line |
| `03-references-ARXIV-2011.10328.json` | `stopped: "budget"` — the refusal | the stop reason is `budget` and the section must say INCOMPLETE |

The agent cases point `paper-scout` at this directory instead of the script, so
they need no network, no key and no `Bash` grant — which this machine cannot give
inside the harness (chunk 1 spec §9). They test what the agent *writes*. The
crawl itself is covered by the script's offline selftest; finding things by the
gold set (`evals/gold/`).
