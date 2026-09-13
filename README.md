# research-bearings

A Claude Code plugin that runs the research loop with typed skills and
contract-bound agents.

One skill, one job, one output file. Context passes between skills through files
with fixed headings, never through conversation. Every methodology rule the
skills apply traces back to a source in [`academic.md`](academic.md).

**Status: chunk 1 of 6.** The question stage works. The landscape chain,
reading, ideation, selection and experiments are not built yet — see
[`docs/design/skills-and-agents.md`](docs/design/skills-and-agents.md) for the
whole plan and [`docs/design/chunk-01-question-stage.md`](docs/design/chunk-01-question-stage.md)
for what chunk 1 specified.

## Install

```bash
claude plugin marketplace add ~/Desktop/Research-Skills
claude plugin install research-bearings@rbh227
```

Adding the marketplace by raw `marketplace.json` URL will not work — the plugin
source is a relative path, and only the manifest gets downloaded that way.

## What ships today

| Command | Does | Writes |
|---|---|---|
| `/research-bearings:setup` | Records what you have: lab, compute, data, code, your calibration, deadline, what counts as a win. Checks what it can from the machine; asks the rest and dates the answers. | `research/CONTEXT.md` |
| `/research-bearings:frame` | Turns a topic into a question worth answering. Diverges into candidate framings, converges on Booth's ladder, then a fresh-context critic attacks the survivor. | `research/QUESTION.md`, `research/framing-log.md` |

Run `setup` first. `frame` will stop if `CONTEXT.md` is missing.

Everything the plugin writes goes under `research/` in your project. A
`PreToolUse` hook enforces that for the plugin's agents — it is the only
enforcement here that is not prompt text.

## Why `frame` diverges before it converges

A skill that only interrogates the question you brought can sharpen it, but it
can never tell you that you are asking the wrong one. That is usually the most
valuable thing a framing session can produce. So the loop generates candidate
framings first — Polya's transformations, Hamming's important-problems question
— kills them on Booth's ladder and the recursive so-what, and repeats until one
stands.

Before any literature has been read those candidates are guesses, and the skill
says so rather than implying otherwise. The stage is re-entrant: once `/surveys`
exists and shows you what the field actually asks, run `frame` again.

## Development

```bash
python3 hooks/guard.py --selftest              # write-scope guard, 13 cases
claude plugin validate ./ --strict             # manifests
claude plugin eval ./ --trust-plugin --allow-tools Write Edit Agent \
  --tag ci --threshold 0.8                      # behavioural suite
```

### Iterating on the plugin itself

`claude plugin install` takes a **snapshot copy** into
`~/.claude/plugins/cache/rbh227/research-bearings/<version>/`. Editing this repo
does not change the installed copy, and `claude plugin update` is a no-op while
the version string in `plugin.json` is unchanged. To pick up edits:

```bash
claude plugin uninstall research-bearings
claude plugin marketplace update rbh227
claude plugin install research-bearings@rbh227
```

Bumping `version` in `plugin.json` works too, and is the right move for a real
release. `claude plugin eval ./` reads the working tree directly, so evals
always test current files — only interactive smoke runs hit the stale copy.

The eval suite spends tokens (roughly $3 a full pass); the guard selftest and
the validator are free.

`Write`, `Edit` and `Agent` are gated and must be granted explicitly, or cases
fail for reasons that look behavioural. One case, `setup-checks-before-asking`,
is tagged `needs-bash` and cannot run on a machine whose `~/.docker` holds
symlinks — see §9 of the chunk 1 spec.

## Layout

```
.claude-plugin/plugin.json         manifest — no component fields, default layout
.claude-plugin/marketplace.json    this repo is its own marketplace
skills/<name>/SKILL.md             user-invoked, run inline
agents/<name>.md                   contract-bound, dispatched by skills
hooks/hooks.json + guard.py        write-scope enforcement
templates/research/                the output headings, in one place
evals/<case>/                      prompt.md + graders/
academic.md                        the source sheet every rule traces to
docs/design/                       what is being built, and why
.scratch/                          the wayfinder tracker for this effort
```

## Licence

MIT.
