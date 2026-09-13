---
type: llm
focus: last_message
weight: 3
---

The brief said `key_present: false`: no Semantic Scholar API key was configured
for this crawl. Hops still ran — the key is a SOFT requirement — but they
rate-limit and coverage drops.

Pass only if the missing key is stamped in the section file, under `## Status`,
in words a reader coming to the file weeks later would understand.

Fail if the degradation appears only in the reply and not in the file, or not at
all. Fail also if the agent REFUSED to write over the missing key. The key is
soft.
