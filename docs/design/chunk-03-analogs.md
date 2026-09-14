# Chunk 3: analogs — the breadth tool

Plan, 2026-09-14. Not yet a spec. Supersedes the chunk 3 the map had pencilled
in (the landscape chain: `/surveys`, `/landscape`, `/brief`) and re-scopes the
premise chunk 2 was built on. What it keeps from chunk 2 is the part that
works: the retrieval script, the ledger, the guard, `/setup`, `/frame`.

## 1. Why this, and why now

The plugin's founding rule is in the sheet three times over — *never generate
from the nearest papers alone; force seeds from adjacent fields; look for
fields that share the shape but not the citation graph* (the narrow-exploration
study, Swanson, Uzzi). Chunk 2 built a snowball tool, which by construction
finds only the citation neighbourhood of what you already have. Crop damage
from drone imagery shares your problem's shape and none of your citation
graph; a snowball out of hurricane-damage papers cannot reach it. The plan put
the breadth tools last, in Stage 4, behind three more librarian skills. That
was the wrong order for what the plugin is for.

Chunk 2 also spent its effort on the wrong premise for this job. It assumed
the model's recall of the literature cannot be trusted, so every line had to
trace to a tool call — cards, a guard, honesty graders, a 70-minute eval tier.
The user's call, 2026-09-14: **trust the model to think; verify what it
cites.** The model's recall is the *source* of breadth — it is the thing that
knows crop damage and lesion change share a shape — and the failure mode we
measured all week (fluent, confident, false) is handled by checking the
citations at the end, not by forbidding the thinking.

That posture applies to this skill. The snowball tool keeps its own; it is
parked, not repudiated.

## 2. What one run does

A user-invoked skill. It starts from whatever framing exists — `/frame`'s
`research/QUESTION.md` (the question, its scope, its `## Vocabulary`) and
`research/framing-log.md` (every framing that died on the way: alternative
shapes of the same interest, worth searching too) — plus whatever the user
says when invoking it, which may widen or narrow all of that. A broad "what
should I even be looking at" and a sharp "this paper's problem, elsewhere" are
both valid inputs; the skill reports which it was given.

Four steps.

**1. Shape.** Strip the problem to what it is without the home field's nouns.
"Per-region change classification on paired overhead imagery, sparse and
noisy labels, domain shift between events" — not "post-disaster building
damage assessment". The `## Vocabulary` heading is the list of words to remove.
The model does this from its own understanding; it is the step nothing else
can do.

**2. Fields.** Name 5–10 fields that share the shape and not the vocabulary,
each with the words *that field* would use. The model does this from recall.
Uzzi's rule shapes the set: mostly adjacent, plus one or two that are genuinely
strange.

**3. Papers.** For each field, one `search` in that field's own words — never
the home field's — through the retrieval script. Real rows, real ids. The model
reads what came back, picks two or three that look like they carry a method
worth moving, and may add a paper it remembers that the search missed. Then it
writes, per field: the shape it shares, why the method might transfer, what is
different, and **the opportunity** — what you would actually try. That last
part is speculative on purpose and labelled as such.

**4. Verify.** Every paper named anywhere in the output is resolved through the
script — by id where there is one, by title search where there is not. A paper
that does not resolve is not removed; it is marked, in place, as unresolved,
so the reader sees exactly where the model's memory outran the record.

Output: `research/analogs/<slug>.md`, a few thousand characters. Readable in
five minutes. Run time: minutes — the model writes a dozen paragraphs, not
twenty thousand characters of bibliography.

## 3. The one honesty rule that survives

Absence stays mechanical. "What you would try" may be as bold as the model
likes. "Nobody has done this" may not appear. What appears instead is what the
search returned: *a search for `<the opportunity, in the analog field's
words>` returned N rows; the closest were these.* The reader draws the
conclusion; the section carries the evidence. This is the rule that would have
stopped the 2,847-character "not unexplored — but only barely" from chunk 2,
and it costs nothing here.

## 4. What it reuses, adds, and parks

**Reused, unchanged:** `scripts/retrieval/snowball.py` (`search`, `batch`,
`health`, the key, the cache, the ledger), `hooks/guard.py`, `/setup`,
`/frame`, `question-critic`.

**Added:**
- The skill. Inline — no new agent. The skill has the session's context,
  which the user identified as the point: it knows what was actually wanted.
  A fresh-context critic that attacks the analogies (the plan's
  `transfer-checker`) is a later addition if the analogies turn out to be
  glib; it is not needed to ship.
- A `verify` verb on the script: takes titles and/or ids, returns
  resolved/unresolved with the matched record. Small. Makes step 4 one call
  and the done-check mechanical.
- A template, `templates/research/analogs.md`, with fixed headings so the
  heading-parity check covers it.

**Parked, not deleted:** the snowball skill and `paper-scout`, their section
format, their eval tier (the cases stay and still run; they stop being
developed), the section-renderer idea (moot), `/landscape`, `/surveys`,
`/brief`. The chunk 2 spec stands as the record of that tool.

**Superseded in `skills-and-agents.md`:** Stage 4's `/fingerprint`,
`/analogs` and `/flip` collapse into this one skill; `analog-scout`,
`field-carder`, `transfer-checker`, `flip-generator` and `novelty-checker`
come off the agent count.

## 5. Done-check

No three-run judge tier. Three checks, in this order:

1. **Mechanical.** `verify` over the output file: every cited paper resolves.
   No field name contains a word from the home `## Vocabulary`. At least five
   fields. Run in seconds, no LLM.
2. **The user reads it,** on the real question, and says whether the
   farming-from-the-air kind of result showed up and whether the transfer
   arguments are worth anything. A run is minutes, so this is the loop.
3. **The gold set changes meaning.** `evals/gold/wildfire-cv.md` was a depth
   test — in-field recall. It gains a heading: *work from another field that
   turned out to matter to me*. That is the breadth recall test, and it is the
   one this chunk is measured on.

## 6. Open

- **Naming.** The user calls this "the scout" — it is what finds papers
  broadly. Recommendation: this skill takes `/scout`; the parked snowball
  skill becomes `/snowball`, which is what it does. One meaning per word.
- **Whether step 2's field list is the model's alone,** or whether the
  framing log's rejected framings are searched as shapes in their own right.
  Cheap to do both; decide after the first real run.
- **A fresh-context critic** for the analogies. Not before the first run
  shows they need one.

## 7. Order

1. `verify` verb, with selftest cases. Half a day.
2. The template and the skill. A day.
3. Static checks green; one run on the acceptance topic; the user reads it.
4. The gold set's new heading, and the map.
