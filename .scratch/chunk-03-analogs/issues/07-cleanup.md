# Cleanup: nothing unreferenced in the tree

Type: task
Status: resolved
Blocked by: 02, 04, 05

## What

Spec §7. Last on purpose: it audits the tree after the rename and the new
skill have landed, so the audit is of the shape that ships. The rule is
**dead is deleted, parked is labelled**. The snowball skill, `paper-scout`,
`section.md`, the crawl fixtures and the snowball eval tier are parked — they
stay, they still run, and every place they appear says *parked* and why.
Anything else that nothing calls, reads, dispatches or links goes.

The audit, concretely:

- `scripts/retrieval/snowball.py` and `hooks/guard.py`: every top-level
  function has a caller in the file, a CLI verb, or a selftest case. List the
  ones that do not; delete them and their imports. Expect candidates from the
  MCP era that survived the port.
- `scripts/retrieval/fixtures/`: every file is read by a selftest case or an
  eval case. Delete the rest.
- `evals/`: every case dispatches a shipped agent or invokes a shipped skill
  by its current name. `evals/results/` is not audited — it is history — but
  confirm it is gitignored or decide to keep it and say why.
- `templates/`: every template is written by a shipped skill and registered
  in `check_headings.py`.
- Every shipped `.md` (skills, agents, templates, README, CONTEXT.md,
  `docs/agents/`): no reference to a path, tool, verb, skill, server, config
  block or eval case that no longer exists. `grep` for `servers/`,
  `.mcp.json`, `userConfig`, `mcp__`, `paper-search`, `openreview-mcp`,
  `s2-snowball`, `get_papers_batch`, `get_references`, `get_citations`,
  `--mocks`, `two-arm`, and the pre-rename skill name.
- `docs/design/`: the two earlier chunk specs are history and stay whole, but
  each gets a dated line at the top saying what in it is superseded and by
  what. `skills-and-agents.md` reflects the collapse of `/fingerprint`,
  `/analogs`, `/flip` into `/scout`, marks the landscape chain deferred, and
  the agent count drops accordingly.
- `research_plugin_build_plan.md` and `academic.md` are local, gitignored
  inputs — confirm they still are.

## Acceptance

- [x] A list, on this ticket, of every deletion with one line of why, and
      every "parked" label added with its location.
- [x] Both selftests green with the same or fewer cases, each remaining case
      still meaningful; static checks green; heading parity green.
- [x] `TAG=snowball RUNS=1` still runs — the parked tier is intact.
- [x] The grep list above returns nothing outside `docs/design/chunk-0[12]-*`
      and `evals/results/`.

## Resolution

2026-09-14. The audit found less dead code than expected and one real rename.

**Deleted:** nothing. Every top-level function in `snowball.py` (44),
`guard.py` (9), `check_headings.py` (3) and `check_analogs.py` (7) has a caller,
a CLI verb or a selftest case. Every fixture has a reader: the five loose ones
are named by selftest cases, and `crawl-dmg/` is read by the eval prompts as a
directory. The MCP era left no orphans behind — the port in ad68db7 took the
functions and left the wrapper.

**Renamed:** `get_papers_batch` → `batch_papers`, the last MCP-era name in
shipped code and the only one out of step with `hop`, `search`, `health` and
the CLI's own `batch` verb.

**Labelled parked**, in four places: `skills/snowball/SKILL.md`,
`agents/paper-scout.md`, the README's skill table and `toolchain.md`. Each says
the same thing — it works, its tier still runs, it is not being developed, and
nothing about it is deprecated.

**Design docs:** chunk 1 gained a banner, because "no `.mcp.json`, no
`servers/`, no `scripts/`" was true of chunk 1 and is no longer true of the
plugin. Chunk 2 already had one from ticket 02. `skills-and-agents.md` collapsed
`/fingerprint`, `/analogs` and `/flip` into `/scout`, deferred `/surveys` with
the rest of the landscape chain, and dropped the agent count from 28 to 23:
`analog-scout`, `field-carder`, `transfer-checker`, `flip-generator` and
`novelty-checker` are gone, because `/scout` does that work inline and its
`Nearest existing:` line is Nova's rule applied directly.

**Greps clean.** `servers/`, `.mcp.json`, `userConfig`, `mcp__`, `paper-search`,
`openreview-mcp`, `s2-snowball`, `get_papers_batch`, `get_references`,
`get_citations`, `--mocks`, `two-arm` and `evals/scout-` appear nowhere outside
the chunk specs (history, both bannered) and the tickets that record the
decisions. `evals/results/`, `academic.md`, `research_plugin_build_plan.md`,
`research/.papers/` and `research/.crawl/` are all gitignored and none is
tracked.

**Green:** manifests, heading parity, `check_analogs.py` 7/7, `guard.py` 30/30,
`snowball.py` 28/28, and the parked tier still runs — `snowball-refuses-without-script`
at 1.00.
