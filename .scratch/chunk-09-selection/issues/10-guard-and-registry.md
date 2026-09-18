# 10: guard cases and the heading registry

Type: task
Status: done
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
- a Bash case per agent: denied for the six with no Bash, and allowed only for
  `ingest_runs.py` for the three that have it.

**`scripts/check_headings.py`** registers the seven new templates with their
writers: premortem → `premortem-agent`; ranking → `/rank`; heilmeier → `/spec`;
baseline → `baseline-reproducer`; experiment → `experiment-designer`; notebook →
`/log`; result → `results-tabulator`.

## Acceptance

- [x] `python3 hooks/guard.py --selftest` is green and every new agent has a frontmatter, web, write-scope and Bash case.
- [x] No new agent can write outside `research/`.
- [x] Exactly three agents may run Bash, and only `ingest_runs.py`.
- [x] `python3 scripts/check_headings.py` is green with all seven new templates registered.
- [x] A skill or agent claiming a heading no template carries is caught.

## Resolution

2026-09-18. `hooks/guard.py` at 133 cases, `scripts/check_headings.py` with all
seven templates and the judge's four output headings. Everything green.

**The ticket said seven agents with no Bash; it is six.** Nine agents, three
granted Bash — `baseline-reproducer`, `results-tabulator`,
`failure-mode-auditor` — and six without. The ticket text was wrong and has been
corrected in place rather than left to be read later as a missing case.

**What actually stops the six is their frontmatter, not the fence.** The guard's
Bash rule admits any agent this plugin ships to the plugin's own scripts, so a
`results-critic` granted Bash could run the ingester. It is not granted Bash,
and the selftest reads that out of the file rather than assuming it — the same
mechanism chunk 8 used for `predictor`.

**Each of the three that may run something is checked in both directions**: the
ingester allowed, `python3 train.py` denied. Nine agents times four properties —
WebSearch, WebFetch, write scope out, write scope in — plus six Bash cases.

**One case is about a file that is not under research/ at all.** An agent
writing the project's own `train.py` is denied. The other write-scope cases use
`/tmp`, which is the easy case; the one that matters is an agent reaching into
the repository it is reading from.

**`tournament-judge` is registered in `AGENT_OUTPUTS`, not `CONTRACTS`.** Its
comparison file has no template because the file is read by `/rank` and by
nobody else, so the four headings live in its own contract — the same shape
`critic` and `question-critic` use.
