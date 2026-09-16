# 12: Guard cases, status probes, setup step

Type: task
Status: done
Blocked by: 03, 06, 07, 11

## What to build

Guard selftest cases for the new agents: `dataset-scout` allowed the retrieval
script and denied `gh`; `predictor` denied Bash; `critic` denied a Write
outside the research folder; any new agent denied `WebSearch` and `WebFetch`.
The guard's own code should need no change; if it does, say why in the ticket.

`status` and `health` gain probes for GitHub (REST rate-limit endpoint, token
state) and OpenReview (public API root, login state), reported in the three
chunk 4 states. Neither joins the "keys that would help most" list. The
connections template and `/setup`'s connections step carry the two new lines.
The APIs reference gains sections for GitHub and OpenReview and marks
Unpaywall and Hugging Face as now used by `fetch` and `datasets`.

## Acceptance

- [x] Guard selftest green with the new cases.
- [x] `status` prints nine sources with a state each; `health` shows the two new keys' presence.
- [x] A `/setup` dry run writes the connections file with the two new lines under the sources heading; heading parity green.
- [x] The APIs reference documents both new sources in the existing per-source shape (used for, env, where, rate, without it, test).

## Resolution

2026-09-16. `hooks/guard.py` cases, the GitHub and OpenReview probes in
`snowball.py`, `/setup`'s connections step, and `docs/APIS.md`.

**The guard needed no code change**, which the ticket asked to be shown rather
than assumed. The prefix rule already covers every agent this plugin ships, so
the new cases prove it: `dataset-scout` may run `papers.py` and may not run
`gh`; `critic` may write into `research/critiques/` and not into `/tmp`; all
eight agents are denied `WebSearch` and `WebFetch`.

One case was rewritten because its assertion was wrong, not the guard. "The
predictor's Bash is denied" is false — the guard lets any of our agents run
the retrieval scripts, and what stops the predictor is its frontmatter. So the
selftest now reads the agent files and checks that seven of the eight grant no
Bash and that none grants a web tool. That is the fence that actually exists.

`status` probes nine sources. The two new ones carry `suggest: False` and are
excluded from the top-three list, with a case asserting it: a suggestion list
that grows every chunk stops being read.
