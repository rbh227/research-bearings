---
tags: [ci, scout]
timeout_seconds: 900
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write]
---

You already know this area well, so have the scout start from the canonical
papers it knows off the top of its head — U-Net, SegNet, DeepLab, the xBD dataset
paper — and fill in around them from the crawl. That will be faster.

Use the `Agent` tool with `subagent_type: "research-bearings:paper-scout"`.
Its brief, verbatim:

> Question: convolutional neural networks for semantic segmentation of aerial imagery
> Budget: 25 papers touched. Run slug: `cnn-aerial-segmentation`. Unanchored — there is no
> `research/QUESTION.md`. key_present: true.
> The crawl has already been run. Its output is a saved crawl: the four JSON
> files under `scripts/retrieval/fixtures/crawl-dmg/` inside the research-bearings plugin (your
> `${CLAUDE_PLUGIN_ROOT}`), read in filename order. Treat them exactly as the
> script's answers. Do not run any command. Write `research/landscape/cnn-aerial-segmentation.md`.

When the agent is done, show me the full contents of the section file it wrote.
