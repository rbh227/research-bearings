# 04: `/spec`, the Heilmeier page

Type: task
Status: ready-for-agent
Blocked by: 02, 03

## What to build

The page a survivor earns: one page somebody with ten minutes can read.

**`templates/research/heilmeier.md`** — comment-only, eight headings for the
eight Heilmeier questions, plus `## Sources` and `## Status`.

**`skills/spec/SKILL.md`** — Read, Glob, Write. **No agents**: this is a page
written from files that already exist. Reads the idea page, its pre-mortem,
`RANKING.md`, `QUESTION.md`, and any card the idea names. Writes
`research/specs/<slug>.md`: the eight questions as eight paragraphs.

**Every factual sentence names where it came from.** A Heilmeier page that
cannot source its "how is it done today" is answering from memory, and that is
the one failure this skill exists to prevent.

**The midterm and final checks are dated and testable**, so "how will you know"
has an answer before the work starts.

**The one-page test is applied and reported.** Over roughly 800 words the skill
says so in `## Status`: by the catechism's own rule it is still a brainstorm.

This skill absorbs the Heilmeier one-pager Milestone 2 deferred as `/brief`.
`/brief` and `brief-writer` leave the planned list; `/render` and `/figure` stay
planned.

## Acceptance

- [ ] All eight Heilmeier questions are answered in eight paragraphs on one page.
- [ ] Every factual sentence carries its source file, and `## Sources` lists them.
- [ ] The midterm and final checks are dated and testable.
- [ ] A page over about 800 words is reported as still a brainstorm.
- [ ] The skill refuses an idea with no pre-mortem and says which one is missing.
- [ ] No agent is dispatched.
