# 10: guard cases and the heading registry

Type: task
Status: ready-for-agent
Blocked by: 02, 03, 04, 06, 07, 08, 09

## What to build

The fence proved for every agent this chunk added, and every template bound to
its writer.

**`hooks/guard.py` selftest** gains, for all nine new agents —
`premortem-agent`, `tournament-judge`, `baseline-reproducer`,
`experiment-designer`, `ablation-planner`, `variance-checker`,
`results-tabulator`, `results-critic`, `failure-mode-auditor`:

- a frontmatter case, so an agent's declared tools match what the guard allows;
- a web case, so no new agent can reach a web tool;
- write-scope cases for the four new directories — premortems, specs, baselines,
  experiments, results — plus `RANKING.md` and `NOTEBOOK.md`;
- a Bash case per agent: denied for the seven with no Bash, and allowed only for
  `ingest_runs.py` for the three that have it.

**`scripts/check_headings.py`** registers the seven new templates with their
writers: premortem → `premortem-agent`; ranking → `/rank`; heilmeier → `/spec`;
baseline → `baseline-reproducer`; experiment → `experiment-designer`; notebook →
`/log`; result → `results-tabulator`.

## Acceptance

- [ ] `python3 hooks/guard.py --selftest` is green and every new agent has a frontmatter, web, write-scope and Bash case.
- [ ] No new agent can write outside `research/`.
- [ ] Exactly three agents may run Bash, and only `ingest_runs.py`.
- [ ] `python3 scripts/check_headings.py` is green with all seven new templates registered.
- [ ] A skill or agent claiming a heading no template carries is caught.
