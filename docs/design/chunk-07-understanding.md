# Chunk 7: understanding and the ledgers

2026-09-16. The plugin learns to read. Eight skills and eight agents turn
landscape lines into paper cards and the five ledgers built on them, and the
rule that the predictor must not see the method stops being a sentence in a
prompt and becomes what is in a file. `docs/design/chunk-05-gathering.md`
produced the lines this chunk consumes; `chunk-04-connections.md` is the
source layer under both.

The spec is `.scratch/chunk-07-understanding/spec.md`, with thirteen tickets
in `issues/`. Build only: no `evals/` cases and no live wildfire test. The
milestone's own test — `/read` on DA-SegFormer and two competitors, `/bits` on
the wildfire matrix — is the acceptance run, and it belongs to the user.

## 1. Decision record

- **The fence is a file boundary, not an instruction.** The whole three-agent
  protocol rests on the predictor not having seen the method, and an agent
  handed a PDF and told "stop at page 2" is an agent that will sometimes not
  stop. So `fetch` writes two files. `intro.txt` ends where the introduction
  ends and the predictor is given that path and no other. Page counts were
  never a candidate: "abstract and intro" is a section boundary, and on some
  papers the introduction ends mid-page 2 and on others it runs to page 4.
- **Where the intro ends is measured, not guessed.** Three findings changed
  the splitter, each from a real paper. `pdftotext -layout` puts both columns
  of a two-column paper on one line, so a heading never ends its line and
  every such paper silently page-cut; reading order fixes it, at the cost of
  tables. IEEE renders small caps as `II. R ELATED W ORK`, which no heading
  regex matches until a capital-space-capitals rule is applied per line. And
  the window a heading may sit in is 40 per cent of the extracted text, not a
  quarter: a real paper's Related Work lands near 28 per cent, because the
  references and the running headers extract too. A 30,000-character ceiling
  is the other half of that rule.
- **A page cut never hands over the whole document.** The fallback was
  `min(9000, len(text))`, which returns everything for anything shorter than
  nine thousand characters — the one outcome the protocol cannot survive. It
  is half the text now, and the metadata record says which split happened, so
  the scorer knows when the predictor may have seen a little of the method.
- **Five papers a run, two agent rounds, one gate.** The build plan said
  twenty papers at once, which is sixty agent runs. The predictor and the
  reader are independent by design, so they go in one message and the scorer
  follows; five papers is what fits a session. `/read` proposes from the
  matrix, shows what is left, and waits.
- **A skim is a first-class outcome and must announce itself.** Keshav: most
  papers deserve pass one. `--skim` is one agent from the intro file, and the
  card carries `pass 1`. `check_cards` requires the value, because a skim that
  does not say it is a skim is a full read to everything downstream.
- **One fact, one place.** The first card written said `pass full` under
  `## Identity` and `Pass stopped at: 1` under `## Prediction score`, both
  looking authoritative. The card template no longer repeats the pass, and the
  scorer is told the dispatcher owns that value. The same rule is why a
  section a later skill owns says `_not run_` rather than standing empty:
  empty and unrun look identical, and the difference is "nobody looked" versus
  "OpenReview had no record".
- **An unplaced card beats an invented cell.** A reader that infers its own
  matrix position produces a card that disagrees with the landscape later and
  nobody can tell which is wrong. `/read` works with no matrix, marks the card
  `_unplaced_`, and `--place` fills it afterwards **by id**, because lines
  carry ids and titles drift. What `--place` cannot do is fill the same-cell
  comparison: placing is a lookup and comparing needs the paper open.
- **`/bits` forms the thesis groups and records them.** The grilling settled
  "the landscape's thesis groups"; the landscape has none. Its sections are
  one per question, its matrix is formulation by data regime, and the merger
  records contradictions, not theses. So `/bits` groups the cards itself, on
  its first run, and writes the grouping into `BITS.md`. Later runs read the
  recorded groups, assign new cards, and start a group only for a card that
  fits none. A group is never dissolved by a run. `/ideas` will read this
  file, and a file that reshuffles its groups every run cannot be built on.
- **GitHub over REST, never `gh`.** The guard admits only this plugin's
  retrieval scripts in Bash. Widening that fence so one agent can shell out is
  a worse trade than one more HTTP call, and the guard's selftest now carries
  the case that proves it: `dataset-scout` may run `papers.py` and may not run
  `gh`.
- **The auditor is on request, one card at a time.** Putting `leakage-auditor`
  inside `/read` would add a fourth agent to every paper for a check that
  matters on the handful you plan to stand a number next to. `/audit <slug>`,
  and eight taxonomy types written every time, including the clean ones,
  because a reader needs to know spatial leakage was checked rather than infer
  it from silence.
- **Two sources degrade in ways worth naming.** Measured 2026-09-16: OpenReview
  answers `/notes/search` anonymously and gates `/notes?forum=` behind a bot
  challenge, on both API versions. So without a login `/reviews` gets the
  submission, its venue and its decision, and reports `login required` for the
  reviews — and the card records that rather than leaving the section unrun.
  And without `UNPAYWALL_EMAIL`, a paper whose only open copy is neither on
  arXiv nor named by an index comes back `no text`, and `/read` skims it from
  the abstract. Both are chunk 4's rule again: a missing key is a state.
- **Neither new key is ever suggested.** `GITHUB_TOKEN` and the OpenReview
  login are probed and excluded from `suggest`. The three keys worth asking
  for are still chunk 4's, and a suggestion list that grows every chunk stops
  being read.

## 2. What ships

| Piece | Change |
|---|---|
| `scripts/retrieval/papers.py` | new, importing the walker's transport rather than copying it. `fetch` (resolve, locate, download, extract, split, cache), `reviews`, `datasets`, `authors`; 27 offline cases and five fixtures |
| `scripts/retrieval/snowball.py` | GitHub and OpenReview probes; `suggest` skips a source flagged `suggest: False`; 45 cases |
| `agents/predictor.md` | Read and Write. Given the intro file and nothing else; three predictions with confidences, committed before anything has read further |
| `agents/reader.md` | Read and Write. The whole paper, never the prediction; the delta sentence or the admission it cannot be written; the same-cell comparison |
| `agents/scorer.md` | Read and Write. The only agent that sees both notes. Scores three predictions, writes the non-obvious line, copies everything else |
| `agents/openreview-reader.md` | Read, Edit, Write. Quotes reviewers; four states for what the verb returned; the field file at three cards |
| `agents/dataset-scout.md` | Read, Bash, Write. Bash for the retrieval scripts only, no web tool. Every line names a host, a card section, or `could not determine` |
| `agents/author-tracker.md` | Read and Write. Groups by affiliation and co-authorship; every direction sentence checkable against the titles beside it |
| `agents/leakage-auditor.md` | Read and Edit. Eight Kapoor and Narayanan types, each with a quote or what was checked. Flags and evidence; no verdict |
| `agents/critic.md` | Read and Write. Fresh context, quotes the passage behind every finding, then the concession ladder. Never edits the file it judges |
| `skills/read/SKILL.md` | propose, confirm, cap of five, fetch, two rounds, `--skim`, `--place`, `check_cards` |
| `skills/verify/SKILL.md` | tags every reference line in place; never deletes |
| `skills/reviews/SKILL.md` | exact title only; one reader for the batch; the login state reported once |
| `skills/datasets/SKILL.md` | names from cards and experiments sections; one scout; no web search |
| `skills/groups/SKILL.md` | card authors only, three years, `--paper` always |
| `skills/audit/SKILL.md` | one card, on request |
| `skills/bits/SKILL.md` | groups recorded and reused; two cards minimum; evaluation and dataset bits count |
| `skills/critique/SKILL.md` | one file of any kind; the ladder with a tally per finding |
| `templates/research/` | `card.md` (16 headings), `prediction.md`, `reading.md`, `reviews.md`, `datasets.md`, `groups.md`, `bits.md`, `critique.md` — all registered with `check_headings.py` |
| `scripts/check_cards.py` | new: missing heading, a delta that is neither the sentence nor the admission, no pass value, a position that is neither a cell nor unplaced, an untagged reference, an empty section a later skill owns, a full read with no prediction score; 13 cases |
| `hooks/guard.py` | no code change. Cases for all eight agents, plus a frontmatter check that seven of them grant no Bash and none grants a web tool |
| `docs/APIS.md`, `CONTEXT.md`, `README.md`, `docs/design/skills-and-agents.md` | nine sources; eleven reading terms; the built lists |

## 3. Done-check

Static, and this is the whole automated check for the chunk: both script
selftests, the guard selftest, heading parity over fourteen templates,
`check_cards`, `check_analogs`, `check_landscape`, and plugin validation.

Live: §4 — dry runs by the implementing agent, not evals.

## 4. What the dry runs found, 2026-09-16

Three papers carded from the damage matrix, all in
`per-building damage classification × paired pre/post satellite`.

**The protocol earned its cost on the first paper.** Reading xBD
(arXiv 1911.09296), the predictor guessed an overall damage-classification F1
of 0.60 to 0.75, held back by class imbalance. The paper reports 0.2654, with
the major-damage class collapsing to 0.0094, and reports localization as IoU
rather than F1 at all. Scores 4, 2, 5; the non-obvious line came from the 2.
That is a fact about the paper a careful reading of the abstract would have
got wrong, and it is the line the three agents exist to produce.

**The same-cell comparison found a real contradiction.** Reading BDANet
(arXiv 2105.07364) with the xBD card as its sibling, the reader named two
conflicts: every method in BDANet's comparison table scores F1 in the 0.70 to
0.78 range while xBD's own baseline reports 0.2654, with no bridge stated
between the two tables; and BDANet reports Train and Test whose counts match
xBD's exactly while never mentioning the holdout partition xBD describes, so
it is not possible from either paper to say which split its Test is. That is
PaperQA2's contradiction detection at read time, and it cost one extra input
to an agent that already had the cell.

**Four things the runs corrected in the script.** Each is in the code with the
measurement beside it.

- A single `response.read()` raises `IncompleteRead` at exactly 4,194,304
  bytes on arXiv 2004.07312, every time, on every attempt; the same response
  read in 256 KiB chunks delivers all 4,973,168. The failure was the read-all,
  not the server, so the retry that appeared to fix it could never have worked.
- An author search for "Yu Shen" returns a profile with fifty papers since the
  floor, because the name belongs to several people. Resolving the author
  through the paper the card already names cuts it to eight. The verb takes
  `--paper` and `/groups` always passes it.
- The author-papers endpoint pages at 100 and promises no ordering, so
  filtering one page by year under-reports a prolific author badly. It pages
  to 500 now and declares the cap rather than presenting a partial list as a
  whole one — one of the six authors queried came back `complete: false`.
- GitHub search does not know what field you are in: a bare "xBD" returns an
  Xbox diagnostic tool above the xView2 solution. `datasets` takes `--context`
  and appends it to the GitHub query only, since hub ids are already
  namespaced.

**The critic found four real problems in a file written in the main thread an
hour earlier.** Pointed at `BITS.md`, it caught a group whose thesis
("one network trained end to end") was contradicted by one of its own cards, a
card marked `_not read_` used as evidence about what a paper does not state, a
two-part assumption whose halves had different support, and an ellipsis that
lost which paper concatenates and which subtracts. All four were correct and
all four are fixed. The ladder ran twice and scored both rebuttals 1, because
both were agreements dressed as rebuttals and an admission is not evidence
against a finding; on the first it also caught an error inside the rebuttal.
Two ladder rules — never concede twice in a row, and the runaway-agreement
flag — need the critic to concede and therefore did not fire.

**`/reviews` ran into its own limit, honestly.** Three real papers gave three
different states: two `no record`, one `login required` with the venue and url
still named. That is the whole state table exercised without credentials, and
the cards say which of the three happened and when.

## 5. What is not done

- No `evals/` cases for any of the eight skills. The repo's behavioural tier
  is untouched by this chunk, by decision.
- The milestone's live test — DA-SegFormer and two competitors, `/bits` on the
  wildfire matrix — is the acceptance run and belongs to the user.
- `/reviews` has never read an actual review. Everything downstream of
  `login required` is offline-tested against fixtures and unexercised live.
- `--place` leaves the same-cell comparison unfilled. Filling it needs a
  re-read, and the skill says so rather than pretending a lookup can do it.
- Two of the concession ladder's rules have never fired: "never concede twice
  in a row" and the runaway-agreement flag both need the critic to concede,
  and across four findings it conceded nothing. Both are in `agents/critic.md`
  with their conditions; neither is exercised live.
- `/bits` has been verified to reuse recorded groups and never dissolve one,
  including across a full rewrite of its bits. It has **not** been shown
  assigning a genuinely new card or starting a group marked new: there are
  three cards and no fourth, and a fake one would have tested nothing.
