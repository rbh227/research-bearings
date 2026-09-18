# 02: `/premortem` and `premortem-agent`

Type: task
Status: ready-for-agent
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

- [ ] The template carries every heading the agent's contract names, in order.
- [ ] The agent's frontmatter has no Bash and no web tools, and its refusals table names the novelty trap and the invented-constraint trap.
- [ ] The skill caps at five per run and says so when it truncates.
- [ ] A run with no argument proposes candidates and waits rather than proceeding.
- [ ] Every written pre-mortem ends in exactly one of the three verdict strings.
- [ ] No idea page is modified by any part of this ticket.
