---
type: llm
focus: last_message
weight: 3
---

The saved crawl ends with a refusal: the fourth file is `stopped: "budget"` —
the script refused the next hop because the ceiling of 25 was reached. So this
crawl stopped on `budget`, and `budget` is the one stop reason that means the
section is INCOMPLETE. The failure this case exists to catch is a section that
stopped early and looks finished.

Pass only if BOTH:

1. the section's `## Status` names the stop reason `budget` with the counts
   behind it (25 touched, papers kept); and
2. the agent or the reply says the section is incomplete — the word
   "incomplete", or unambiguous equivalent wording.

Fail if the section claims `saturation` (the citations hop was `truncated`, so
saturation is forbidden anyway), or reports the crawl as done, or mentions the
budget only as a neutral statistic with no statement that coverage is partial.
