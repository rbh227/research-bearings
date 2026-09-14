# <the problem, as a title>

<!-- Written by /research-bearings:scout. One run, one file, five headings.
     This is the breadth artifact: fields that share the problem's shape and
     not its citation graph. The depth artifact - the citation neighbourhood of
     a question - is research/landscape/<slug>.md, written by /snowball. -->

## Question

<!-- What the run was given, in the words it was given, then where it came
     from on its own line: "Framed — research/QUESTION.md" or "Unframed — run
     on the invocation text as typed." If the invocation widened or narrowed
     the framed question, say how, in one line. -->

## Shape

<!-- The problem with the home field's nouns removed: what it is structurally,
     in words any field would recognise. "Per-region change classification on
     paired overhead imagery, sparse and noisy labels, domain shift between
     captures" — not "post-disaster building damage assessment".

     Then, on its own line, the removed vocabulary, so a reader can see what
     was stripped and judge whether the shape survived it. -->

## Fields

<!-- One ### per field, five minimum. Never the home field, and never a field
     that shares the home field's citation graph. One search each, in THAT
     field's words.

     ### <field, in its own words>
     - Shares: <which element of the shape>
     - Searched: `<query>` → <N> rows
     - Papers:
       - <title> · <year> · S2 `<id>`
       - <title> · <year> · _unresolved: not found by title_
     - Transfer: <one paragraph — why the method might move to this problem,
       and what is different about it. Grounded in what the rows say.>
     - Opportunity (speculative): <one paragraph — what you would actually try.
       Labelled speculative because it is: it is the one part of this file that
       is not sourced from anything.>
     - Nearest existing: `<query>` → <N> rows; closest: <title> (S2 `<id>`)

     The "Nearest existing" line is the absence rule. It reports what a search
     for the opportunity returned, and lets the reader conclude. "Unexplored",
     "gap", "novel" and "nobody" do not appear in this file. -->

## Verification

<!-- Every paper named anywhere above, checked by
     `snowball.py verify`, with the counts:

     - <title> — resolved, S2 `<id>`
     - <title> — unresolved, closest: <what the search returned>

     Then: resolved N, unresolved M, checked N+M.

     An unresolved paper stays in ## Fields, marked. It is not deleted: where
     the model's memory outran the record is information the reader wants. -->

## Status

<!-- Date. Run slug. Searches made, and rows returned across them — not a
     papers-touched count: this skill makes no hops, so that figure is always
     zero and reads as though nothing was retrieved. Framed or unframed. Key
     present or not — unkeyed runs rate-limit and may return fewer rows per
     field, which is a degradation and is stamped here, not silently absorbed.
     Any field whose search returned zero rows after a re-query. -->
