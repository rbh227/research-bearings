# 08: guard cases and the heading registry

Type: task
Status: done
Blocked by: 04, 05, 06, 07

## What to build

**`check_headings.py`**: register the four new templates with their writers —
`ideas-log.md` → `/brainstorm` and `/ideas`; `idea.md` → `/ideas`;
`persona.md` → `agents/persona-ideator.md`; `diversity.md` →
`agents/diversity-planner.md`.

**`hooks/guard.py` selftest**: chunk 8's two agents, in the style of the chunk 7
block — the guard needs no change, and the cases are there to prove it rather
than assume it. Frontmatter cases: neither `persona-ideator` nor
`diversity-planner` grants Bash, WebSearch or WebFetch. Web cases: WebSearch
and WebFetch denied to both. Write cases: denied outside `research/`, allowed
into `research/ideas/`.

## Acceptance

- [x] `python3 scripts/check_headings.py` green with the four new registrations.
- [x] `python3 hooks/guard.py --selftest` green with the new cases, and the new-case count named in the commit.
- [x] No behaviour change in the guard itself — selftest and registry only.

## Resolution

2026-09-16. `scripts/check_headings.py` (four registrations),
`hooks/guard.py` (selftest only).

Heading parity green: 21 templates, 2 agent contracts. Guard 63 cases → 73, all
green, no behaviour change — the prefix rule already covered both agents and the
ten new cases prove it rather than assume it. Neither agent is granted Bash at
all, since neither retrieves.
