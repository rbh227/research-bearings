# 06: `/baseline`, `/replicate` and `baseline-reproducer`

Type: task
Status: ready-for-agent
Blocked by: —

## What to build

Reproducing the strongest published number, and the same machinery as a
calibration test.

**`templates/research/baseline.md`** — comment-only. Headings for the exact
published number with the card and table it came from, what the paper says about
its setup, what the user's setup differs in, the reproduction plan as numbered
steps the user can run, the achieved number and gap with conditions, and
`## Reproduction status`.

**`agents/baseline-reproducer.md`** — Read, Grep, Glob, Write, and Bash
restricted to this plugin's own scripts. Reads the card, the fetched full text,
the datasets ledger row, and the user's own code and data description. Writes
`research/baselines/<card-slug>.md`.

**It does not run anything.** The plan is written, the user runs it, the skill
records what came back. `## Reproduction status` is one of exactly three: `not
attempted`, `attempted, gap recorded`, `contested` — the last for a published
number that would not reproduce, with what was tried.

**`skills/baseline/SKILL.md`** and **`skills/replicate/SKILL.md`** — Read, Glob,
Grep, Bash, Write, AskUserQuestion, Agent. One card slug each. `/replicate` is
the same machinery pointed at a paper the user is **not** building on, and its
file says so: the gap is a fact about the user's pipeline, not about the paper.

## Acceptance

- [ ] The published number is recorded with the card and the table it came from, or the file says it could not be found and what was checked.
- [ ] The reproduction plan is numbered steps a human can run.
- [ ] No agent or skill in this ticket executes the user's code.
- [ ] `## Reproduction status` is exactly one of the three strings.
- [ ] A number that would not reproduce lands as `contested` with what was tried.
- [ ] A `/replicate` file states that its gap is a fact about the pipeline.
