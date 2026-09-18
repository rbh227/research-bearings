# 06: `/baseline`, `/replicate` and `baseline-reproducer`

Type: task
Status: done
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

- [x] The published number is recorded with the card and the table it came from, or the file says it could not be found and what was checked.
- [x] The reproduction plan is numbered steps a human can run.
- [x] No agent or skill in this ticket executes the user's code.
- [x] `## Reproduction status` is exactly one of the three strings.
- [x] A number that would not reproduce lands as `contested` with what was tried.
- [x] A `/replicate` file states that its gap is a fact about the pipeline.

## Resolution

2026-09-18. `templates/research/baseline.md`, `agents/baseline-reproducer.md`,
`skills/baseline/SKILL.md`, `skills/replicate/SKILL.md`. Heading parity green.

**The target is the table's number, never the abstract's.** An abstract's
headline figure is usually the best of several conditions, so reproducing it
means reproducing that condition rather than the one being compared against.
Both the agent's contract and its refusals table say so, and the template's
first heading asks for the table number and the condition beside it.

**What the paper does NOT say is its own paragraph.** Musgrave's finding is that
the unstated pieces are where reproductions go, so the setup section names them
explicitly rather than describing only what is stated. A dimension that cannot
be determined is written `unknown, <what was checked>` and never assumed to
match.

**`contested` requires the attempt list, and the refusal says why.** It is a
claim that somebody's published number did not reproduce. Without the attempts,
the conditions varied and the numbers reached, it is a complaint about their
work. The contract also says what it is not: not an accusation, and not a
failure of the reproduction.

**`/replicate` is its own skill because the meaning has to be fixed before the
run.** A gap discovered on a paper you have no stake in is a gap you will read
as the paper's fault. Naming the run a calibration first is the only version
that tests anything, so the skill refuses a paper the researcher is building on
and writes the sentence that keeps the file readable a year later.

**The calibration's output is the comparison, not the gap.** The skill lists
every other gap under `research/baselines/` beside this one, with the three
readings spelled out: a gap only in the baselines, a gap in both, and a
calibration gap larger than the baselines — which means the setup is wrong in a
way the researcher's own work has been hiding.

**The agent's Bash is the fetch verb and nothing else**, enforced by the guard
rather than by its prose. It writes the plan; the researcher runs it.
