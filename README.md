# Research Bearings

**Typed skills and contract-bound agents for the part of research that is hard to delegate: deciding what to work on.**

A Claude Code plugin that frames a question worth answering, maps what your field and the fields that never cite yours have already done, turns papers into cards you can build on, generates and ranks ideas, and pre-registers the experiment before you spend compute. Everything it writes lands under `research/` in your project as plain markdown with fixed headings, and every paper it names is checkable against the record.

![Research Bearings](docs/diagrams/banner.svg)

```
  FRAME         GATHER        READ          THINK         EXPERIMENT    RESULT
 ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐
 │Question│ ─▶ │ Matrix │ ─▶ │ Cards  │ ─▶ │ Ranked │ ─▶ │ Design │ ─▶ │Verdict │
 │  gate  │    │Analogs │    │3 agents│    │  gate  │    │  gate  │    │3 rounds│
 └────────┘    └────────┘    └────────┘    └────────┘    └────────┘    └────────┘
  /start        /orient       /read         /think        /design       /result
```

Three human gates: you approve the question, you pick which ideas survive, you decide whether to spend compute. Nothing downstream runs until you say so, and no agent ever runs your code.

---

## Commands

Type `/research-bearings:router`, or ask "what next?", and the front door reads what exists under `research/`, names the one command that comes next with the evidence beside it, and runs it when you say yes. These are the commands it hands you.

| What you're doing | Command | Key principle |
|---|---|---|
| Starting from nothing | `/start` | Setup, then frame. A pause between. |
| Framing a question worth answering | `/frame` | A question names who decides differently |
| Mapping what exists | `/orient` | Surveys first, then a matrix; every line verified |
| Finding fields that solved your problem under another name | `/scout` | Strip your vocabulary, search theirs |
| Reading a paper into a card | `/read` | Predict before you read; a judge that never saw the guess |
| Going from cards to a ranked shortlist | `/think` | Attack every idea before ranking it |
| Writing the one page a professor reads | `/spec` | Heilmeier's eight, every sentence sourced |
| Pre-registering an experiment | `/design` | The stop rule is named while the number is unknown |
| Logging a run | `/log` | Every attempt, before its result is known |
| Reading a result | `/result` | Three rounds, none sees the others' verdict |

Every skill is invoked as `/research-bearings:<name>`.

---

## Quick start

```bash
claude plugin marketplace add ~/Desktop/Research-Skills
claude plugin install research-bearings@rbh227
```

Then, in any project:

```
/research-bearings:router
```

On an empty folder it names `/start`. No API key is required; `/setup` probes every source it can reach and writes which ones answered and which three keys would help most. See [Sources and keys](#sources-and-keys).

---

## All 27 skills

One skill, one job, one file. Each writes into `research/` under fixed headings that a script checks.

### Front door

| Skill | What it does | Use when |
|---|---|---|
| `router` | Reads the state through one script, prints a brief, names the next command with the precondition it checked, asks once, runs it. Offers a fork of two or three when the folder has one. | "What next?" |
| `start` | `/setup` then `/frame`, with the context file's summary and one question between them. | Day one |
| `orient` | `/surveys` then `/landscape`, ending in a printed brief: surveys found, cells filled, cells that returned nothing, the three uncarded papers the matrix ranks highest. | After the question is approved |
| `think` | `/bits`, `/scout`, `/ideas`, `/premortem`, `/rank`. Pauses at every file boundary; a file that exists gets a rerun-keep-stop question carrying its date and what is newer than it. | After the cards are read |

### Questions

| Skill | What it does | Use when |
|---|---|---|
| `setup` | Checks the machine, probes the sources, interviews you for what it cannot check. Writes `CONTEXT.md` and `CONNECTIONS.md`. | Starting or inheriting a project |
| `frame` | Diverges into candidate framings, converges with Booth's ladder and the Heilmeier eight, has a fresh-context critic attack the survivor. Writes `QUESTION.md`. | A question feels vague or unfalsifiable |

### Gathering

| Skill | What it does | Use when |
|---|---|---|
| `surveys` | One searcher restricted to reviews, then a differ that extracts each survey's own taxonomy and harvests vocabulary into the question. | Before the landscape |
| `landscape` | Seven questions from `QUESTION.md`, seven searchers in parallel, a probe per matrix cell, a merger that lays the sections side by side. Writes `matrix.md` and `timeslice.md`. | You want to know what exists in your own field |
| `scout` | Strips your field's nouns off the problem, names the fields that share its shape, sends one searcher per field with your vocabulary blocked. Writes `analogs/<slug>.md`. | You suspect someone solved this under a different name |
| `datasets` | Dataset rows from the cards, looked up on the Hugging Face hub and GitHub: split protocol, licence, who uses it, or `could not determine, checked <hosts>`. | After reading, before any baseline |
| `groups` | The authors on your cards, their last three years, grouped into labs with one checkable sentence each. | You want the competitive landscape |

### Processing

| Skill | What it does | Use when |
|---|---|---|
| `read` | The three-agent read: a predictor that sees only the introduction, a reader that never sees the prediction, a scorer that sees both. Proposes five papers from the matrix and waits. Writes `papers/<slug>.md`. | The matrix has lines nobody has read |
| `verify` | Tags every reference in one file as verified, candidate, or not found with the indexes checked. Never deletes a line. | Anything that names papers |
| `audit` | The eight Kapoor and Narayanan leakage types against one card, each with the passage or what was checked. | Before you build on a number |
| `reviews` | What OpenReview's referees pushed on, onto the card; the pattern across papers once three carry notes. | You want to know what this field's reviewers push on |
| `critique` | A fresh-context critic that quotes the passage behind every finding, then scores your rebuttals on evidence, concedes only at four, never twice in a row. | Any file under `research/` |
| `bits` | One assumption per group of cards that share a thesis. Groups are recorded and reused, so `/ideas` reads a file that does not reshuffle. | Several papers are carded |
| `brainstorm` | The dump: important problems before feasibility, Polya's transformations one at a time, four to six persona agents from your field's own record. Decides nothing. | You want everything out of your head |
| `ideas` | Generates from five seed kinds, puts every candidate to the index and writes the row count it came back with, then plans retrieval from the fields that would make the set less self-similar. Novelty is a retrieval result, never a feeling. | You have bits, analogs, or a log |

### Selection

| Skill | What it does | Use when |
|---|---|---|
| `premortem` | One fresh-context agent per idea, none of which generated it: the baselines it must beat, the field's metric, what the evaluation depends on, a verdict in three states. Judges execution, never novelty. | After `/ideas`, before `/rank` |
| `rank` | A bounded pairwise tournament whose judges see two ideas and never their authors, Alon's feasibility-against-interest grid, and a final order by cheapest kill, with every disagreement named. | After the pre-mortems |
| `spec` | The Heilmeier page for a survivor: eight questions, eight paragraphs, one page, every factual sentence sourced to a file. | An idea survived ranking |

### Experiments

| Skill | What it does | Use when |
|---|---|---|
| `baseline` | The plan to reproduce the strongest published number you intend to beat, with the table it came from and what the paper leaves unstated, then the gap. | Before `/design` |
| `replicate` | The same machinery pointed at a paper you are not building on, so the gap is a fact about your pipeline. | You want to know if your gaps mean anything |
| `design` | The pre-registration: seven fields, Platt's competing hypotheses with the run that separates them, the leakage taxonomy against your split, a stop rule. Never edited after. | Before you spend compute |
| `log` | Every attempt appended to one immutable notebook before its result is known, then the run directory ingested and attached by config hash. | Before and after every run |
| `result` | A tabulator that builds the table from the runs only, a fresh critic that applies the stop rule literally, an auditor that walks the seven failure modes. | After `/log` |

Planned and not built: `render` (the matrix as a clickable page) and `figure` (a pipeline figure).

---

## Agents

An agent exists where a separate context is the mechanism: a judge that must not see how the thing was made, a worker that must see one question and not the others, or a writer whose tools are the contract.

| Agent | The one question it answers | What it never sees |
|---|---|---|
| `question-critic` | What is wrong with this question? | The reasoning that produced it |
| `searcher` | What does the record hold on this question, in this field? | The other six searchers |
| `merger` | Laid side by side, what do the sections say, and where do they disagree? | Anything but the sections; Read and Write only |
| `survey-differ` | How does each survey carve up the field? | Anything past the abstracts, and it says so |
| `predictor` | From the first page alone, what will this paper do and where will it be weak? | The body of the paper |
| `reader` | What does this paper actually do, and what does it change? | The prediction |
| `scorer` | What did a careful first reading get wrong? | Nothing; it is the only one that sees both notes |
| `openreview-reader` | What did the referees push on? | Praise; it quotes reviewers |
| `dataset-scout` | What is actually in the data this field trains on? | Anything not in a host record or a quoted passage |
| `author-tracker` | Who is working on this and where are they heading? | Anything not checkable against the titles beside it |
| `leakage-auditor` | Could this number be higher than the method deserves? | A type it may skip; all eight are written |
| `critic` | What is wrong with this file? | The reasoning behind it |
| `persona-ideator` | What would this person want to know? | A persona with no warrant in the record |
| `diversity-planner` | What is this set of ideas not drawing on? | An idea to propose; it never does |
| `premortem-agent` | How does this idea die in execution? | Novelty; that was settled by retrieval |
| `tournament-judge` | Of these two, which should run first? | Who wrote either |
| `baseline-reproducer` | What would it take to hit this published number? | Your code running; it writes the plan |
| `experiment-designer` | What will be run, and what result would make you stop? | The result |
| `ablation-planner` | If this works, how will anyone know which part worked? | The design's author's reasons |
| `variance-checker` | Does this number have enough seeds to be compared? | A single-seed number in a table; it refuses one |
| `results-tabulator` | What do the run directories actually say? | The hypothesis; it judges nothing |
| `results-critic` | Applying the rule written before the run, did it survive? | What anyone hoped for |
| `failure-mode-auditor` | Is there a file that rules this failure out? | The verdict |

---

## How it works

Four rules, each enforced somewhere you can point at.

1. **The model may think freely; its citations get checked.** Everything named is resolved against the record, exact match only. A near match is a candidate and never certified. What will not resolve stays in the file, marked.
2. **No file says a gap exists.** It reports what a search returned and lets you draw the conclusion. "Unexplored", "gap", "novel" and "nobody" do not appear, and a checker fails the file if they do.
3. **The generator never judges in the same context.** Critics, scorers and mergers run fresh, with narrower tools than the thing they judge.
4. **Retrieved content is data, not instructions.** And abstention beats a guess: "could not determine, checked X and Y" is a valid output.

**Gathering** fans out and merges back through files. Seven searchers, one question each, and a merger that reads the seven files and nothing else.

![How gathering works](docs/diagrams/gathering-fan-out.svg)

**Reading** is three contexts. The predictor commits a guess from the introduction; the reader never sees it; the scorer sees both and writes what a careful first reading would have missed.

![The read trio](docs/diagrams/read-trio.svg)

**The split is a hook, not a prompt.** Research agents can read the world and cannot run code. Experiment agents can read your runs and cannot reach the web. The guard denies a plugin agent any write outside `research/`, any Bash command other than the plugin's own scripts, and any web tool except the searcher's last-resort search.

![The tool split](docs/diagrams/tool-split.svg)

---

## Sources and keys

Nine sources. Four carry retrieval: Semantic Scholar, OpenAlex, Crossref and arXiv. Unpaywall finds the open-access PDF a read needs; the Hugging Face hub and GitHub fill the dataset ledger; OpenReview carries the reviews; Zotero is probed and reserved. Every one works without a key, at the unkeyed rate, and the script says which index answered each call.

Two degrade in a way worth knowing. Without `UNPAYWALL_EMAIL`, a paper whose only open-access copy is not on arXiv comes back `no text` and `/read` skims it from the abstract. OpenReview answers search anonymously but gates the forum behind a bot challenge, so without a login `/reviews` gets the venue and the decision and not the reviews, and says so.

Keys are read from the environment. `S2_API_KEY`, `OPENALEX_MAILTO`, `CROSSREF_MAILTO` and the rest are listed with where to get them and a one-line test for each in [`docs/APIS.md`](docs/APIS.md).

```bash
python3 scripts/retrieval/snowball.py status --md     # every source, live, in a few seconds
```

---

## Running the checks

```bash
# offline, seconds: the scripts, the guard, the structural checks, the grader facts
python3 scripts/retrieval/snowball.py --selftest
python3 scripts/retrieval/papers.py --selftest
python3 scripts/ingest_runs.py --selftest
python3 scripts/state.py --selftest
python3 hooks/guard.py --selftest
python3 scripts/check_headings.py
python3 evals/fixtures/check_cases.py

# 33 behavioural cases, run by Claude Code's eval harness; each is a full Claude child
claude plugin eval . --scaffold --allow-tools "Bash(python3 *)"

# recall of a live landscape run against the gold list
python3 evals/landscape/recall.py evals/landscape/runs/damage --headings "damage assessment"
```

The cases need fixture folders, which each case's scaffold assembles from the outputs of past live runs; [`evals/fixtures/README.md`](evals/fixtures/README.md) says which grants each needs. The gold list is `evals/gold/wildfire-cv.md`; read its provenance note before reading a recall number.

---

## Project structure

| Path | What lives there |
|---|---|
| `skills/` | 27 skills, one `SKILL.md` each: purpose, inputs, agents dispatched, the file written with its headings, a refusals table |
| `agents/` | 23 agents: the one question each answers, its tools, its output headings, what it must not do |
| `scripts/` | `state.py` (the loop as a table), `ingest_runs.py` (run directories nobody formatted for it), six checkers and their shared library |
| `scripts/retrieval/` | `snowball.py` (status, search, verify, neighborhood) and `papers.py` (fetch, reviews, datasets, authors) |
| `hooks/` | The guard: write scope, Bash fence, web fence |
| `templates/` | The 28 file formats; the source of truth for every heading |
| `evals/` | 33 cases, the fixtures and their assembler, the gold list, the landscape and read runs |
| `docs/APIS.md` | Sources, keys, rates, one-line tests |
| `docs/design/` | One note per chunk: what was decided, what the build found, what the live runs corrected |
| `docs/diagrams/` | The banner and the three diagrams above, as SVG and HTML |

The methodology every skill applies traces to a source in a reading sheet kept local and not shipped; `docs/design/skills-and-agents.md` joins each skill to its justification.

---

## License

MIT.
