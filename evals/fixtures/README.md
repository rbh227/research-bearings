# Fixtures for the front-door cases

`assemble.sh <shape> [target]` builds a `research/` folder from the files the
live runs left under `landscape/runs/` and `read/runs/`. Three shapes: `empty`,
`wildfire` (question and landscape, no cards), `damage` (question, landscape,
three cards, datasets, groups, a bits file dated before two of the cards, one
critique). It copies and never invents; the dates it sets are explained at the
top of the script.

The router and composite cases each carry a `case.yaml` naming a `scaffold.sh`
that calls this script into the run's workspace. Scaffolds run only when asked,
and the router needs Bash for the state script, so a run is:

```bash
claude plugin eval . --case 'router-*' --scaffold --allow-tools "Bash(python3 *)"
```

The expected facts in each `llm` grader were read from
`python3 scripts/state.py <assembled folder>` on the day the case was written;
if the table in the state script changes, re-run it and change the graders.

To look at a shape by hand:

```bash
evals/fixtures/assemble.sh damage /tmp/dmg/research && python3 scripts/state.py /tmp/dmg/research
```
