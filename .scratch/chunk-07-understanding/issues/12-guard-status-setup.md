# 12: Guard cases, status probes, setup step

Type: task
Status: ready-for-agent
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

- [ ] Guard selftest green with the new cases.
- [ ] `status` prints nine sources with a state each; `health` shows the two new keys' presence.
- [ ] A `/setup` dry run writes the connections file with the two new lines under the sources heading; heading parity green.
- [ ] The APIs reference documents both new sources in the existing per-source shape (used for, env, where, rate, without it, test).
