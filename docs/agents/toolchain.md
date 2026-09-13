# Toolchain

The four verbs skills use instead of hardcoded stack commands. A verb whose value is `none` is skipped, never guessed.

This repo is a Claude Code plugin. There is no compiler and no package manager, but there are real checks: manifest validation, a heading-parity check between templates and the skills that write them, a selftest on the write-scope guard, and a behavioural eval suite.

| Verb | Command |
| --- | --- |
| build | `none` |
| static checks | `claude plugin validate ./ --strict && python3 scripts/check_headings.py` |
| one test file | `python3 hooks/guard.py --selftest` |
| full suite | `claude plugin eval ./ --tag ci --trust-plugin --judge-model sonnet --allow-tools Write Edit Agent --threshold 0.8` |

Consumers: `/implement`, `/tdd`, `/codex-review`, `/run-tickets`. Run **static checks** before every commit, **one test file** per red-green slice, and **full suite** once before a review gate.

Notes:

- **Static checks and one test file are free and fast.** Run them freely.
- **The full suite launches a real Claude child per case**, three runs each by default, plus a no-plugin baseline arm. `--runs 1 --ablation none` is fine while iterating but is **not** a pass: single-run LLM grading is noisy and has twice failed correct behaviour here. Use the full form before any gate.
- **`--judge-model sonnet` matters.** The default judge is `haiku`, which has misread nuanced criteria in this suite — twice marking correct output as failing. Anything judged on reasoning rather than presence needs the stronger judge.
- **`--allow-tools Write Edit Agent` is required.** Those tools are gated; without the grant, cases fail for reasons that look behavioural.
- **`--tag ci`** excludes `setup-checks-before-asking`, which needs a `Bash` grant this machine cannot give (Docker symlinks; see the chunk 1 spec §9).
- `--trust-plugin` skips the first-run trust prompt, which is what CI needs. `--scaffold` is pointless here: `scaffold_script` is accepted by the schema but never executes.
