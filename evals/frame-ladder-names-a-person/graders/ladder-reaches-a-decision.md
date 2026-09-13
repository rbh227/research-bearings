---
type: llm
focus: last_message
weight: 1
---
The USER offered "advances the state of the art in remote sensing" and "helps the
research community" as the significance of their question. Both fail Booth's
so-what test: neither names anyone who decides anything. The agent's job is to
reject that and push for someone real.

Pass if BOTH hold:

1. The agent rejects the offered significance — walks a so-what recursion on it
   and reaches a negative verdict, however phrased.
2. It pushes the user toward a named person or role who makes a specific
   decision the answer would change, and toward what that person would do
   differently. Offering several candidate roles for the user to choose between
   counts, and so does naming the user's own lab as the real decision-maker,
   provided a concrete decision is attached.

Fail only if the agent ACCEPTS the offered significance and moves on to fill in
the rest of the question, or if it never tests the significance at all.

Important: the agent will QUOTE the user's phrases — "advances the state of the
art", "the research community" — in order to attack them. Quoting them, walking
them down a ladder, or naming them as the thing that fails is the CORRECT
behaviour and must not be read as accepting them. Judge only what the agent
concludes about that significance, never the mere presence of those words in its
message.
