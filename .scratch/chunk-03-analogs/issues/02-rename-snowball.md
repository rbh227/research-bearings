# Rename: the snowball skill becomes `/snowball`; `/scout` is freed

Type: task
Status: ready-for-agent
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

- [ ] `grep -rn "research-bearings:scout\|/scout\b" --include=*.md .` outside
      `docs/design/chunk-0[12]-*.md` and `evals/results/` returns nothing that
      means the snowball.
- [ ] `claude plugin validate skills/ --strict` green; heading parity green
      (`section.md` → `skills/snowball/SKILL.md`).
- [ ] `TAG=snowball CASE=snowball-refuses-without-script RUNS=1` passes: the
      renamed skill still refuses without the script.
- [ ] Both chunk specs carry one line each saying the skill was renamed and
      why, dated.
