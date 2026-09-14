# research-bearings

A Claude Code plugin for the part of research that is hard to delegate: deciding
what to work on.

Models are good at finding papers in your own field. They are worse at the thing
that actually moves research along — noticing that somebody in an unrelated field
already solved the shape of your problem, under different words, in a literature
that never cites yours.

That is what this is for.

## The idea

Your problem has a **shape** underneath its vocabulary. "Post-disaster building
damage assessment from satellite imagery" is, structurally:

> two captures of one scene at different times, imperfectly aligned; a verdict
> per region rather than per image; labels that are sparse, noisy and ordered by
> severity; and a domain shift between one event and the next.

Written that way, it stops being a remote-sensing problem. Crop stress from
repeat drone flights over a field has that shape. So does lesion change across
two MRI scans, crack progression in bridge inspections, and transient detection
in astronomical surveys — where, it turns out, two groups independently
concluded that the image-alignment step everyone uses should be thrown away,
because its artefacts dominate the error.

None of those would ever appear in a search of your own literature, and no
citation graph reaches them. If anyone had cited across, it would not be the
connection worth finding.

## What it does

Four skills. Each does one job and writes one file.

| | | writes |
|---|---|---|
| `/setup` | Records the project's constraints: lab, compute, data access, deadline, and what would count as a win. | `research/CONTEXT.md` |
| `/frame` | Turns a topic into a question worth answering, then has a critic in a fresh context attack it. | `research/QUESTION.md` |
| `/scout` | Finds the fields that share your problem's shape but not its citation graph, and what might transfer from each. | `research/analogs/<slug>.md` |

Run `/setup` first. `/frame` needs it. `/scout` needs neither — it will run on
whatever you type and say so in the file.

### What a `/scout` run looks like

1. **Shape.** Your problem, with your field's nouns removed.
2. **Fields.** Five to ten that share the shape, each in its own words. Mostly
   adjacent, one or two genuinely strange.
3. **Confirm.** It shows you the shape and every search it is about to run. This
   is where you steer — searching takes seconds, the framing is the work.
4. **Search.** One query per field, never in your vocabulary.
5. **Write.** Per field: what shape it shares, what might transfer, what is
   different, and what you would actually try.
6. **Verify.** Every paper it named is checked against Semantic Scholar.

A few minutes, a few thousand words, and you read it.

## The rule everything else follows from

**The model may think freely. Its citations get checked.**

You want a model's recall here — it is the thing that knows crop damage and
lesion change share a shape. What you cannot have is a model quietly inventing a
citation to go with the insight.

So every paper named in the output is resolved against the record, and anything
that will not resolve stays in the file **marked as unresolved**, next to the
closest real thing the search returned. Nothing is deleted, because where recall
outran the record is exactly what a reader wants to see.

One rule comes with it: the file never says a gap exists. It reports what a
search returned and lets you draw the conclusion. An absence claim becomes an
empty cell in somebody's matrix, and an empty cell is what sends a person to
spend a semester on work that already exists.

## Install

```bash
claude plugin marketplace add ~/Desktop/Research-Skills
claude plugin install research-bearings@rbh227
```

An API key is optional but worth having — a line in
`~/.config/research-bearings/s2-api-key`, or `SEMANTIC_SCHOLAR_API_KEY`. Without
one the API rate-limits after a few calls, coverage drops, and `/scout` stamps
that in the file rather than quietly returning less.

Everything the plugin writes goes under `research/` in your project. Nothing
runs in the background and nothing stays resident: retrieval is one standard-library
script, invoked when it is needed, gone when it exits.

## Status

**Chunk 3 of 6.** The question stage and the breadth tool work. Reading,
ideation, selection and experiments are designed and not built —
[`docs/design/skills-and-agents.md`](docs/design/skills-and-agents.md) has the
whole plan.

Not yet done: a live run judged by a human. The automated checks are structural
only, by design — see [`docs/design/chunk-03-analogs.md`](docs/design/chunk-03-analogs.md) §6.

## Layout

```
skills/                    setup, frame, scout — one job, one file each
agents/question-critic.md  attacks a framed question from a fresh context
scripts/retrieval/         search, batch, verify, health, --selftest
scripts/check_analogs.py   the structural done-check for a /scout file
scripts/check_headings.py  templates and the skills that write them agree
hooks/                     write-scope guard: agents write under research/, nowhere else
templates/research/        the file formats, and the source of truth for them
docs/design/               why each decision went the way it did
evals/                     eval cases, and the gold set for recall
```

## Development

Two verbs, both free and fast, in
[`docs/agents/toolchain.md`](docs/agents/toolchain.md) — manifest validation,
heading parity, and the two selftests. Run them freely.

The methodology every skill applies traces to a source in `academic.md`, the
sheet this plugin is derived from. It is kept local and not shipped.
