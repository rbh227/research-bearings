# CONTEXT.md

Glossary for the research plugin effort. One meaning per word.

## Terms

- **map**: The wayfinder planning artifact for an effort, under `.scratch/<effort>/map.md`, with one child ticket per decision. Never used for anything the plugin produces.
- **landscape**: The plugin's Milestone 1 deliverable for a research question: the surveys diff, the concept matrix, the time slice, and the brief. The build plan's "map chain" is the sequence of skills that produces a landscape.
- **ticket**: A wayfinder child issue holding one decision or investigation. Not a plugin concept.
- **destination**: What a map is finding its way to. For this effort: Milestones 0 and 1 specified sharply enough to hand to `/to-spec`.
- **research-bearings**: The plugin this effort is building. A Claude Code plugin whose typed skills and contract-bound agents run the research loop; Milestone 1 produces a landscape.
- **acceptance run**: A trial of the built plugin on a real research question, performed by the user after handoff. Not part of any map; it produces the next map's loose idea.

## Retrieval terms

Added with chunk 2 for a snowballing skill, replaced with chunk 3's when that
skill was deleted (2026-09-14). All of these describe one `/research-bearings:scout`
run.

- **shape**: The problem written without the home field's nouns — what it is structurally, in words any field would recognise. The one step nothing else in the plugin does, and the rest of a run is only as good as it.
- **field**: One area that shares the shape and not the vocabulary, searched in its own words. A field whose papers would plausibly cite your seeds is not a field, it is the home field with a wider collar.
- **home vocabulary**: The words `## Vocabulary` in `research/QUESTION.md` lists. Stripped in step 1, banned from field names, and never used as a query — a query in your own words finds your own field.
- **transfer**: Why a field's method might move to your problem, and what is different about it. Grounded in the rows the search returned.
- **opportunity**: What you would actually try, per field. The one speculative thing in the file, and labelled as such.
- **nearest existing**: The opportunity put to the index, with a row count and the closest title. This is the only shape an absence claim may take here; "unexplored", "gap", "novel" and "nobody" do not appear at all.
- **verify**: Resolving every paper the file names against the record — by id, or by title with case, punctuation and spacing folded. **Only an exact match resolves.** A prefix or substring match is reported as a candidate and not certified: measured 2026-09-14, "Attention Is All You Need for Wildfire Damage Assessment" prefix-matched "Attention Is All You Need" and came back resolved, carrying the wrong paper's id.
- **unresolved**: A paper `verify` could not match. It stays in the file, marked, with the closest thing the search did return. Never deleted: where recall outran the record is what a reader wants to see.
- **framed** / **unframed**: Whether the run took its problem from `research/QUESTION.md`. Unframed runs are stamped as such, and are a normal way to use the skill.
- **bound**: Searches times `--limit`, where the searches are the field list the user approves before any of them run. There is no budget and no ledger: a citation walk compounds and needs a ceiling enforced per request, and search does not.

## Connection terms

Added with chunk 4 (2026-09-15), when the retrieval script grew from one index
to four resolvers and seven probes. `docs/APIS.md` is the reference.

- **source**: One external API the scripts can talk to. Nine since chunk 7: Semantic Scholar, OpenAlex, Crossref, arXiv, Unpaywall, Hugging Face, Zotero, GitHub, OpenReview. The first four are resolvers; the rest are read by one verb each or probed only.
- **resolver**: The code in `snowball.py` that turns one source's answers into the unified record. Four exist: `s2`, `openalex`, `crossref`, `arxiv`. The other three sources are probed only.
- **index**: A source `search` queries for papers by keyword. Two: Semantic Scholar and OpenAlex, merged. arXiv is searched only when asked for by name.
- **connected** / **connected-no-key** / **not connected**: The three states `status` reports per source, defined in `docs/APIS.md`. Reachable is a state; throttled is not an outage; keyless is never an error.
- **degraded**: An index that failed inside one `search` call while the other answered. Named in the result, stamped in the file, never silently absorbed.
- **candidate**: What `verify` calls a prefix or substring title match. Reported with the id it nearly matched, and **never certified**: a candidate line stays unresolved until a human promotes it. Replaces the free-text "NOT the same paper" as the marker.
- **CONNECTIONS.md**: `research/CONNECTIONS.md`, written by `/setup` from `status --md`. One dated line per source. Every searching skill reads it first and adapts.
- **web rule**: `WebSearch` and `WebFetch` are allowed in exactly two places, the `searcher` agent's last resort and `/scout` reading a page an index pointed at, and the guard denies both to every other agent this plugin ships.

## Gathering terms

Added with chunk 5 (2026-09-15), the gathering cycle: `/surveys`, `/landscape`, and `/scout` rewired onto one agent.

- **neighborhood**: The script verb, and what it returns: the seeds for one query plus one hop backward and one forward from each, deduplicated and ranked inside itself. The depth tool, recovered from 249188a and rebuilt on two indexes.
- **seed**: One of the top 30 papers by relevance for a query, interleaved across Semantic Scholar and OpenAlex. Every seed is walked both ways before the next seed.
- **centrality**: How many neighborhood papers cite a paper, counted over the edges the walk actually saw. The primary rank; `influentialCitationCount`, citations per year and presence in both indexes break ties, in that order.
- **foundational** / **current** / **surveys**: The three groups every section carries. Older than five years; the last five years; title says survey, review or overview or the paper cites 100+ neighborhood papers.
- **section**: One searcher's file: `## Question`, the three groups, `## What was searched`, `## What returned nothing`. Under `research/landscape/sections/` or `research/analogs/sections/`. The only thing the merger reads.
- **searcher**: The one retrieval agent. One question, one field, one query, one section. Runs `neighborhood`; pastes lines; may WebSearch once, as a last resort, labelled. Replaces the deleted `paper-scout`.
- **merger**: The contract-bound agent that lays sections side by side into `matrix.md` and `timeslice.md`. Copies lines, names the query behind every empty cell, marks disagreements as contradictions, cannot add a claim.
- **cell probe**: One `search` per formulation × data regime pair, run by `/landscape` after the sections return and written as `sections/cells.md`, so the merger can name the query behind an empty cell without running one.
- **blocked**: The vocabulary a searcher's query may not use. In `/scout` it is the home vocabulary; the script refuses the query, so the home field cannot leak in by accident.
- **stop reason**: Why a walk ended: `complete`, `saturation` (a block of five seeds added under 5 percent), or `budget` (400 papers). Always recorded in `## What was searched`.

## Reading terms

Added with chunk 7 (2026-09-16), the reading milestone: `/read` and the seven
ledger and judgement skills built on the cards it writes — `/verify`,
`/reviews`, `/datasets`, `/groups`, `/audit`, `/bits`, `/critique`.

- **card**: One paper, understood, at `research/papers/<slug>.md`. Sixteen fixed headings. Written by the `scorer` at the end of a `/read` run and edited afterwards only by the skill that owns a section. The unit every skill after this one reads.
- **pass**: Which of Keshav's three passes the read stopped at, recorded on every card. `full` is the three-agent protocol; `1` is a skim. A skim that does not say it is a skim is a full read to everything downstream, which is why `check_cards` requires the value.
- **intro text** / **full text**: The two files `fetch` writes per paper, in the cache. The intro text ends where the introduction ends. The predictor is handed the intro text and nothing else, so the rule that it must not see the method is a file boundary and not a sentence in a prompt.
- **split**: How `fetch` decided where the introduction ends: `heading` (the first section heading after it, named) or `page-cut` (the fallback, two pages). Recorded on the metadata record, because a page cut is the case where the predictor may have seen a little of the method.
- **unplaced**: A card written with no matrix to place it in, or whose paper appears in no cell. Marked, never guessed: a card that invents its own cell disagrees with the landscape later. `/read --place` fills it once a matrix exists.
- **tag**: What `/verify` appends to a reference line: `verified`, the candidate marker, or `not found` with the indexes checked. A reference with no tag is a `check_cards` failure. A not-found reference stays in the file, marked, exactly as an unresolved paper does in a section.
- **review notes**: The `## Reviews` section of a card, from OpenReview: ratings, the objections that recur, what the authors conceded, the decision. Reviewers say what authors will not.
- **leakage flag**: One line under `## Leakage`, one per Kapoor and Narayanan leakage type, each carrying a quoted passage or "could not determine, checked X and Y". Flags and evidence; no score and no verdict.
- **thesis group**: A set of cards that share a thesis, named by `/bits` on its first run and recorded in `BITS.md` with its slugs. Ré groups by thesis, not by topic, and the landscape has no such grouping to inherit: sections are per question and cells are formulation by data regime. Recorded rather than recomputed, so the file `/ideas` reads does not reshuffle between runs.
- **bit**: The assumption one thesis group shares, in one sentence, with the cards behind it and the cells they sit in. Method, evaluation or dataset. A group of one card is too thin to carry one, and is listed as such.
- **critique**: One fresh-context attack on one file, at `research/critiques/<file>-<date>.md`. Findings, then rebuttals scored one to five on the concession ladder. Never edits the file it judges.

## Ideation terms

Added with chunk 8 (2026-09-16), the ideation milestone: `/brainstorm` and
`/ideas`, and the two agents they dispatch.

- **seed (of an idea)**: The thing an idea came from, named by file and line, under an idea page's `## Seed`. **Distinct from the retrieval seed above**, which is one of the top papers a walk starts from; the two senses never share a line, which is why the retrieval count on an idea page is written `Papers the query found` and not as a seed count. A candidate that cannot name a seed was generated from what the model already knew — the measured failure this whole stage is built against.
- **seed kind**: `bit`, `analog`, `contradiction`, `abandoned`, `persona`, or `conversation`. The six forms a seed line may take in `IDEAS.md`. A run that has only one of them is allowed, stamped, and is what the stop rule catches.
- **candidate**: One generated idea before it has a page. Every candidate is put to the index and carries the query, how many papers the query found, and the row count that came back. Not to be confused with the retrieval sense of **candidate**, which is a title match `verify` refused to certify.
- **increment**: A candidate whose nearest existing paper is plainly the same idea. Marked, kept, and logged under `## Dropped` with the title and the counts — never deleted, because what was considered and set aside is what stops it being reconsidered from scratch next month.
- **promoted**: A candidate that got a page at `research/ideas/<slug>.md`. `check_ideas.py` fails a log whose `## Promoted` names a slug with no page: the log and the pages may not disagree.
- **abandoned direction**: A direction the record shows was dropped — a time-slice thread with no line in the current period, or a foundational line whose forward hop returned nothing recent. Read from the files and named with the line it came from; never inferred from a feeling about what the field stopped caring about.
- **persona**: One stakeholder's perspective on the question, written by `persona-ideator` at `research/ideas/personas/<date>-<slug>.md`. Questions, not proposals, except under the last heading.
- **cited by path**: How an idea names its seed, and the reason nothing under `research/ideas/` is ever overwritten. Sections, persona files and plans are dated and deduplicated by suffix, because the retrieval script writes a section with `open(path, "w")` and a second run on the same field would replace the evidence an already-promoted idea rests on. The log is append-only; the files it points at have to be too.
- **warrant**: The file and line a persona was drawn from — a lab in the groups ledger, a venue on the cards, a dataset producer, the decision-maker in `QUESTION.md`, an adjacent field on an analog page. A persona's whole identity. Without one it is marked `from the role, not the record`, which is honest; an invented affiliation is not.
- **round**: One generate-and-index pass in `/ideas`. Two by default: round one from the seeds, round two from the sections the diversity fields returned. A third happens only if the user asks.
- **spread**: The countable form of the diversity rule — candidates per seed kind, and per field of origin — written in `## Status` every run. `/ideas` may not stop while every candidate shares one seed kind, or while every nearest-existing came back from a home-vocabulary query **with no field search behind any of them**. The second condition carries that clause because without it it is vacuous: step 3 puts every candidate to the index in the home vocabulary by design, so the unqualified form could never be false and the run could never stop. Nothing computes similarity, typicality or a diversity score; the decision that struck `similarity.py` stands.
- **typicality note**: One written sentence on an idea page: the conventional core and the atypical injection. A note by design, and the same decision as above.
- **IDEAS.md**: `research/IDEAS.md`, the running idea log, appended by `/brainstorm` and `/ideas` and rewritten by neither. Four headings. An idea that dies with its session was a conversation, not an idea.

## Selection and experiment terms

Added with chunk 9 (2026-09-18), the selection and experiments milestone: eight
skills and nine agents, from a pile of idea pages to a result something other
than its author has judged.

- **pre-mortem**: The post-mortem written before the three months are spent, at `research/premortems/<slug>-<date>.md`, by an agent that did not generate the idea. It judges **execution only** — novelty was settled at `/ideas` by retrieval, and interest belongs to `/rank`. Its own file, never a section of the idea page, because a judge does not rewrite what it judges.
- **the three verdicts**: `executable`, `executable with changes`, `not executable as written`. A pre-mortem's first verdict line, read mechanically by `/rank` and `/design`. `executable with changes` is defined by **nameability**: if the changes cannot be named, the state is `not executable as written`, and without that rule the middle state is where every uncertain idea lands.
- **constraint unknown**: What a pre-mortem or an experiment page writes where `CONTEXT.md` does not state the compute, the time or the access it is judging against, followed by what was assumed. Never a silent assumption of a cluster. An idea judged feasible against imagined compute has passed a check that did not happen.
- **pairing**: One comparison of exactly two ideas by a `tournament-judge` that sees both pages and both pre-mortems and **nothing about who wrote either or which seed produced it**. A model asked to score one idea returns four; asked to pick between two, it has to find a difference and name it.
- **the bound**: How many pairings a ranking will cost, shown and approved before the first judge runs. Round robin at five ideas or fewer; three pairings each above that; twelve total, hard. Twelve ideas compared every way is sixty-six judge calls.
- **cheapest kill**: The ordering rule in `RANKING.md` — run the experiment most likely to end the project first, because the next month buys information and the cheapest information comes first. Written from each idea page's `## Cheapest kill` cost line. **Not** the tournament order, which measures interest; both are written and every disagreement between them is named.
- **the hard-but-feasible region**: The marked quadrant of Alon's five-by-five grid, feasibility against interest, drawn from the judges' one-to-five scores. The quadrant students avoid. Nothing computes those scores: each is a written judgement with its evidence line beside it, the same decision that struck `similarity.py`.
- **set aside**: An idea whose pre-mortem said `not executable as written`. Listed with its blocker, not ranked and not deleted — a broken idea scored on interest outranks a working one, and then somebody runs it.
- **Heilmeier page**: `research/specs/<slug>.md`, the eight questions in eight paragraphs, one page. Every factual sentence names the file it came from; a sentence nothing supports is written in place as `not established in the cards I read` and listed under `## Sources` as `unsourced:` — such a sentence may exist, it may not be invisible. This is the page Milestone 2 deferred as `/brief`.
- **the one-page test**: The catechism's own rule, applied and reported. Over about 800 words `/spec` writes that the page is still a brainstorm. It is never trimmed to pass: a page cut to fit and a page that fit are different findings.
- **reproduction status**: `not attempted`, `attempted, gap recorded`, `contested`. The three states of a baseline file. **`contested` requires the attempt list** — each attempt, the conditions varied, the number reached — because it says a published number did not reproduce, and without the attempts it is a complaint about somebody's work.
- **calibration**: A `/replicate` run: the same machinery pointed at a paper the researcher is **not** building on, so the gap it reports is a fact about their pipeline rather than about the paper. Chosen before the answer is known, and the file carries the sentence that says so, because a calibration file read later without it looks like a failed baseline.
- **pre-registration**: The seven fields on `research/experiments/<slug>.md` — hypothesis, baseline and why, metric and why, seeds and variance plan, leakage check, compute budget and search size, stop rule — written before the run and **never edited after it**. A changed design is a new page with a new slug and the old one stays.
- **stop rule**: `- Abandon if: <result>`, in that shape, naming a quantity and a threshold. `results-critic` applies it literally and is given nothing else to interpret. A stop rule written after the number exists is a rationalisation with a heading.
- **competing hypotheses**: Platt's two or three explanations that could each produce the expected outcome, and the one run whose result differs between them. H2 is almost always "the gain comes from somewhere you did not intend". A section may say that **no run discriminates** — that is a real finding; it may not contain an invented one.
- **notebook entry**: One attempt in `research/NOTEBOOK.md`, opened **before the run** with the date, the experiment page, the config hash and the seeds. The result is appended as a second block beneath it; the opening block is never rewritten, so a planned seed count that disagrees with the actual one stays visible as a disagreement.
- **append-only**: The notebook's contract, and the only permitted operation on it is inserting lines. An attempt that failed, was misconfigured, or was embarrassing stays exactly where it landed. One notebook, not one per experiment: post-hoc selection is impossible only if every attempt lands in the same place.
- **config hash**: The sha256 of a config file's bytes as `ingest_runs.py` computed them. Provenance: which exact file a run was started from. It includes the seed, so five seeds are five config hashes, which is why it groups nothing.
- **condition hash**: The sha256 of the canonical parsed config with every seed key removed, also from `ingest_runs.py`. Runs that share one differ only in seed and are one condition — the key `variance-checker` and `results-tabulator` group on, and the key by which a later ingest finds the notebook entry that was opened before the run. A config that would not parse has none, and such a run belongs to no condition. Added after the adversarial review (2026-09-18): with the raw hash alone, every multi-seed experiment was five single-seed conditions.
- **refused: single seed**: What `variance-checker` returns for a metric with one seed behind it, written **into the notebook entry** rather than omitted from a table. A one-seed number that quietly never appears looks identical to a number nobody produced. `short of plan` — fewer seeds than planned, more than one — is not a refusal: the count travels with the number.
- **not sourced**: The heading on a result page holding every number that was wanted and could not be traced to a run directory, with what was looked for. It is why the table can be trusted: a missing number is neither quietly dropped nor quietly filled in.
- **the three rounds**: `/result`'s structure. The tabulator builds the table and judges nothing; the critic gets the pre-registration and the table and **not** the tabulator's commentary; the auditor walks M1–M7 and is **not told the verdict**, because an auditor that knows the result was a win looks for reasons it is fine.
- **survived / killed / inconclusive**: The critic's three states. **`inconclusive` must be argued**: it names which clause could not be applied and what specific obtainable evidence would decide it. "More seeds" is not an argument. An `inconclusive` with neither is the critic declining to answer.
- **M1–M7**: Lu et al.'s seven failure modes — implementation bugs that pass self-review, hallucinated citations, hallucinated results, shortcut reliance, a bug reframed as an insight, methodology fabrication, frame-lock. All seven are answered every run including the clean ones, each with a file path or `unchecked:` and what was looked at. **No score**: one number cannot carry seven kinds of doubt.
- **run-shaped**: What `ingest_runs.py` calls a directory holding a config, a metrics file or a log. There is no layout to adopt; it reads run directories nobody formatted for it. A `.json` is classified by name, and one whose name says neither config nor metrics is reported as unclassified rather than guessed at.
- **no agent runs your code**: The chunk's largest departure from the build plan, and the guard's doing. `SCRIPT_ROOT` admits this plugin's own `scripts/` and nothing else, so "whether to spend compute" is a fact about the code rather than a sentence in a skill.

## Front-door terms

Added with chunk 10 (2026-09-18), the last milestone: `/router` and the three
composites.

- **router**: `/research-bearings:router`, the front door. Reads the state script, prints the brief, names the next command with the precondition it checked, asks once, invokes on yes. Never a signpost that only points and never a chauffeur that runs unasked. Reachable by description on "what next?" as well as by name.
- **composite**: A skill that runs a fixed sequence of other skills in the main thread through the Skill tool — `/start`, `/orient`, `/think` — adding nothing to any of them and writing nothing itself. Not an agent: a composite judges nothing, so it needs no fresh context.
- **file boundary**: The point in a composite between one step's output file and the next step. Every boundary asks once; the first step needs no yes because typing the composite was it. A skill's own gates (landscape's seven queries, rank's pairing list) are not boundaries and the composite does not touch them.
- **staleness fact**: What the state script reports for a derived file that exists: the count of upstream files newer than it by date, the newest upstream date, and `not_named` — the upstream pages the file never mentions. Both are carried in the rerun-keep-stop question and never decided on by the composite; they can disagree, and on first contact they did (a bits file two cards "stale" by date that named all three). Zero is a fact too.
- **rerun, keep, or stop**: The question a composite asks at a boundary whose output already exists. Keep is not skip — a kept file is read by the next step as it stands — and nothing cascades: a rerun of an earlier step does not rerun later ones.
- **brief**: The one screen the router prints and every composite ends with: stage reached, what exists with dates, what is stale, repairs, next moves. Derived from the state script and the files; never saved, because a saved brief is a heading to keep true.
- **state script**: `scripts/state.py`. A dependency table in the loop's order and a read of a `research/` folder against it. Six move statuses: `ready`, `stale`, `repeat` (an output that grows, such as cards), `done`, `blocked`, `skipped` (a required upstream file absent while a later step has output — a repair, not a move). `present-but-malformed` is a state a file can be in and still satisfy a precondition; the file is listed under repairs with the skill that writes it.
- **on-demand skill**: verify, audit, critique, reviews, replicate, and the two ledgers, datasets and groups. Rows in the state table flagged so the router finds them by stated goal and never names one as the next move. A ledger is asked for; it is never the next step.
- **synthetic fixture**: `evals/fixtures/selection/`, six idea pages and six pre-mortems invented so `/rank`'s bound can be graded. The one fixture that is not a copy of a live run; every file in it says so in its first comment. Not research, and never copied into a real `research/`.
