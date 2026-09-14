# Scripts, not servers

Type: task
Status: resolved
Blocked by:

## Question

The first run of the chunk 2 eval suite (2026-09-13) showed the MCP packaging
breaking three separate ways in one day — a 30 s cold start past the connect
ceiling, credentials in a file the sandbox could not see, a persistent process
the OS killed — and two real plugin defects underneath: the budget was a
sentence and did not hold (told 40, touched 114–160), and a missing *optional*
key read as a dead server. The user asked why there was a server at all. The
plan's reason ("use existing MCP servers so we write no custom code") was
already broken: no existing server walked citations, so `s2_snowball.py` was
written anyway. The user chose ARS's shape — scripts, run on demand, nothing
resident — and accepted the rework.

Supersedes ticket 10's choice of a server, and its reading of ticket 03:
"scouts must be denied Bash" becomes "the scout's Bash is fenced by the guard to
one script".

## Acceptance

- [x] `scripts/retrieval/snowball.py`: search, references, citations, batch,
      health; standard library only; `--selftest` offline; budget kept in a
      per-run ledger on disk and enforced before the request, hop limit clamped
      to what remains; key from `SEMANTIC_SCHOLAR_API_KEY` or one line in
      `~/.config/research-bearings/s2-api-key`.
- [x] `hooks/guard.py` fences `Bash` for this plugin's agents to
      `python3 <plugin>/scripts/retrieval/<x>.py ...` with no shell operators;
      selftest covers it.
- [x] `/scout` and `paper-scout` call the script; the agent accepts a saved crawl
      for offline replay; `/scout` reads the ledger back and reports it over the
      section's figure if they differ.
- [x] `/setup` probes the script, not a server; template wording follows.
- [x] Deleted: `servers/`, `.mcp.json`, the `userConfig` block, both third-party
      servers, the two-arm eval runner, the live-crawl eval cases.
- [x] Eval suite re-cut: agent cases replay `scripts/retrieval/fixtures/crawl-dmg/` and need
      no network, key or Bash grant; one skill case withholds Bash so the
      precondition must refuse; one invocation runs everything.
- [x] No unused code or fixtures left; every shipped `.md` describes the script
      design, with the old design kept only as history in the chunk 2 spec.
- [x] README carries a short table of free academic APIs, labelled as unmeasured
      except the one in use.
- [x] Static checks green; plugin reinstalled (0.3.1) so other projects pick it up.
- [ ] The re-cut suite green on one run. **Partial:** 6 of 9 at 1.00 on the
      second run (absence, invents-no-prose, missing-fields, refuses-without-
      script; refuses-memory-papers and reports-stop-reason failed only on a
      grader premise and a prompt wording, both fixed in 91eeb05 and not yet
      re-run). stamps-unanchored wrote its file; its judge call, stamps-no-key's
      re-run and title-only-greylit are blocked by the account's spend limit
      (resets 11pm America/New_York). Then the 3-run verdict.

## Answer

Done, on the acceptance list above, with one box partial for a reason outside
the repo. The walker is `scripts/retrieval/snowball.py` — standard library, one
file, run on demand — with the budget as a per-run ledger enforced before the
request and clamped per hop and per batch, and the key from an env var or one
line in `~/.config/research-bearings/s2-api-key`. The server, its manifest, the
`userConfig` block and both third-party servers are gone. The guard fences the
scout's Bash to the script (22 cases). `/scout` reads the ledger back and reports
it over the section's figure if they differ. The suite is re-cut around a saved
crawl under `scripts/retrieval/fixtures/crawl-dmg/` — not `evals/`, which the
harness denies the agent — and needs no network, key or Bash grant.

Two contract gaps and two script defects were found and closed on the way
(chunk 2 spec §11.7–§11.9): the skill interpreting the field; `Kept because`
unbounded in content; a batch that could overspend; a ledger write failure that
silently reset the budget. Nothing found says the scout fabricates: in every run
where it could not reach its data, it refused to write rather than fill cards
from recall.

**Done:** ad68db7, 9b5b7ff, 6b137e8, cc21e16, 91eeb05 — script, ledger, guard,
swap, re-cut suite, docs; the remaining eval runs wait on the spend limit.

## Comments
