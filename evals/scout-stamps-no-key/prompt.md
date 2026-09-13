---
tags: [ci, scout]
timeout_seconds: 600
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, mcp__plugin_research-bearings_s2-snowball__health, mcp__plugin_research-bearings_s2-snowball__get_references, mcp__plugin_research-bearings_s2-snowball__get_citations, mcp__plugin_research-bearings_s2-snowball__get_papers_batch, mcp__plugin_research-bearings_paper-search__search_openalex, mcp__plugin_research-bearings_paper-search__search_semantic, mcp__plugin_research-bearings_paper-search__search_arxiv]
---

<!-- The eval sandbox gives the child a CLEAN HOME, so neither
     ~/.config/paper-search-mcp/.env nor the plugin's semantic_scholar_api_key
     userConfig value is present. `health` therefore reports key_present: false
     on every harness run, with no setup required. Measured 2026-09-13 from the
     kept sandbox of a timed-out run.

     That is why this case is in `ci` after all. The chunk-2 spec assumed the
     no-key path could only be forced by hand on an unkeyed machine (§9.6); the
     harness forces it automatically, for every scout case. This one is simply
     the case that asserts on it. -->

Scout the literature on building damage assessment from satellite imagery.
Budget 40 papers touched. Don't ask me anything first.

When it's done, show me the full contents of the section file it wrote.
