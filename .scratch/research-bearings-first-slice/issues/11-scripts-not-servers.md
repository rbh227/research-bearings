# Scripts, not servers

Type: task
Status: claimed
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

- [ ] `scripts/retrieval/snowball.py`: search, references, citations, batch,
      health; standard library only; `--selftest` offline; budget kept in a
      per-run ledger on disk and enforced before the request, hop limit clamped
      to what remains; key from `SEMANTIC_SCHOLAR_API_KEY` or one line in
      `~/.config/research-bearings/s2-api-key`.
- [ ] `hooks/guard.py` fences `Bash` for this plugin's agents to
      `python3 <plugin>/scripts/retrieval/<x>.py ...` with no shell operators;
      selftest covers it.
- [ ] `/scout` and `paper-scout` call the script; the agent accepts a saved crawl
      for offline replay; `/scout` reads the ledger back and reports it over the
      section's figure if they differ.
- [ ] `/setup` probes the script, not a server; template wording follows.
- [ ] Deleted: `servers/`, `.mcp.json`, the `userConfig` block, both third-party
      servers, the two-arm eval runner, the live-crawl eval cases.
- [ ] Eval suite re-cut: agent cases replay `scripts/retrieval/fixtures/crawl-dmg/` and need
      no network, key or Bash grant; one skill case withholds Bash so the
      precondition must refuse; one invocation runs everything.
- [ ] No unused code or fixtures left; every shipped `.md` describes the script
      design, with the old design kept only as history in the chunk 2 spec.
- [ ] README carries a short table of free academic APIs, labelled as unmeasured
      except the one in use.
- [ ] Static checks green; the re-cut suite run at least once; plugin reinstalled
      so other projects pick up 0.3.0.

## Answer

_pending — filled at resolve_

## Comments
