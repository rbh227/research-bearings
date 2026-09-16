# 04: `/read --skim`, `--place`, and the no-matrix path

Type: task
Status: ready-for-agent
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

- [ ] `--skim` on a real paper produces a card with `pass: 1`, no prediction note, and `check_cards` green.
- [ ] With the matrix file absent, a full read produces an `unplaced` card and the run report lists it.
- [ ] With the matrix restored, `--place` fills that card's position without dispatching any agent, and a card whose paper is in no cell is reported as still unplaced.
- [ ] A paper with no open-access text is skimmed from the abstract and the card states the fetch state.
