# research-bearings

A Claude Code plugin that runs the research loop with typed skills and
contract-bound agents.

One skill, one job, one output file. Context passes between skills through files
with fixed headings, never through conversation. Every methodology rule the
skills apply traces back to a source in `academic.md`, the sheet this plugin is
derived from — kept local, not shipped.

**Status: chunk 2 of 6, unverified.** The question stage works. Retrieval is
built — three bundled MCP servers and one scout that snowballs a citation graph
into a landscape section — and its plumbing is checked against the live API, but
**its behavioural eval suite has not been run yet**, so treat `/scout` as working
rather than proven. The rest of the landscape chain — surveys, the seven-way
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

Three MCP servers ship with the plugin and register as
`plugin:research-bearings:*`:

| Server | What it is | Used by |
|---|---|---|
| `paper-search` | [`paper-search-mcp`](https://pypi.org/project/paper-search-mcp/) — arXiv, Semantic Scholar, OpenAlex, Crossref and more | seed search |
| `s2-snowball` | ours, `servers/s2_snowball.py` — references, citations, batch metadata over the Semantic Scholar Graph API | every hop |
| `openreview` | `openreview-mcp` — bundled, dormant until `/reviews` | nothing yet |

Neither of the off-the-shelf servers exposes a references or citations tool,
which is why the plugin owns one. `s2-snowball` is a single PEP 723 file run by
`uv run --script`; it needs no install step and carries an offline selftest over
real captured API responses.

It keeps two caches, deliberately different things:

- **`~/.claude/plugins/data/research-bearings-rbh227/s2-cache/`** — raw API
  responses, shared across projects, disposable. Expiry is direction-aware: a
  paper's reference list never changes, so it never expires; its citation list
  grows, so it expires in 30 days.
- **`<project>/research/.papers/`** — one JSON record per paper the crawl
  touched, including the ones the scout rejected. Greppable, gitignored, and
  written by the server rather than routed through the model's context. The
  rejected papers are the point: the paper nearest a future idea is
  disproportionately likely to be one a scout threw away.

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
snowball server offline against real captured API responses (12 cases),
template/contract heading parity, and the plugin, skill and agent manifests.

The behavioural suite is the `full suite` verb in
[`docs/agents/toolchain.md`](docs/agents/toolchain.md) — run it from there rather
than from a copy here, which is how the two drift apart. That file also explains
why each flag is present.

`Write`, `Edit`, `Agent` and every `mcp__*` tool are gated and must be granted
explicitly, or cases fail for reasons that look behavioural. `--mocks off` is
what actually starts the retrieval servers; the default does not start a plugin
server that has no mock.

Two cases are out of the `ci` tag because this machine cannot run them honestly:
`setup-checks-before-asking` needs a `Bash` grant (chunk 1 spec §9), and
`scout-stamps-no-key` needs a machine with no Semantic Scholar key configured
(chunk 2 spec §9.6).

**Working inside this repo shows three `Pending approval` MCP entries.** The
plugin's own `.mcp.json` sits at the repo root, so a session opened here reads it
as a *project* config as well. Do not approve them — project scope does not
expand `${CLAUDE_PLUGIN_ROOT}` or `${user_config.*}`, so they would either fail to
start or shadow the bundled copies. They only appear here, and only because
`source: "./"` makes the plugin root and the project root the same directory.

## Layout

```
.claude-plugin/plugin.json         manifest — no component fields, default layout
.claude-plugin/marketplace.json    this repo is its own marketplace
skills/<name>/SKILL.md             user-invoked, run inline
agents/<name>.md                   contract-bound, dispatched by skills
.mcp.json                          three bundled MCP servers, auto-discovered
servers/s2_snowball.py             the citation walker, PEP 723, --selftest
servers/fixtures/                  real captured API responses the selftest runs on
hooks/hooks.json + guard.py        write-scope enforcement
scripts/check_headings.py          template / contract parity
templates/research/                the output headings, in one place
evals/<case>/                      prompt.md + graders/
docs/agents/                       tracker, domain, triage and toolchain conventions
docs/design/                       what is being built, and why
.scratch/                          the wayfinder tracker for this effort
```

## Licence

MIT.
