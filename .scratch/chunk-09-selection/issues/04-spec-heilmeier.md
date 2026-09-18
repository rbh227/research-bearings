# 04: `/spec`, the Heilmeier page

Type: task
Status: done
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

- [x] All eight Heilmeier questions are answered in eight paragraphs on one page.
- [x] Every factual sentence carries its source file, and `## Sources` lists them.
- [x] The midterm and final checks are dated and testable.
- [x] A page over about 800 words is reported as still a brainstorm.
- [x] The skill refuses an idea with no pre-mortem and says which one is missing.
- [x] No agent is dispatched.

## Resolution

2026-09-18. `templates/research/heilmeier.md`, `skills/spec/SKILL.md`. Heading
parity green. No agents, as specified.

**No agent, and the skill says why.** An agent here would have to be handed
every file and could still answer question 2 from training rather than from a
card. The sourcing IS the work, so it happens in the main thread where the files
already are.

**An unsourced sentence may exist; it may not be invisible.** The alternative
rules both fail: forbidding them produces a page that omits what is true but
uncited, and allowing them silently produces a hallucination with eight
headings. So they are written as `not established in the cards I read` in place
and listed under `## Sources` as `unsourced:`.

**The risks paragraph is the pre-mortem's paragraph.** It is drawn from
`## What would have to be true that probably is not` and `## Verdict`, cited, and
the skill refuses an idea with no pre-mortem for exactly this reason: question 5
would otherwise be written from imagination. A risks section gentler than the
judge it came from is the page overruling its judge with no new evidence, and
that gets its own refusals row.

**The one-page test is reported, never enforced.** The skill counts the eight
answers and writes the verdict; it does not trim. A page cut to fit and a page
that fit are different findings, and only one of them means the idea is
understood.

**Two refusals and one warning.** No pre-mortem and `not executable as written`
both refuse. Not appearing in `RANKING.md` is a warning and the page is still
written — an unranked idea is a workflow state, not a defect in the idea.

**`/brief` is retired here, not deferred.** Milestone 2 deferred "the Heilmeier
one-pager" under that name; this is that page. The skill says so, and ticket 11
removes `/brief` from the planned list.
