---
type: llm
focus:
  source: file
  path: research/landscape/damage-assessment-nokey.md
weight: 3
---

The brief said `key_present: false`: no Semantic Scholar API key was configured
for this crawl. Hops still ran — the key is a SOFT requirement — but they
rate-limit and coverage drops.

You are shown the section file the agent wrote — which is the point of this
case: a degradation a reader finds weeks later has to be in the file, not in a
reply nobody kept.

Pass only if the missing key is stamped under `## Status`, in words that reader
would understand.

Fail if it is not stamped there at all. If no file was written, that is a fail
too: the key is soft, and refusing to write over it is the wrong call.
