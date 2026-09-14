# Toolchain

The four verbs skills use instead of hardcoded stack commands. A verb whose value is `none` is skipped, never guessed.

This repo is a Claude Code plugin. There is no compiler and no package manager, but there are real checks: manifest validation, a heading-parity check between templates and the skills that write them, a selftest on the write-scope guard, a selftest on the retrieval script, and a structural check on what /scout writes.

| Verb | Command |
| --- | --- |
| build | `none` |
| static checks | `claude plugin validate ./ --strict && claude plugin validate skills/ --strict && claude plugin validate agents/ --strict && python3 scripts/check_headings.py && python3 scripts/check_analogs.py --selftest` |
| one test file | `python3 hooks/guard.py --selftest && python3 scripts/retrieval/snowball.py --selftest && python3 scripts/check_analogs.py --selftest` |
| full suite | `none` — the behavioural tier went with the snowballing skill on 2026-09-14. `/scout`'s done-check is `scripts/check_analogs.py`, which is a static check, not a judge. `scripts/run_evals.sh` went with it; it is in git at 249188a if a case suite exists again. |

Consumers: `/implement`, `/tdd`, `/codex-review`, `/run-tickets`. Run **static checks** before every commit and **one test file** per red-green slice. There is no full suite to run before a review gate; the static checks are the gate.

Notes:

- **Static checks and one test file are free and fast.** Run them freely.
- **`check_analogs.py` is the whole automated done-check for chunk 3.** There is no judge tier for `/scout`: every rule it has — a checkable id on every paper line, counts that agree, no home-field names, five fields, no absence claims — can be decided by looking, so nothing there needs a model. Point it at a written file (`python3 scripts/check_analogs.py research/analogs/<slug>.md`) or run `--selftest` for its seven fixtures.
- **`validate ./` alone is weaker than it looks.** Pointed at this repo it validates the *marketplace* manifest and stops, because `marketplace.json` is what it finds first. Skill and agent frontmatter is only checked when you point it at `skills/` and `agents/` directly — hence three calls. Pointing it at a single `.md` file does not work: it tries to parse the file as a JSON manifest.
- **`validate .claude-plugin/plugin.json --strict` fails on this repo by design.** It walks components and warns that a root `CLAUDE.md` is not loaded as plugin context. That warning is correct and permanent: this repo is both the plugin and a project, and the `CLAUDE.md` is the project's. Not part of the verb.
