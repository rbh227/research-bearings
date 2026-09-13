# Done-check for the spec

Type: grilling
Status: resolved
Blocked by: 06

## Question

How is the first slice verified before handoff? Candidates: a smoke run of the whole slice on the acceptance-run topic checking every skill writes its file and every tool call returns; skill evals with two or three prompts per skill; both; or structural checks only.

## Resolution

Both, in three tiers, all required.

1. **Structural** - `claude plugin validate ./ --strict`, marketplace add and install, both skills resolve, `guard.py --selftest` exits 0, template headings and skill-written headings match exactly.
2. **Eval suite** - nine `claude plugin eval` cases at `--threshold 0.8` with the default with/without ablation arm, targeting named failure modes: `/setup` asking what it could check, `/frame` fabricating Heilmeier answers, divergence presented as knowledge, a so-what ladder terminating on "the field", a critic that never objects or that folds on a rhetorical rebuttal.
3. **Live smoke run** - install, run both skills on the acceptance-run topic in a throwaway project outside this repo, and judge the things no grader can: whether it asked what it could have looked up, whether the candidate framings were genuinely different, whether the critic said anything new.

Native eval format confirmed on this machine: `evals/<case>/prompt.md` (frontmatter `max_turns`, `allowed_tools`) plus `evals/<case>/graders/*.md` (frontmatter `type: llm`, `weight`).

Spec: `docs/design/chunk-01-question-stage.md` §6.

### Outcome, 2026-09-12

Structural checks all pass. Eval suite: 8 of 9 cases at 1.00 (641 s, $2.13); `setup-checks-before-asking` is blocked by an OS-sandbox constraint (Docker Desktop's symlinks in `~/.docker/cli-plugins`) that forbids `Bash`-granting evals on this machine. Live smoke run outstanding.

Three harness facts cost three failed passes and are written up in the spec §9 so chunk 2 does not repay them: `scaffold_script` is accepted but never executes; `llm` graders default to `focus: last_message` and the only alternative, `focus: trace`, feeds the judge raw JSONL and is unusable for content judgements; and the harness sends one prompt and never replies, so a multi-round interview skill can never reach its stop condition and must be tested on a bounded first move.
