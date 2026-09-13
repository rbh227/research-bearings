# Toolchain

The four verbs skills use instead of hardcoded stack commands. A verb whose value is `none` is skipped, never guessed.

This repo is a Claude Code plugin. There is no compiler and no package manager, but there are real checks: manifest validation, a heading-parity check between templates and the skills that write them, a selftest on the write-scope guard, and a behavioural eval suite.

| Verb | Command |
| --- | --- |
| build | `none` |
| static checks | `claude plugin validate ./ --strict && claude plugin validate skills/ --strict && claude plugin validate agents/ --strict && python3 scripts/check_headings.py` |
| one test file | `python3 hooks/guard.py --selftest && python3 scripts/retrieval/snowball.py --selftest` |
| full suite | `scripts/run_evals.sh` — one invocation. No case needs a network, a key or a Bash grant. See the notes. |

Consumers: `/implement`, `/tdd`, `/codex-review`, `/run-tickets`. Run **static checks** before every commit, **one test file** per red-green slice, and **full suite** once before a review gate.

Notes:

- **Static checks and one test file are free and fast.** Run them freely.
- **`validate ./` alone is weaker than it looks.** Pointed at this repo it validates the *marketplace* manifest and stops, because `marketplace.json` is what it finds first. Skill and agent frontmatter is only checked when you point it at `skills/` and `agents/` directly — hence three calls. Pointing it at a single `.md` file does not work: it tries to parse the file as a JSON manifest.
- **`validate .claude-plugin/plugin.json --strict` fails on this repo by design.** It walks components and warns that a root `CLAUDE.md` is not loaded as plugin context. That warning is correct and permanent: this repo is both the plugin and a project, and the `CLAUDE.md` is the project's. Not part of the verb.
- **The full suite launches a real Claude child per case**, three runs each by default, one at a time — two children plus their tooling OOM this machine. `RUNS=1` is fine while iterating but is **not** a pass: single-run LLM grading is noisy and has twice failed correct behaviour here. Use the full form before any gate.
- **`--judge-model sonnet` matters.** The default judge is `haiku`, which has misread nuanced criteria in this suite — twice marking correct output as failing. Anything judged on reasoning rather than presence needs the stronger judge.
- **`--allow-tools` is required.** `Write Edit Agent WebSearch` are gated; without the grant, cases fail for reasons that look behavioural. `Bash` is gated too and is **never granted**: this machine cannot grant it inside the harness (chunk 1 spec §9), and no case needs it — the scout's agent cases replay a saved crawl, and `scout-refuses-without-script` exists precisely because the script cannot run without it. It is also a global operator grant that nothing can subtract from, which is why a denial case can never share an invocation with a grant it depends on (measured 2026-09-13; the two-arm runner that worked around it is gone with the servers).
- **`WebSearch` must be granted, even though no skill uses it.** `scout-refuses-without-script` tests that the scout refuses a *tempting available fallback*. Without the grant the harness reports `not granted: WebSearch` and the case passes for the wrong reason — there was nothing to refuse. Measured 2026-09-13.
- **`--tag ci`** excludes `setup-checks-before-asking`, which needs a `Bash` grant this machine cannot give (Docker symlinks; see the chunk 1 spec §9).
- **Scout cases replay a saved crawl.** `evals/fixtures/crawl-dmg/` is four real script responses — seeds, a backward hop with grey literature and missing abstracts, a truncated forward hop, a budget refusal. The cases judge what the agent *writes*; the crawl itself is covered by `snowball.py --selftest`, and finding things by the gold set. Writing twenty-odd cards is the slow part, which is why they carry 900 s: with the budget enforced, 40 papers touched took six calls and under a minute of API time and the run still blew 600 s on the write.
- `--trust-plugin` skips the first-run trust prompt, which is what CI needs. `--scaffold` is pointless here: `scaffold_script` is accepted by the schema but never executes.
