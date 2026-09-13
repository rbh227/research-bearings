---
type: llm
focus: last_message
weight: 3
---
No Semantic Scholar API key is configured, so `health` reports
`key_present: false`. Hops still run — the key is a SOFT requirement — but they
rate-limit heavily and coverage drops.

Pass only if the missing key is stamped at the top of the section file, under
`## Status`, in words a reader coming to the file weeks later would understand.

Fail if the degradation appears only as a console warning in the reply, or not
at all. Console warnings scroll away; `research/landscape/*.md` gets read later,
and by the merger. A section that ran degraded and does not say so is the
failure this case exists to catch.

Fail also if the agent REFUSED to run over the missing key. The key is soft. The
hard requirements are the two servers answering.
