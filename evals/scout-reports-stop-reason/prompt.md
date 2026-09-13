---
tags: [ci, scout]
timeout_seconds: 1200
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, mcp__plugin_research-bearings_s2-snowball__health, mcp__plugin_research-bearings_s2-snowball__get_references, mcp__plugin_research-bearings_s2-snowball__get_citations, mcp__plugin_research-bearings_s2-snowball__get_papers_batch, mcp__plugin_research-bearings_paper-search__search_openalex, mcp__plugin_research-bearings_paper-search__search_semantic, mcp__plugin_research-bearings_paper-search__search_arxiv]
---

Scout the literature on deep learning for wildfire spread prediction. Use a
budget of 25 papers touched — I know that is small, I want to see what happens.
Don't ask me anything first.

When it's done, show me the full contents of the section file it wrote.
