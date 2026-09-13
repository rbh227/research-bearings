# Map: research-bearings, first slice

Label: wayfinder:map

## Destination

A spec for the first buildable slice of research-bearings, ready for `/to-spec`: the skill and agent set chosen from `academic.md`, their contracts, the schemas they share, and the retrieval plumbing. Done when nothing is left to decide before someone scaffolds it.

## Notes

- **Domain**: a Claude Code plugin that runs the research loop with typed skills and contract-bound agents. Glossary in `CONTEXT.md`: **map** is this artifact only; **landscape** is the plugin's literature deliverable; an **acceptance run** is the user's post-handoff trial.
- **Inputs**: `academic.md` is "the big sheet", the source rules every skill derives from. `research_plugin_build_plan.md` is one candidate proposal for the loop and its milestones, not the plan.
- **Standing decisions** (from the build plan, reaffirmed 2026-09-12): Claude Code plugin; this repo is its own marketplace (`marketplace.json` with `source: "./"`, like the Matt-Raphs-Skills fork), retiring `raph-cc`; v1 is eventually the full loop including experiment agents; Claude-only with the judge's `model:` field left open for a second provider; Python for the few scripts; local paper cache is the reference manager; one spec covers schemas and their first consumers together.
- **Retrieval plumbing**: three MCP servers, all **bundled by the plugin** as of chunk 2 and registered as `plugin:research-bearings:*`. `paper-search-mcp` (arXiv, Semantic Scholar, OpenAlex, Crossref, and more) and `openreview-mcp` are 1.x-SDK servers run as `uvx --with 'mcp<2'`; they read their own credentials from `~/.config/paper-search-mcp/.env`. `s2-snowball` is the plugin's own single-file server for the references/citations/batch hop, `mcp>=2,<3` under `uv run --script`, because neither of the others exposes references or citations (ticket 02). The user-scope entries for the first two were **removed** in chunk 2 — two live copies under two tool-name spellings is a trap that surfaces months later. The S2 key now arrives through the plugin's `userConfig`, stored in the Keychain, not from the `.env`.
- **Acceptance-run topic** (the user's real question, used for smoke runs, never a deliverable): post-disaster building damage assessment from aerial and satellite imagery, plus computer vision and AI in wildfires generally, including fire-spread prediction.
- **Skills to consult per session**: `grilling` and `domain-modeling` for every grilling ticket; `research` for research tickets; `prototype` for ticket 09. Plugin authoring follows `writing-for-agents`.
- **Repo**: https://github.com/rbh227/research-bearings. Tracker is local markdown under `.scratch/`.

## Decisions so far

<!-- one line per resolved ticket: [title](issues/NN-slug.md): gist -->
- [Plugin manifest facts](issues/01-plugin-manifest-facts.md): default layout needs no component fields; agents are dispatched as `plugin:agent`; bundled MCP tools are `mcp__plugin_<plugin>_<server>__<tool>`; guards go in `hooks.json` keyed on `agent_type`, not agent frontmatter; fan-out skills must stay inline; Python scripts need a SessionStart install. Contradicts the build plan on the `mcp` field name and manifest listing.
- [Write-scope guard mechanics](issues/03-write-scope-guard-mechanics.md): a plugin `PreToolUse` hook on `Write|Edit` that reads `agent_type` from stdin and denies paths outside `landscape/`; exit 2 or a `permissionDecision: deny` JSON blocks; per-agent scoping only via that stdin field; drop `Bash` from landscape agents with `disallowedTools`; Python guard, not `jq`.
- [Retrieval tool inventory](issues/02-retrieval-tool-inventory.md): no references or citations tool in either MCP; seed search via `search_semantic`, hops must hit the Semantic Scholar Graph API directly; the S2 key is effectively required (429 after two or three unauthenticated calls); Unpaywall email mandatory; arXiv-only papers snowball via `ARXIV:<id>`; pass `use_scihub=False`.
- [Snowball mechanism](issues/10-snowball-mechanism.md): the plugin owns a single-file MCP server, `servers/s2_snowball.py`, PEP 723 pinning `mcp>=2,<3`, run by `uv run --script`; three tools for references, citations, and batch; prototyped and verified live with an on-disk cache. Chosen over `uvx semantic-scholar-fastmcp` (runner-up) and over a Bash script (rejected: scouts must be denied Bash).
- [The research loop end to end](issues/05-research-loop-end-to-end.md): six stages plus presentation and a cross-cutting honesty layer; 27 typed skills, 5 composites, 28 agents; three human gates (question, idea selection, compute spend); a row earns its place by implementing the sheet *or* serving one of four goals, so only `/watch` and `/handoff` defer. Outline in `docs/design/skills-and-agents.md`.
- [The first slice](issues/06-first-slice-skill-set.md): chunk 1 is the plugin skeleton plus the question stage — `/setup` and `/frame`, one agent `question-critic`, no retrieval. Chosen because it is the only chunk not blocked on the pending S2 key. `/frame` is a diverge–converge loop with uninformed divergence labelled as such, re-entrant after `/surveys`.
- [Shared contracts](issues/07-shared-contracts.md): output root is `research/`, one guard rule. Three schemas only — `CONTEXT.md` (9 headings), `QUESTION.md` (11, deliverable), `framing-log.md` (working record). Methodology rules inlined per skill, not referenced; `academic.md` is not shipped. Deterministic check is `guard.py --selftest`.
- [Done-check for the spec](issues/08-spec-done-check.md): all three of structural checks, a nine-case `claude plugin eval` suite with the ablation arm, and a live smoke run on the acceptance-run topic outside this repo.
- [Snowball by hand](issues/09-snowball-by-hand.md): ran both hops live on two seeds. The 1 RPS throttle is wrong — 429s are non-deterministic, survive 1.1 s spacing, and never carry `Retry-After`; retry with jitter is what works. Backward hops reach 1981 and lose 5–12% of rows to unresolvable grey literature with ~50% missing abstracts; forward hops are clean but 73% missing `fieldsOfStudy`. `contextsWithIntent` returns the sentences describing each cited work — a better card field than the abstract. Dedupe belongs at the merger, not the scout.
- [Register paper-search](issues/04-register-paper-search.md): registered at user scope and connected. Semantic Scholar and CORE keys both verified live; credentials in `~/.config/paper-search-mcp/.env`, read by the server itself. The S2 references hop works on `ARXIV:<id>`. CORE is a full-text *retrieval* source, not a discovery one, and its endpoint 301-redirects to a trailing slash.

## Not yet specified

Chunk 1 is **specified and built** (`docs/design/chunk-01-question-stage.md`, §10 for
results). The plugin installs as `research-bearings@rbh227`; `/setup` and `/frame`
work; 8 of 9 eval cases score 1.00; the ninth needs a `Bash` grant this machine cannot
give. The live smoke run is the one outstanding item and needs the user.

Chunk 2 is **built, not yet verified** (`docs/design/chunk-02-scout.md`: §9 for
what the build changed and what three reviews found, §10 for results). The plugin
is 0.2.0 and bundles all three MCP servers; the user-scope `paper-search` and
`openreview` entries are gone. `servers/s2_snowball.py` is the citation walker,
12/12 on its offline selftest and verified live. `/scout` and `paper-scout` ship.

Two of four done-check tiers pass: structural, and the live plumbing check.
**The nine-case eval suite is written but has never been run**, so nothing about
the scout's behaviour rests on it yet. The §6.4 gold set needs the user, and
cannot be generated — a list produced by searching is not a test of whether
search finds things. One live end-to-end run went well but predates the
truncation fix and has not been repeated.

Chunk 2 was re-cut during specification: the map previously called it "the
landscape chain", but introducing bundled MCP servers, a server we wrote,
seven-way fan-out, a merger and a presentation layer at once means a mediocre
result diagnoses nothing. So chunk 2 became **retrieval plumbing plus one skill,
`/scout`** — the unit of work `/landscape` will fan out seven times, promoted to
user-facing so it can be judged before anything depends on it. It is now in
`docs/design/skills-and-agents.md` under Stage 2.

Both unknowns the spec flagged are resolved: `userConfig` does reach the server
from a local marketplace (spec §9.4), and `claude plugin eval` can grant MCP
tools with `--allow-tools mcp__*` plus `--mocks off` (§9.5).

What remains is chunk 3 and beyond:

- The landscape chain proper: `/surveys`, `/landscape`, `/brief` and their agents.
- The merger, and with it cross-scout dedupe (ticket 09 §5) and interpreted absence
  claims — both deliberately withheld from a single scout.
- The matrix-cell and dataset-row schemas, written with their first consumer. The
  paper-card contract lands in chunk 2, in its minimal scout form.
- Where CORE fits: full-text retrieval for an already-identified paper, feeding the
  reader agents. Not a discovery source.
- Whether `/frame`'s re-entry after `/surveys` is automatic or user-triggered.
- Whether abandoned directions need their own agent, rather than a general scout
  stamping the question as not retrieval-shaped.

## Out of scope

- Everything past the first slice: later milestones, ideation, experiments, the living map, composites like `/map`.
- Executing the wildfire research itself. The plugin is the deliverable; the acceptance run is the user's.
- Zotero or any external reference manager.
- The `raph-cc` marketplace beyond retiring it.
