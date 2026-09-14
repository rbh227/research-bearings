# Cleanup: nothing unreferenced in the tree

Type: task
Status: ready-for-agent
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

- [ ] A list, on this ticket, of every deletion with one line of why, and
      every "parked" label added with its location.
- [ ] Both selftests green with the same or fewer cases, each remaining case
      still meaningful; static checks green; heading parity green.
- [ ] `TAG=snowball RUNS=1` still runs — the parked tier is intact.
- [ ] The grep list above returns nothing outside `docs/design/chunk-0[12]-*`
      and `evals/results/`.
