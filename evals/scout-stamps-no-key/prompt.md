---
timeout_seconds: 600
max_turns: 30
allowed_tools: [Read, Glob, Grep, Skill, Agent, Write, mcp__plugin_research-bearings_s2-snowball__health, mcp__plugin_research-bearings_s2-snowball__get_references, mcp__plugin_research-bearings_s2-snowball__get_citations, mcp__plugin_research-bearings_s2-snowball__get_papers_batch, mcp__plugin_research-bearings_paper-search__search_semantic, mcp__plugin_research-bearings_paper-search__search_arxiv]
---

<!-- NOT tagged ci. Needs a machine where the plugin's
     semantic_scholar_api_key userConfig value is unset, so health reports
     key_present: false.

     A case-level `env:` override does NOT work, measured 2026-09-13: .mcp.json's
     own env block sets SEMANTIC_SCHOLAR_API_KEY from ${user_config...}, and that
     wins over anything inherited from the parent process. Running a session with
     SEMANTIC_SCHOLAR_API_KEY="" still reports key_present: true.

     So this case runs by hand, on an unkeyed machine or after clearing the value
     with an uninstall / reinstall-without---config cycle. Same shape as chunk 1's
     setup-checks-before-asking, and the same reason it is out of the ci tag. -->

Scout the literature on building damage assessment from satellite imagery.
Budget 40 papers touched. Don't ask me anything first.

When it's done, show me the full contents of the section file it wrote.
