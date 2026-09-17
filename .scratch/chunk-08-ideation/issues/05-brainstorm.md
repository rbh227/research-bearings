# 05: `/brainstorm`

Type: task
Status: done
Blocked by: 01, 04

## What to build

`skills/brainstorm/SKILL.md` (Read, Glob, Grep, Write, Edit, AskUserQuestion,
Agent — no Bash). Appends to `research/IDEAS.md`; dispatches four to six
`persona-ideator` agents in one message.

The loop, per the spec:

1. **Input**, in order, each overriding the last: `QUESTION.md` and
   `CONTEXT.md`; `BITS.md`, cards, ledgers, analog pages if they exist; the
   invocation text. With none of them the run is unframed and says so.
2. **The three banks, in this order.** Hamming (what are the important
   problems, why are you not working on them), then Polya's seven
   transformations one at a time with what falls out of each recorded even
   when it is "nothing", then the stakeholders. **Feasibility is not asked
   here** — `/premortem` owns it, and importance-before-feasibility is the
   rule, not a preference.
3. **Personas from the record**: the decision-maker in `QUESTION.md`, the labs
   in the groups ledger, the venues on the cards, the dataset producers in the
   datasets ledger, the adjacent fields on the analog pages. Each carries a
   one-line warrant. With none of those files, fall back to the five STORM
   roles and stamp the personas unwarranted.
4. **Dispatch** all personas in one message with the persona, its warrant, the
   question, the paths it may read, and its output path.
5. **The union, attributed** — near-duplicate questions from two personas stay
   two lines.
6. **Append everything to `IDEAS.md`** with its source, and say what `/ideas`
   would do with it.

Decides nothing: no ranking, no novelty claim, no page.

## Acceptance

- [x] The skill names every heading of `templates/research/ideas-log.md`.
- [ ] Runs with no landscape and no cards, from `QUESTION.md` or the invocation text alone, and stamps the run unframed. **Not run** — written and readable, never executed; build-only chunk.
- [ ] Persona count is capped at six and each persona carries a warrant or is stamped unwarranted. **Cap and warrant rule are in the skill; no dispatch has happened.**
- [x] Nothing in the skill ranks, scores, or claims novelty; the refusals table says why.
- [x] Plugin validation green; heading parity green.

## Resolution

2026-09-16. `skills/brainstorm/SKILL.md`, 192 lines.

The three banks in a fixed order, with feasibility excluded from the skill
entirely — that ordering is the ticket's main content and it is written as the
rule, with Hamming's reason beside it. Polya's seven transformations are a table
of seven prompts, and a transformation that yields nothing is recorded as
nothing.

Personas come from five file sources in priority order, each with a quoted
warrant, falling back to STORM's five roles stamped unwarranted. Six is the cap
and the whole fan-out.

**No Bash.** The skill retrieves nothing; putting a candidate to the index is
`/ideas` step 3, and the separation is why this one can run before any source is
connected.
