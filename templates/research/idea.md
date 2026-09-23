# <the idea, as a title of three or four words>

<!-- One idea, at research/ideas/<slug>.md. Nine headings, fixed.
     Written by /research-bearings:ideas, from a candidate that the index did
     not show to be an increment.

     This is what /premortem, /rank and /spec will read. They read it by
     heading, so a missing heading is a downstream skill reading nothing and
     believing it found nothing. check_ideas.py enforces the shape.

     Nothing here is ranked or scored. A page is a proposal with its seed, the
     nearest thing that already exists, and the cheapest experiment that would
     end it. -->

## Idea

<!-- One sentence: what you would actually do. Not the area it is in.

     "Train the damage head on the pre-image alone and use the post-image only
     as a consistency signal" is an idea. "Better domain adaptation for damage
     assessment" is an area. -->

## Seed

<!-- Where this came from, in the log's own vocabulary, with the file and the
     line:

     - Kind: bit | analog | contradiction | abandoned | persona | conversation
     - From: research/BITS.md § Bits § <the bit's heading>
     - Line: "<the clause that produced it, quoted>"

     A candidate that cannot name its seed was generated from what the model
     already knew, which is the failure mode this whole stage is built
     against. -->

## What it flips

<!-- The assumption, contradiction or stopped direction this goes against,
     quoted from the file it lives in.

     For a bit: the bit's sentence, and what follows if it is false.
     For a contradiction: the two lines that disagree, and what would settle it.
     For an abandoned direction: what stopped it then, and what has changed
       since — tools, data, compute — quoted from the record where possible.
     For a persona question: the question, attributed.
     For a conversation seed: what the user said. -->

## Nearest existing

<!-- The absence rule. The only shape a claim about what does not exist may
     take here:

     - Query: "<the candidate, in the home vocabulary, as it was put to the index>"
     - Papers the query found: <n> of 5 requested (counts.seeds)
     - Rows: <n> of a 30-paper budget (counts.neighborhood)
     - Nearest: <title> · <year> · <S2|arXiv|OpenAlex|DOI> `<id>` · verified
     - Reading: <one line — what the nearest paper does that this does not, or
       the honest statement that it is close>

     BOTH numbers, because the row count saturates. Measured 2026-09-16: a walk
     with --budget 30 returned "neighborhood 30" for a query in a dense area,
     and it will return 30 for almost any query that has seeds at all. "30 of
     30" means the walk filled up, not that the literature holds thirty papers.
     The other number is the one that moves: it is how many of the five
     requested papers the search could find for this query at all, and a query
     that finds one or two is the thin case worth noticing. It is not called a
     seed count here because `seed` already means a paper a walk starts from
     (CONTEXT.md § Gathering terms) and this page's ## Seed heading means
     something else entirely.

     The analog pages carry the row count alone, from the same call — this page
     carries one number more, and that is deliberate.

     "Unexplored", "gap", "novel" and "nobody" do not appear on this page.
     You ran one walk. Report the counts and let the reader conclude. -->

## What would have to be true

<!-- The assumptions the idea rests on, one per line, each marked:

     - <assumption> — checkable: <how, and roughly what it costs>
     - <assumption> — not checkable before the experiment

     An idea whose assumptions are all unmarked is a wish. An idea whose
     assumptions are all checkable is probably an increment. -->

## Cheapest kill

<!-- The smallest experiment that would end this idea, and the result that
     would end it:

     - Experiment: <what you would run>
     - Kills it if: <the result that means stop>
     - Costs: <data, compute, time — roughly>

     Steinhardt: order by the cheapest kill. This line is what /rank sorts on
     later, so it is written here, before anything is invested. -->

## Typicality

<!-- One written sentence. Uzzi: the highest-impact work combines a mostly
     conventional core with a small atypical injection.

     "The core is standard segmentation on standard benchmarks; the atypical
     injection is the consistency objective borrowed from stereo matching."

     NOTHING COMPUTES THIS. It is a note, deliberately, and it is the same
     decision that struck similarity.py. -->

## References

<!-- Paper lines in the shape every other file uses, each carrying a verify
     tag:

     - <title> · <year> · <S2|arXiv|OpenAlex|DOI> `<id>` · verified
     - <title> · <year> · _candidate: prefix match only, <title it nearly matched> (<id>)_
     - <title> · <year> · _not found: checked s2, openalex, crossref_

     A reference with no tag is a claim nobody can check. A not-found paper
     stays in the file, marked. -->

## Status

<!-- Date. The skill and the round that produced it. Whether an earlier run
     marked this an increment and what changed. The counts this run reported.

     Written 2026-09-20 by /ideas, round 2. Seed: bit:<group>. Not marked an
     increment on any run. Nearest existing: <n> rows. -->
