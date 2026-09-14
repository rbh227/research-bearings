# Chunk 3 spec: `/scout`, the breadth tool

2026-09-14. Supersedes the chunk 3 the map had pencilled in (the landscape
chain) and re-scopes chunk 2's premise for this skill only. Tickets in
`.scratch/chunk-03-analogs/issues/`.

## 1. Decision record

- **Why.** The sheet's founding rule, three times over: never generate from
  the nearest papers alone; force seeds from adjacent fields; find the fields
  that share the shape and not the citation graph (narrow-exploration study,
  Swanson, Uzzi). Chunk 2 built a snowball, which by construction finds only
  the neighbourhood of what you already have. The plan had scheduled breadth
  last. Wrong order for what the plugin is for.
- **Posture.** Trust the model to think; verify what it cites. The model's
  recall is the source of breadth. The fluent-confident-false failure measured
  all week is handled by resolving every citation at the end and marking what
  does not resolve — not by forbidding the thinking. Applies to this skill. The
  snowball keeps its every-line-tool-sourced contract and is parked.
- **Naming.** This skill is `/scout` — it is what finds papers broadly. The
  parked snowball skill becomes `/snowball`. `paper-scout` keeps its name; it
  is the snowball's agent and is still dispatched by it. One meaning per word.
- **Shape.** One skill, inline, no new agent, minutes per run. The skill has
  the session's context, which is the point.
- **Depth.** All the way to an opportunity per field, labelled speculative,
  with the transfer argument underneath it and absence kept mechanical.

## 2. The skill: `/scout`

`skills/scout/SKILL.md`. `allowed-tools: Read, Glob, Bash, AskUserQuestion`.
Writes `research/analogs/<slug>.md`. The guard's Bash fence applies to this
plugin's *agents*; the skill runs in the main thread, so its Bash is the
user's own grant. It still calls nothing but the retrieval script.

**Precondition — soft.** `snowball.py health` must print JSON. `key_present:
false` is stamped, not a stop. No `research/QUESTION.md` is stamped
*unframed*, not a stop: a broad "what should I even be looking at" is a valid
input and the skill says which kind it got.

**Input.** In this order, each overriding the last: `research/QUESTION.md`
(`## Question`, scope, `## Vocabulary`); `research/framing-log.md` `##
Rejected framings` (alternative shapes of the same interest — searched as
shapes in their own right, ticket 04 decides how many); the invocation text.

**Confirm.** Show the user the shape (step 1) and the field list (step 2)
before any search. This is the one place a human can steer breadth cheaply;
the search is seconds, the framing is the work.

**Steps.**

1. **Shape.** The problem without the home field's nouns. `## Vocabulary` is
   the list of words to remove. Written by the skill from its own
   understanding.
2. **Fields.** 5–10 that share the shape and not the vocabulary, each with
   the words *that* field uses. Uzzi's rule: mostly adjacent, one or two
   strange. The home field is not a field. From recall.
3. **Papers.** One `search "<field's words>" --limit 10` per field. Never the home vocabulary. Read what came back; keep two or
   three per field that look like they carry a movable method; add a
   remembered paper if the search missed it. Then per field: what shape it
   shares, why the method might transfer, what is different, and the
   opportunity — what you would try. The opportunity is speculative and says
   so.
4. **Verify.** `snowball.py verify` over every paper named anywhere in the
   file — by id where there is one, by title where there is not. Resolved
   papers get their S2 id written in. Unresolved ones stay, marked in place as
   `_unresolved: not found by title_`. Nothing is silently dropped.

**Report.** Show the file. Say: fields, papers, unresolved count, and whether
the run was framed or unframed.

**Bound.** No budget and no `--run`: a crawl needs a ledger because it
compounds, and search does not — every call returns at most `--limit` rows and
starts nothing. The run's size is searches × limit, and the searches are the
field list the user approves at the confirm step, which is why that step must
enumerate every search including the `Nearest existing:` ones. `## Status`
reports searches made and rows returned. **Corrected 2026-09-14**, after an
adversarial review: the skill passed `--run`/`--budget` on every search and
claimed the ledger enforced them; `search` reads the ledger and never charges
it, so the budget was decorative and `## Status` would have reported zero
papers touched on a run that returned a hundred rows.

**Rules this skill applies.** Narrow-exploration study (force seeds from
adjacent fields); Swanson (strip the nouns, search each characteristic without
the home vocabulary); Uzzi (conventional core, strange injection); *absence is
mechanical* (§3).

**Refusals.**

| The shortcut | Why not |
|---|---|
| "These are well-known papers, I'll skip verify." | The well-known ones are the ones memory gets wrong. Measured 2026-09-14: a title that did not say ViT, cited as saying ViT. |
| "Nobody has done this." | Show what the search returned. The reader concludes. |
| "I'll search with the question's own terms first, to anchor." | The home vocabulary finds the home field. That is `/snowball`'s job. |
| "Remote sensing counts as an adjacent field." | It is the home field with a wider collar. A field that shares the citation graph is not an analog. |
| "One field, ten papers, done properly." | Breadth is the deliverable. Five fields minimum. |
| "The search returned nothing, so the field is empty." | It returned nothing *for those words*. Re-query once in different words, then report both. |

## 3. Absence stays mechanical

The one chunk 2 rule that survives the posture change. Per opportunity, one
line: `Nearest existing: \`<the opportunity, in the field's words>\` → N rows;
closest: <title> (S2 id)`. "Unexplored", "gap", "novel", "nobody" do not
appear. This is what would have stopped chunk 2's 2,847-character "not
unexplored — but only barely", and it costs one search.

## 4. The script: `verify`

`snowball.py verify [--title "<t>"]... [--id <S2|ARXIV:|DOI:>]...`

One JSON object: `results[]`, each `{query, kind: title|id, resolved: bool,
paperId, title, year, match}`; `resolved_count`, `unresolved_count`. Titles
resolve through `search` with the title as the query, matched by normalised
title comparison (case, punctuation, whitespace folded; stdlib only). **Only an
exact match after folding resolves.** A prefix or substring match is returned
as `NOT the same paper unless you say so`, naming the candidate and its id:
measured 2026-09-14, "Attention Is All You Need for Wildfire Damage Assessment"
prefix-matched "Attention Is All You Need" and came back resolved, carrying that
paper's id onto a remembered citation — the fabrication this verb exists to
catch, wearing a checkmark. Ids resolve through
`batch`. Does not charge the ledger; does write records. Selftest cases:
exact title, punctuation-variant title, a title that does not exist, an id,
a bad id, mixed batch.

## 5. The template

`templates/research/analogs.md`, registered with `check_headings.py` against
`skills/scout/SKILL.md`. Fixed headings:

`## Question` · `## Shape` · `## Fields` · `## Verification` · `## Status`

Under `## Fields`, one `###` per field, fixed lines:

```
### <field, in its own words>
- Shares: <the shape element>
- Searched: `<query>` → <N> rows
- Papers:
  - <title> · <year> · S2 `<id>`
  - <title> · <year> · _unresolved: not found by title_
- Transfer: <one paragraph>
- Opportunity (speculative): <one paragraph>
- Nearest existing: `<query>` → <N> rows; closest: <title> (S2 `<id>`)
```

`## Verification` lists every paper in the file with resolved/unresolved and
the counts. `## Status`: date, slug, searches made, rows returned,
framed/unframed, key present or not.

## 6. Done-check

Mechanical only, for now. The user's call, 2026-09-14: no testing yet — the
point of this chunk is the skillset coming together, and a live run is judged
once there is a set to judge.

1. **`scripts/check_analogs.py`, seconds, no LLM.** Every `- <title> ·` line
   under `## Fields` carries either an S2 id or the unresolved marker;
   `## Verification`'s counts agree with the lines; no `###` field name
   contains a word from `## Vocabulary`; at least five `###` fields; the four
   banned absence words are absent. Run by the static-checks verb.
2. **Static checks green** — manifests, heading parity, both selftests.

Deferred, and recorded here so it is not lost: a live run on the acceptance
topic with the user reading the output cold, and a breadth heading in
`evals/gold/wildfire-cv.md` (*work from another field that turned out to
matter to me*) as the recall number this tool is eventually measured on. No
judge tier, then or now. The snowball's eval cases stay and still run under
their tag; they stop being developed.

## 7. Cleanup

A ticket of its own (07): after the rename and the new skill land, nothing in
the tree is unreferenced. Every function in `snowball.py` and `guard.py` has a
caller or a selftest; every fixture is read by a case or a selftest; every
eval case targets a shipped skill or agent by its current name; no shipped
`.md` names a path, tool, or skill that no longer exists; the design docs
mark what is parked. What is *parked* stays — the snowball, its agent, its
template, its tier — and is labelled parked wherever it appears. Dead is
deleted.

## 8. Order

01 `verify` verb → 02 rename → 03 template + heading parity → 04 the skill →
05 `check_analogs.py` → 07 cleanup. 04 depends on 01–03; 07 is last on
purpose. There is no 06: the first live run is deferred until the skillset is
together.
