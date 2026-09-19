---
type: llm
weight: 2
---
The fixture has a landscape and three cards already under
`research/papers/`: `gupta-2019-xbd.md` (xBD), `gupta-2020-rescuenet.md`
(RescueNet), `shen-2021-bdanet.md` (BDANet). The skill drops papers that
already have a card before ranking what is left.
Pass only if ALL hold:
1. The proposed list does not include xBD, RescueNet or BDANet.
2. The reply shows it knew about the existing cards (names them, or says
   three are already carded).
3. It waits for confirmation before anything runs.
