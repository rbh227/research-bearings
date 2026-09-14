---
tags: [ci, scout]
timeout_seconds: 900
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write]
---

Some of what that paper cites is technical reports and challenge write-ups rather
than papers, and that material matters to me, so make sure I can see it.

Use the `Agent` tool with `subagent_type: "research-bearings:paper-scout"`.
Its brief, verbatim:

> Question: the literature reachable from arXiv paper 2405.04800 (DeepDamageNet) — its references and citations
> Budget: 25 papers touched. Run slug: `deepdamagenet-neighbourhood`. Unanchored — there is no
> `research/QUESTION.md`. key_present: true.
> The crawl has already been run. Its output is a saved crawl: the four JSON
> files under `scripts/retrieval/fixtures/crawl-dmg/` inside the research-bearings plugin (your
> `${CLAUDE_PLUGIN_ROOT}`), read in filename order. Treat them exactly as the
> script's answers. Do not run any command. Write `research/landscape/deepdamagenet-neighbourhood.md`.

When the agent is done, tell me in a sentence or two where it landed. The file
it wrote is the record — don't paste it back at me.
