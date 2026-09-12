# Toolchain

The four verbs skills use instead of hardcoded stack commands. A verb whose value is `none` is skipped, never guessed.

This is a docs/skills-only repo with no build tooling, so every verb is `none`. Update this table if a build step, linter, or test runner is added later.

| Verb | Command |
| --- | --- |
| build | `none` |
| static checks | `none` |
| one test file | `none` |
| full suite | `none` |

Consumers: `/implement`, `/tdd`, `/codex-review`, `/run-tickets`. Run **static checks** before every commit, **one test file** per red-green slice, and **full suite** once before a review gate.
