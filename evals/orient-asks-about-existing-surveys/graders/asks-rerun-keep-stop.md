---
type: llm
weight: 2
---
The fixture has `QUESTION.md` (dated 2026-09-15 09:00) and
`landscape/surveys.md` (dated 2026-09-15 10:00), nothing else. For this
folder `python3 scripts/state.py` reports the `surveys` move as `done` —
the file exists and nothing upstream is newer — and `landscape` as `ready`.

Pass only if ALL hold:

1. Before running anything, the reply asks whether to rerun, keep, or stop on
   the existing surveys file (all three words, or clear equivalents).
2. That question carries the file's date (2026-09-15, or "the 15th") and
   says nothing upstream is newer than it (zero newer, or that the question
   file is older).
3. The landscape step has not begun: no seven queries are shown, no matrix is
   written.
4. It does not silently skip the surveys step, and does not rerun it unasked.
