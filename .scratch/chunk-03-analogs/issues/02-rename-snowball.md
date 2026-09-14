# Rename: the snowball skill becomes `/snowball`; `/scout` is freed

Type: task
Status: resolved
Blocked by:

## What

Spec §1, naming. `skills/scout/` → `skills/snowball/`, frontmatter `name:
snowball`, description rewritten to say what it is: a depth tool that walks
the citation neighbourhood of one question. `paper-scout` keeps its name. Every
reference follows: `CONTEXT.md` glossary (the retrieval terms describe "one
`/research-bearings:scout` run" — now `/snowball`), `README.md`, both chunk
specs (as history, with a note), `skills-and-agents.md` Stage 2, `hooks/`
comments, the eval suite.

The eval cases keep testing `paper-scout` by dispatching it directly, so most
prompts do not change. `scout-refuses-without-script` invokes the skill by
task description and must now invoke `/snowball`. Case directories rename
`scout-*` → `snowball-*`, tag `scout` → `snowball`, `run_evals.sh` comment and
`toolchain.md` follow. The chunk 2 spec's §11.10 table keeps the old names as
the record of that run.

## Acceptance

- [x] `grep -rn "research-bearings:scout\|/scout\b" --include=*.md .` outside
      `docs/design/chunk-0[12]-*.md` and `evals/results/` returns nothing that
      means the snowball.
- [x] `claude plugin validate skills/ --strict` green; heading parity green
      (`section.md` → `skills/snowball/SKILL.md`).
- [x] `TAG=snowball CASE=snowball-refuses-without-script RUNS=1` passes: the
      renamed skill still refuses without the script.
- [x] Both chunk specs carry one line each saying the skill was renamed and
      why, dated.

## Resolution

2026-09-14. `skills/scout` -> `skills/snowball`, `evals/scout-*` ->
`evals/snowball-*`, tag `scout` -> `snowball`, and every invocation in
CONTEXT.md, the templates, README, setup's resource table and
skills-and-agents.md. `paper-scout` keeps its name.

One change beyond the rename: `snowball-refuses-without-script` used to open
"Scout the literature on ..." and relied on the description matching that verb.
With the verb reassigned it names the skill outright, which is a better test of
a precondition anyway. Verified: 1.00, 59 seconds.

Chunk 2's spec carries a banner - everything below it reads `/scout` and means
`/snowball`.
