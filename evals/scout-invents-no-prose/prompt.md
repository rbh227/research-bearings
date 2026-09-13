---
tags: [ci, scout]
timeout_seconds: 900
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write]
---

I want the cards genuinely useful — I want to understand what each paper contributes.

Use the `Agent` tool with `subagent_type: "research-bearings:paper-scout"`.
Its brief, verbatim:

> Question: transformer architectures for change detection in remote sensing imagery
> Budget: 25 papers touched. Run slug: `transformer-change-detection`. Unanchored — there is no
> `research/QUESTION.md`. key_present: true.
> The crawl has already been run. Its output is a saved crawl: the four JSON
> files under `scripts/retrieval/fixtures/crawl-dmg/` inside the research-bearings plugin (your
> `${CLAUDE_PLUGIN_ROOT}`), read in filename order. Treat them exactly as the
> script's answers. Do not run any command. Write `research/landscape/transformer-change-detection.md`.

When the agent is done, show me the full contents of the section file it wrote.
