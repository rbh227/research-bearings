---
type: llm
weight: 2
---
There is no `research/` folder. The skill's input rules say that with none
of the files the run is "unframed", which is a normal way to use it: say
which mode you are in, and stamp it in `## Status` when the log is written.
Pass only if ALL hold:
1. The reply does not refuse and does not send the user to setup or frame
   first.
2. It says explicitly that it is running unframed (that word, or that
   there is no question file and it is proceeding from what was typed).
3. It begins with the important-problems question, using the user's
   stated interest as the seed.
