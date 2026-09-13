# Toolchain

The four verbs skills use instead of hardcoded stack commands. A verb whose value is `none` is skipped, never guessed.

This repo is a Claude Code plugin. There is no compiler and no package manager, but there are real checks: manifest validation, a heading-parity check between templates and the skills that write them, a selftest on the write-scope guard, and a behavioural eval suite.

| Verb | Command |
| --- | --- |
| build | `none` |
| static checks | `claude plugin validate ./ --strict && claude plugin validate skills/ --strict && claude plugin validate agents/ --strict && python3 scripts/check_headings.py` |
| one test file | `python3 hooks/guard.py --selftest && python3 servers/s2_snowball.py --selftest` |
| full suite | `claude plugin eval ./ --tag ci --trust-plugin --judge-model sonnet --mocks off --allow-tools Write Edit Agent WebSearch 'mcp__plugin_research-bearings_s2-snowball__*' 'mcp__plugin_research-bearings_paper-search__*' --threshold 0.8` |

Consumers: `/implement`, `/tdd`, `/codex-review`, `/run-tickets`. Run **static checks** before every commit, **one test file** per red-green slice, and **full suite** once before a review gate.

Notes:

- **Static checks and one test file are free and fast.** Run them freely.
- **`validate ./` alone is weaker than it looks.** Pointed at this repo it validates the *marketplace* manifest and stops, because `marketplace.json` is what it finds first. Skill and agent frontmatter is only checked when you point it at `skills/` and `agents/` directly — hence three calls. Pointing it at a single `.md` file does not work: it tries to parse the file as a JSON manifest.
- **`validate .claude-plugin/plugin.json --strict` fails on this repo by design.** It walks components and warns that a root `CLAUDE.md` is not loaded as plugin context. That warning is correct and permanent: this repo is both the plugin and a project, and the `CLAUDE.md` is the project's. Not part of the verb.
- **The full suite launches a real Claude child per case**, three runs each by default, plus a no-plugin baseline arm. `--runs 1 --ablation none` is fine while iterating but is **not** a pass: single-run LLM grading is noisy and has twice failed correct behaviour here. Use the full form before any gate.
- **`--judge-model sonnet` matters.** The default judge is `haiku`, which has misread nuanced criteria in this suite — twice marking correct output as failing. Anything judged on reasoning rather than presence needs the stronger judge.
- **`--allow-tools` is required, and now covers MCP.** `Write Edit Agent` are gated; so are `mcp__*` tools. Without the grant, cases fail for reasons that look behavioural. Probed 2026-09-13: `--allow-tools` accepts `mcp__*` patterns, so the scout suite has automated cover.
- **`WebSearch` must be granted, even though no skill uses it.** `scout-refuses-without-snowball` tests that the scout refuses a *tempting available fallback*. Without the grant the harness reports `not granted: WebSearch` and the case passes for the wrong reason — there was nothing to refuse. Measured 2026-09-13.
- **`--mocks off` starts the real retrieval servers.** The default, `record`, does not start a plugin server that has no mock, so every scout case would fail its precondition check. `off` starts them as you, outside the OS sandbox — which is fine for a plugin you wrote, and is the only way to exercise a live hop.
- **`--tag ci`** excludes `setup-checks-before-asking`, which needs a `Bash` grant this machine cannot give (Docker symlinks; see the chunk 1 spec §9).
- **Scout cases run a reduced budget.** The harness times out at 600 s and a full 250-paper crawl does not fit. Budget is a parameter of the skill, not a constant, for exactly this reason.
- `--trust-plugin` skips the first-run trust prompt, which is what CI needs. `--scaffold` is pointless here: `scaffold_script` is accepted by the schema but never executes.
