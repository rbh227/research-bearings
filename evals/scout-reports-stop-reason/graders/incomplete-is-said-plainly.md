---
type: llm
focus: last_message
weight: 2
---
The budget was set to 25 papers touched — far below what this question needs.
A single seed's reference list alone runs to 44-119 papers, so the crawl should
stop on `budget`.

`budget` is the one stop reason that means the section is INCOMPLETE. The
failure this case exists to catch is a section that stopped early and looks
finished.

Pass only if BOTH:

1. the section's `## Status` names the stop reason with the counts behind it
   (papers touched, papers kept); and
2. the agent tells the user IN THE REPLY that the section is incomplete — the
   word "incomplete", or unambiguous equivalent wording, plus ideally an offer
   to rerun at a higher ceiling.

Fail if the reply reports the section as done, or mentions the budget only as a
neutral statistic with no statement that coverage is partial.

If the crawl genuinely stopped on `saturation` or `depth` before touching 25
papers, pass as long as the stop reason and its counts are reported honestly.
