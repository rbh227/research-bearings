# 08: `/log`, the notebook and `variance-checker`

Type: task
Status: ready-for-agent
Blocked by: 01, 07

## What to build

One append-only notebook, written to **before** the result is known.

**`templates/research/notebook.md`** — comment-only, for `research/NOTEBOOK.md`.
One entry shape: the date, the experiment page it belongs to, the config hash,
the seeds, and — attached later — the result and any refusal.

**`agents/variance-checker.md`** — Read, Write. Reads the ingest output and the
experiment page's variance plan and returns, per metric, whether the seed count
meets the plan. **A single-seed number is refused entry to any results table**,
and the refusal is written into the notebook entry rather than being a silent
omission.

**`skills/log/SKILL.md`** — Read, Glob, Bash, Write, Edit, AskUserQuestion,
Agent. Two modes, and the first is the point:

- `/log --start <slug>` appends the attempt to `research/NOTEBOOK.md` **before
  the run**, with the date, the experiment page, the config hash and the seeds.
- `/log <run-dir>` ingests afterwards through `ingest_runs.py` and attaches
  results to that entry by config hash.

An ingest that finds no opening entry **says so**: a run with no pre-registration
is a finding, not an error. The skill reports what the script found and what it
could not parse.

**The notebook is append-only.** No line of it is ever edited or deleted — an
attempt that embarrassed the user is still there. One notebook, not one per
experiment, because post-hoc selection is impossible only if every attempt lands
in the same place.

## Acceptance

- [ ] `--start` writes an entry before any run exists, and the entry names its experiment page.
- [ ] An ingest attaches to the opening entry by config hash.
- [ ] An ingest with no opening entry is reported as a finding with the run named.
- [ ] A single-seed metric is refused a table and the refusal text is in the notebook entry.
- [ ] Unparseable files are reported per file with the reason.
- [ ] No existing notebook line is edited or removed by any path through the skill.
