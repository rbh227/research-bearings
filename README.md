# research-bearings

A Claude Code plugin that runs the research loop with typed skills and
contract-bound agents.

One skill, one job, one output file. Context passes between skills through files
with fixed headings, never through conversation. Every methodology rule the
skills apply traces back to a source in `academic.md`, the sheet this plugin is
derived from — kept local, not shipped.

**Status: chunk 2 of 6, being verified.** The question stage works. Retrieval
is built — one standard-library script that snowballs a citation graph into a
landscape section — and checked against the live API. Its behavioural eval suite
first ran on 2026-09-13, found the budget was not being enforced, and is being
re-cut around the script (chunk 2 spec §11); treat `/scout` as working rather
than proven until that lands. The rest of the landscape chain — surveys, the seven-way
fan-out, the merger, the matrix and the brief — plus reading, ideation,
selection and experiments are not built yet. See
[`docs/design/skills-and-agents.md`](docs/design/skills-and-agents.md) for the
whole plan, and the chunk specs for what each one decided:
[chunk 1](docs/design/chunk-01-question-stage.md),
[chunk 2](docs/design/chunk-02-scout.md).

## Install

```bash
claude plugin marketplace add ~/Desktop/Research-Skills
claude plugin install research-bearings@rbh227
```

Adding the marketplace by raw `marketplace.json` URL will not work — the plugin
source is a relative path, and only the manifest gets downloaded that way.

The plugin asks for a **Semantic Scholar API key** at enable time
([get one here](https://www.semanticscholar.org/product/api)). It is stored in
your keychain, not in this repo. It is not required — but the unauthenticated
pool 429s after two or three calls, so without it the snowball hops rate-limit
heavily and `/scout` stamps the reduced coverage at the top of every section it
writes. To set it non-interactively:

```bash
claude plugin install research-bearings@rbh227 --config semantic_scholar_api_key=YOUR_KEY
```

`--config` is ignored if the plugin is already installed; uninstall first.

## What ships today

| Command | Does | Writes |
|---|---|---|
| `/research-bearings:setup` | Records what you have: lab, compute, data, code, your calibration, deadline, what counts as a win. Checks what it can from the machine; asks the rest and dates the answers. | `research/CONTEXT.md` |
| `/research-bearings:frame` | Turns a topic into a question worth answering. Diverges into candidate framings, converges on Booth's ladder, then a fresh-context critic attacks the survivor. | `research/QUESTION.md`, `research/framing-log.md` |
| `/research-bearings:scout` | Answers one literature question: finds seed papers, walks their references and citations, and writes 25–35 paper cards with the search log behind them. | `research/landscape/<slug>.md` |

Run `setup` first. `frame` will stop if `CONTEXT.md` is missing. `scout` does
not require either — it runs unanchored and says so in the file.

Everything the plugin writes goes under `research/` in your project. A
`PreToolUse` hook enforces that for the plugin's agents — it is the only
enforcement here that is not prompt text.

## How retrieval works

One script, standard library only, run on demand and gone when it exits:

    python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" search|references|citations|batch|health ...

It talks to the Semantic Scholar Graph API, the one source here that answers
"what does this paper cite" and "who cites this paper" — the two questions the
method (Wohlin, Ré) is built on. Keyword search finds papers that use your words;
following citations finds what the field is built on. Each call prints one JSON
object. Nothing stays resident, nothing needs installing, and the scout agent's
Bash is fenced by the guard to this one script and nothing else.

Chunk 2 first shipped this as three MCP servers, two of them third-party. That was
the wrong packaging — a persistent process, an 80-package dependency tree, a 30 s
cold start, credentials in a file the eval sandbox could not see — and it was
replaced the day the suite first ran. The chunk 2 spec §11 records why.

**The key.** `SEMANTIC_SCHOLAR_API_KEY` in the environment, or one line in
`~/.config/research-bearings/s2-api-key`. Optional, but effectively required for
a crawl: unauthenticated calls 429 after a few requests. Without it the scout runs
degraded and stamps the section.

**The budget.** Every call takes `--run <slug> --budget <N>`. The script keeps a
ledger at `research/.crawl/<slug>.touched.json` of the distinct papers it has
handed out, refuses a hop once the ceiling is reached — before spending the
request — and sizes each hop to what remains. The ceiling used to be a sentence in
the agent's prompt; told 40, it touched 114–160.

Two on-disk artifacts:

- **`~/.cache/research-bearings/s2/`** — raw API responses, shared across
  projects, disposable. Expiry is direction-aware: a paper's reference list never
  changes, so it never expires; its citation list grows, so it expires after 30
  days.
- **`research/.papers/<paperId>.json`** — one record per paper touched, in your
  project. Written by the script rather than the scout: several hundred records
  through a model's context costs tokens and invites transcription errors. Both
  `research/.papers/` and `research/.crawl/` are regenerable; `/setup` adds them
  to your `.gitignore`.

## What a scout will not do

It has read no papers, and the contract is built around that. Every line on a
card is metadata from a tool call or a sentence some other paper wrote — the
`contextsWithIntent` field, which returns the sentences in which a citing paper
describes the cited work, tagged `background` / `methodology` / `result`. That
survives the ~50% missing-abstract rate on backward hops, and it is the citing
author's own characterization rather than an agent's guess.

The only scout-authored prose on a card is one `Kept because` line.

It also will not tell you a gap exists. A scout may state facts about its own
search — this query returned zero rows, this hop surfaced nothing matching this
term — and every section ends with the queries and counts behind it. It may not
write "no published work combines X and Y." An absence claim becomes an empty
cell in a matrix, and an empty cell is what sends someone to spend a semester on
work that already exists. Interpreted absence becomes legitimate at the merger,
which can see seven scouts' coverage at once.

When a section stops on `budget` rather than `saturation`, it says so, in those
words, at the top of the file. The failure worth designing against is not
stopping early — it is stopping early and looking finished.

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

The `static checks` and `one test file` verbs in
[`docs/agents/toolchain.md`](docs/agents/toolchain.md) are free and fast — run
them freely. Between them they cover the write-scope guard (13 cases), the
retrieval script offline against real captured API responses (16 cases),
template/contract heading parity, and the plugin, skill and agent manifests.

The behavioural suite is the `full suite` verb in
[`docs/agents/toolchain.md`](docs/agents/toolchain.md) — run it from there rather
than from a copy here, which is how the two drift apart. That file also explains
why each flag is present.

`Write`, `Edit`, `Agent` and `Bash` are gated and must be granted explicitly,
or cases fail for reasons that look behavioural. This machine cannot grant `Bash`
inside the harness (chunk 1 spec §9), which is why the scout's agent cases hand it
a saved crawl and judge only what it writes; the crawl itself is covered by the
script's offline selftest, and finding things by the gold set. `setup-checks-before-asking`
stays out of the `ci` tag for the same reason.

## Layout

```
.claude-plugin/plugin.json         manifest — no component fields, default layout
.claude-plugin/marketplace.json    this repo is its own marketplace
skills/<name>/SKILL.md             user-invoked, run inline
agents/<name>.md                   contract-bound, dispatched by skills
scripts/retrieval/snowball.py      the citation walker: search, hops, budget ledger, --selftest
scripts/retrieval/fixtures/        real captured API responses the selftest runs on
hooks/hooks.json + guard.py        write-scope and Bash-scope enforcement
scripts/check_headings.py          template / contract parity
templates/research/                the output headings, in one place
evals/<case>/                      prompt.md + graders/
docs/agents/                       tracker, domain, triage and toolchain conventions
docs/design/                       what is being built, and why
.scratch/                          the wayfinder tracker for this effort
```

## Licence

MIT.
