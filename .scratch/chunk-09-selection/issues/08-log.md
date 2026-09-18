# 08: `/log`, the notebook and `variance-checker`

Type: task
Status: done
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

- [x] `--start` writes an entry before any run exists, and the entry names its experiment page.
- [x] An ingest attaches to the opening entry by config hash.
- [x] An ingest with no opening entry is reported as a finding with the run named.
- [x] A single-seed metric is refused a table and the refusal text is in the notebook entry.
- [x] Unparseable files are reported per file with the reason.
- [x] No existing notebook line is edited or removed by any path through the skill.

## Resolution

2026-09-18. `templates/research/notebook.md`, `agents/variance-checker.md`,
`skills/log/SKILL.md`. Heading parity green.

**The result is appended as a second block, not written into the first.** The
spec said "attaches results to that entry"; the obvious reading is filling in a
`- Result:` line, and that is an edit. So the opening block carries only what is
known before the run and has no result field at all, and the ingest appends a
`#### Ingested <date>` block beneath it. The append-only claim then survives
contact with the second mode, and a planned seed count that disagrees with the
actual one stays visible as a disagreement rather than being corrected away.

**The only permitted operation on the notebook is inserting lines.** Stated in
the skill, in the template's `## The rule`, and enforced by having nowhere in
either contract that rewrites one. `Edit` is in the tool list to insert under an
anchor, never to change what is there.

**An ingest with no opening entry writes the entry anyway, marked `NONE`.**
Refusing it would hide a run that had no pre-registration, which is exactly what
somebody should see. It is a finding about the work and it stays.

**`short of plan` is deliberately not a refusal.** Three seeds where five were
planned is a real measurement with three seeds behind it; refusing it hides a
number and presenting it as five is a lie. The count travels with the number.
One seed is different in kind — there is no variance estimate at all, so there
is nothing to carry — and that is the only state that blocks a table.

**The refusal is written into the notebook, not omitted from a table.** A
single-seed number that quietly never appears looks identical to a number nobody
produced. That line is in the agent's contract, the skill and the template,
because it is the difference between a rule and a habit.

**`Seeds: not yet fixed` rather than the plan's number.** Copying the variance
plan into the entry before the run would record a plan as though it were a fact
about this run, and the later disagreement would be invisible.

**The variance checker groups by config hash and refuses to merge conditions.**
Two runs whose configs differ in anything but the seed are different conditions;
treating them as one is how a table averages across a change nobody noticed.

**Adversarial review, 2026-09-18.** The notebook entry and the ingest match were
keyed on the config hash, which includes the seed — a five-seed attempt could
never find its opening entry. Entries now carry both hashes and match on the
condition hash; `variance-checker` groups on it too.
