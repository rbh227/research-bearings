# 02: `/premortem` and `premortem-agent`

Type: task
Status: done
Blocked by: —

## What to build

The skill that attacks an idea in execution, and the agent that does it.

**`templates/research/premortem.md`** — comment-only style, every heading
present, every heading's contents described in a comment. Seven headings: the
idea restated in the agent's own words (so a misreading is visible), the
baselines it must beat and whether each exists and runs, the field's own metric
and whether the idea uses it, the evaluation plan and what it depends on, what
would have to be true that probably is not, the three-state verdict, and what
would change the verdict.

**`agents/premortem-agent.md`** — Read, Write. No Bash, no web tools. Same shape
as the existing agents: frontmatter with `name`, `description`, `tools`,
`model: inherit`, a heading contract and a refusals table. Writes
`research/premortems/<slug>-<date>.md`.

It judges **execution, not novelty.** Novelty was settled at `/ideas` by
retrieval and re-litigating it here is the failure mode this agent exists to
avoid; its refusals table says so. Feasibility is judged in the user's stated
compute and time, taken from `CONTEXT.md`. Where `CONTEXT.md` does not say, it
writes `constraint unknown` and names what it assumed — never a silent
assumption of a cluster.

The verdict is one of exactly three: `executable`, `executable with changes`,
`not executable as written`.

**`skills/premortem/SKILL.md`** — Read, Glob, Grep, Write, AskUserQuestion,
Agent. With no arguments, proposes every idea page with no pre-mortem, newest
first, and waits. With slugs, takes those. **Cap: five per run**, the same cap
`/read` uses. One agent per idea, dispatched in one message, each with only the
idea page, `QUESTION.md`, `CONTEXT.md`, and the card paths the idea names.
Reports the pre-mortems written and the count in each of the three states.

The pre-mortem is its own file. **The idea page is never edited** — a judge does
not rewrite what it judges, and chunk 8's nine idea headings are a shipped
contract.

## Acceptance

- [x] The template carries every heading the agent's contract names, in order.
- [x] The agent's frontmatter has no Bash and no web tools, and its refusals table names the novelty trap and the invented-constraint trap.
- [x] The skill caps at five per run and says so when it truncates.
- [x] A run with no argument proposes candidates and waits rather than proceeding.
- [x] Every written pre-mortem ends in exactly one of the three verdict strings.
- [x] No idea page is modified by any part of this ticket.

## Resolution

2026-09-18. `templates/research/premortem.md`, `agents/premortem-agent.md`,
`skills/premortem/SKILL.md`. Heading parity green.

**Eight headings, not the seven the spec named.** The seven judgement headings
are exactly as specified; `## Status` is the eighth, carrying the date, the
paths read and what could not be checked. Every one of the other twenty-one
templates in this repo ends that way, and the `constraint unknown` state needs
somewhere to be visible without reading the whole file. The deviation is here
rather than silent.

**The verdict line has a fixed shape.** `- Verdict: <state>` as the first line
of `## Verdict`, one of exactly three strings, because `/rank` sets ideas aside
on it and `/design` refuses on it. A downstream skill reading prose for a
three-state value is how a fourth state gets invented.

**`executable with changes` is defined by nameability.** The agent's contract
says it plainly: if the changes cannot be named, the state is `not executable as
written`. Without that, the middle state is where every uncertain idea lands and
the three states collapse into one.

**The novelty refusal is the agent's largest section.** It has read no
literature beyond the cards it was handed, so an opinion about what exists is
exactly the hallucinated claim the plugin is built against. Its refusals table
has three separate entries for the ways that opinion sneaks back in — "done
before", "incremental", and judging whether the work is worth doing.

**Cards are resolved by the skill, not the agent.** The skill turns the idea
page's reference lines into paths under `research/papers/` and passes only the
ones that exist. A reference with no card is left out, so the agent reports what
it could not check rather than citing a file it does not have.
