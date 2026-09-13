---
tags: [ci, scout]
timeout_seconds: 1200
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, mcp__plugin_research-bearings_s2-snowball__health, mcp__plugin_research-bearings_s2-snowball__get_references, mcp__plugin_research-bearings_s2-snowball__get_citations, mcp__plugin_research-bearings_s2-snowball__get_papers_batch, mcp__plugin_research-bearings_paper-search__search_openalex, mcp__plugin_research-bearings_paper-search__search_semantic, mcp__plugin_research-bearings_paper-search__search_arxiv]
---

<!-- ARXIV:2405.04800 (DeepDamageNet) has 25 references, 3 of which have no
     Semantic Scholar record: an Imantics documentation page, a crowdsourced
     damage technical report, and the CrowdAI mapping challenge baseline. -->

Scout the literature reachable from arXiv paper 2405.04800 — walk its
references and citations. Budget 20 papers touched. Some of what it cites is
technical reports and challenge write-ups rather than papers, and that material
matters to me, so make sure I can see it. Don't ask me anything first.

When it's done, show me the full contents of the section file it wrote.
