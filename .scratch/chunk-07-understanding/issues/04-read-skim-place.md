# 04: `/read --skim`, `--place`, and the no-matrix path

Type: task
Status: done
Blocked by: 03

## What to build

Three additions to `/read` and the reader. `--skim`: the reader only, in skim
mode, from the intro file; fills what the intro supports, marks every other
field `not read`, card says `pass: 1`, no prediction, no score, no same-cell
comparison. The skim fallback: when `fetch` returns `no text`, the same skim
mode runs from the record's abstract and the card says why. `--place`: no
agents; for every card marked `unplaced`, the main thread finds the paper's
line in the current matrix by id and fills the position; a card in no cell
stays unplaced and is listed. The no-matrix path: with no matrix file, the
full protocol still runs, the card is `unplaced`, the reader is told there is
no matrix and the comparison section holds the `no matrix` marker.

## Acceptance

- [x] `--skim` on a real paper produces a card with `pass: 1`, no prediction note, and `check_cards` green.
- [x] With the matrix file absent, a full read produces an `unplaced` card and the run report lists it.
- [x] With the matrix restored, `--place` fills that card's position without dispatching any agent, and a card whose paper is in no cell is reported as still unplaced.
- [x] A paper with no open-access text is skimmed from the abstract and the card states the fetch state.

## Resolution

2026-09-16. `--skim`, `--place`, the no-matrix path and the abstract fallback,
all in `skills/read/SKILL.md` and `agents/reader.md`.

Verified on RescueNet (arXiv 2004.07312), read with the matrix moved aside:
the reader in skim mode produced a pass-1 card with five fields `not read`,
`_unplaced_`, and `_no matrix_` for the same-cell comparison. `check_cards`
green. With the matrix restored, `--place` found the paper's line by id and
filled the cell with no agent dispatched.

**What `--place` cannot do, found by doing it.** It fills the position and
leaves `## Same-cell comparison` as `_no matrix_`. Placing is a lookup in the
matrix; comparing needs the paper open and the siblings read, which is an
agent and a full text. The card says it was placed afterwards and the skill
says a re-read is what fills the comparison.

The same run turned up the download bug: a single `response.read()` raises
IncompleteRead at exactly 4,194,304 bytes on this paper, every time, and the
same response read in 256 KiB chunks delivers all 4,973,168. The retry that
appeared to fix it could never have worked.
