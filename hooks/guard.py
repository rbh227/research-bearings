#!/usr/bin/env python3
"""Write-scope guard for research-bearings agents.

A PreToolUse hook on Write|Edit|Bash|WebSearch|WebFetch. Agents shipped by
this plugin may only write under <project>/research/ and may only run this
plugin's own scripts. Everything else — the main thread, other plugins'
agents, Claude Code's built-in agents — passes through untouched.

  Write|Edit          file_path must resolve under <project>/research/.
  Bash                the command must be exactly `python3 <plugin>/scripts/<x>.py ...`
                      with no shell operators outside quotes and no command
                      substitution anywhere. Back since 2026-09-15, when the
                      `searcher` agent was granted Bash.

                      The root widened from scripts/retrieval/ to scripts/ on
                      2026-09-18 so `ingest_runs.py` could live where it
                      belongs rather than be smuggled into the retrieval
                      directory. What the fence actually guarantees is
                      unchanged: this plugin's own reviewed code, one command,
                      no shell syntax, no chaining, no other binary. It is
                      still the case that no agent can run the user's training
                      script — that is the whole reason "whether to spend
                      compute" is a human gate and not a sentence in a skill.
  WebSearch|WebFetch  denied to every agent this plugin ships except
                      `searcher`, which may WebSearch as a last resort when
                      every index returned nothing (docs/APIS.md). The main
                      thread is not an agent, so /scout's WebFetch of a page
                      the indexes pointed at passes through.

The Bash fence was here from chunk 2 to 2026-09-14, left with `paper-scout`,
and came back from 249188a on 2026-09-15 with its cases, including the
quote-aware scan that took two attempts to get right.

Per-agent scoping is only possible this way: plugin-shipped agent frontmatter
ignores `hooks`, and PreToolUse has no agent-type matcher, so the script reads
`agent_type` from stdin and scopes itself.

Standard library only, so there is no install story. Run --selftest to check it.
"""

import json
import os
import shlex
import sys

PLUGIN_PREFIX = "research-bearings:"
WRITE_ROOT = "research"
SCRIPT_ROOT = ("scripts",)
INTERPRETERS = ("python3", "python")
# Characters that separate or redirect commands when the shell sees them
# outside quotes. `&` counts as much as `;` does: `snowball.py health & curl
# evil` is two commands.
SHELL_OPERATORS = ";&|<>()\n\r"
# Command substitution runs even inside double quotes. Only single quotes
# suppress it, so these are refused wherever they are not single-quoted.
SUBSTITUTION = "$("
BACKTICK = "`"
# The one agent allowed on the open web, and the one tool it gets there.
WEB_ALLOWED = {"research-bearings:searcher": ("WebSearch",)}


def plugin_root():
    return os.path.realpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def _roots(payload, env):
    """Directories a research/ folder may hang off, most authoritative first.

    CLAUDE_PROJECT_DIR stays at the project root even inside a worktree, where
    cwd follows Claude. Both are accepted so neither case is a false denial.
    """
    candidates = [env.get("CLAUDE_PROJECT_DIR"), payload.get("cwd")]
    seen, out = set(), []
    for c in candidates:
        if not c:
            continue
        r = os.path.realpath(c)
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


def decide_write(payload, env):
    path = (payload.get("tool_input") or {}).get("file_path")
    if not path:
        return None

    target = os.path.realpath(path)
    for root in _roots(payload, env):
        allowed = os.path.realpath(os.path.join(root, WRITE_ROOT))
        if target == allowed or target.startswith(allowed + os.sep):
            return None

    return (
        "research-bearings agents may only write under {}/. Refused: {}. "
        "If this agent genuinely needs to write elsewhere, that is a contract "
        "change, not a path change.".format(WRITE_ROOT, target)
    )


def has_shell_syntax(command):
    """True if the command carries shell syntax that could run a second thing.

    Quote-aware in both directions, and both directions were wrong once:
    `search "flood | damage"` is one argument the shell never splits, and was
    being refused; `health & curl evil` is two commands, and was being allowed.
    So operators count only outside quotes, and command substitution counts
    inside double quotes too, because the shell still runs it there.
    """
    i, n, quote = 0, len(command), None
    while i < n:
        c = command[i]
        if quote == "'":
            if c == "'":
                quote = None
            i += 1
            continue
        if c == "\\":
            i += 2
            continue
        if command.startswith(SUBSTITUTION, i) or c == BACKTICK:
            return True
        if quote == '"':
            if c == '"':
                quote = None
            i += 1
            continue
        if c in "'\"":
            quote = c
            i += 1
            continue
        if c in SHELL_OPERATORS:
            return True
        i += 1
    # An unterminated quote is not a command this guard can reason about.
    return quote is not None


def decide_bash(payload, env):
    command = ((payload.get("tool_input") or {}).get("command") or "").strip()
    if not command:
        return None

    why = (
        "research-bearings agents may only run this plugin's own scripts: "
        "`python3 <plugin>/scripts/<script>.py ...`, nothing else and "
        "nothing chained. Your own code is yours to run. Refused: {}".format(command[:200])
    )
    if has_shell_syntax(command):
        return why
    try:
        parts = shlex.split(command)
    except ValueError:
        return why
    if len(parts) < 2 or os.path.basename(parts[0]) not in INTERPRETERS:
        return why

    root = plugin_root()
    script = parts[1]
    # The agent is told to spell the path with ${CLAUDE_PLUGIN_ROOT}. The hook's
    # own environment may or may not carry that variable, so resolve it here
    # rather than trusting expandvars to.
    for token in ("${CLAUDE_PLUGIN_ROOT}", "$CLAUDE_PLUGIN_ROOT"):
        script = script.replace(token, root)
    script = os.path.realpath(os.path.expandvars(script))

    allowed = os.path.realpath(os.path.join(root, *SCRIPT_ROOT))
    if script.startswith(allowed + os.sep) and script.endswith(".py"):
        return None
    return why


def decide(payload, env):
    """Return a denial reason, or None to allow.

    Allowing is the default for everything this guard does not understand. A
    guard that fails closed would block the user's own edits on a malformed
    payload, which is a worse failure than the one it prevents.
    """
    agent = payload.get("agent_type") or ""
    if not agent.startswith(PLUGIN_PREFIX):
        return None

    tool = payload.get("tool_name") or ""
    if tool in ("Write", "Edit"):
        return decide_write(payload, env)
    if tool == "Bash":
        return decide_bash(payload, env)
    if tool in ("WebSearch", "WebFetch"):
        return decide_web(agent, tool)
    return None


def decide_web(agent, tool):
    if tool in WEB_ALLOWED.get(agent, ()):
        return None
    return (
        "research-bearings agents read the indexes, not the open web. {} is "
        "refused for {}. The two exceptions are in docs/APIS.md; anything else "
        "is a contract change, not a tool change.".format(tool, agent)
    )


def run(stdin_text, env):
    """Return (exit_code, stdout). Used by main and by the selftest."""
    try:
        payload = json.loads(stdin_text)
        if not isinstance(payload, dict):
            return 0, ""
    except (ValueError, TypeError):
        return 0, ""

    reason = decide(payload, env)
    if reason is None:
        return 0, ""

    return 0, json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason,
            }
        }
    )


# --------------------------------------------------------------------------
# selftest
# --------------------------------------------------------------------------


def selftest():
    import tempfile

    failures = []

    def check(name, stdin_text, env, want_deny):
        code, out = run(stdin_text, env)
        got_deny = bool(out) and '"deny"' in out
        ok = code == 0 and got_deny == want_deny
        print("  {} {}".format("PASS" if ok else "FAIL", name))
        if not ok:
            failures.append(name)
            print("       exit={} deny={} (wanted deny={})".format(code, got_deny, want_deny))

    with tempfile.TemporaryDirectory() as project:
        project = os.path.realpath(project)
        os.makedirs(os.path.join(project, "research", "landscape"))
        env = {"CLAUDE_PROJECT_DIR": project}

        def payload(agent, path):
            return json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Write",
                    "agent_type": agent,
                    "cwd": project,
                    "tool_input": {"file_path": path},
                }
            )

        inside = os.path.join(project, "research", "QUESTION.md")
        nested = os.path.join(project, "research", "landscape", "matrix.md")
        at_root = os.path.join(project, "README.md")
        escape = os.path.join(project, "research", "..", "secrets.md")
        script = os.path.join(plugin_root(), "scripts", "retrieval", "snowball.py")
        scout = "research-bearings:searcher"

        print("guard.py selftest")

        # 1. No agent_type at all: the main thread. Never touched.
        check(
            "main thread write is allowed",
            json.dumps({"tool_name": "Write", "cwd": project,
                        "tool_input": {"file_path": at_root}}),
            env, False)

        # 2. Somebody else's agent. Not our business.
        check("another plugin's agent is allowed",
              payload("Explore", at_root), env, False)

        # 3-4. Our agent, inside the write root.
        check("our agent writing inside research/ is allowed",
              payload("research-bearings:question-critic", inside), env, False)
        check("our agent writing deep inside research/ is allowed",
              payload(scout, nested), env, False)

        # 5-7. Our agent, outside the write root.
        check("our agent writing at project root is DENIED",
              payload("research-bearings:question-critic", at_root), env, True)
        check("our agent writing to /tmp is DENIED",
              payload("research-bearings:question-critic", "/tmp/loose.md"), env, True)
        check("our agent escaping via research/.. is DENIED",
              payload("research-bearings:question-critic", escape), env, True)

        # 8. A prefix that merely looks like ours.
        check("a path like research-notes/ does not count as research/",
              payload("research-bearings:question-critic",
                      os.path.join(project, "research-notes", "x.md")), env, True)

        # 9-11. Malformed input must never block the user's own work.
        check("malformed JSON is allowed", "{not json", env, False)
        check("empty stdin is allowed", "", env, False)
        check("JSON that is not an object is allowed", "[1,2,3]", env, False)

        # 12. Our agent, but no file_path in the payload.
        check("missing file_path is allowed",
              json.dumps({"agent_type": "research-bearings:question-critic",
                          "cwd": project, "tool_input": {}}), env, False)

        # 13. No CLAUDE_PROJECT_DIR: fall back to cwd.
        check("falls back to cwd when CLAUDE_PROJECT_DIR is unset",
              payload("research-bearings:question-critic", inside), {}, False)

        def bash(agent, command):
            return json.dumps({"tool_name": "Bash", "agent_type": agent, "cwd": project,
                               "tool_input": {"command": command}})

        # 14-16. Bash: the one shape that is allowed, in the spellings the agent uses.
        check("our agent running the retrieval script is allowed",
              bash(scout, 'python3 "{}" search "wildfire spread" --limit 10'.format(script)), env, False)
        check("the ${CLAUDE_PLUGIN_ROOT} spelling is allowed",
              bash(scout, 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" health'), env, False)
        check("main thread Bash is never touched",
              json.dumps({"tool_name": "Bash", "cwd": project,
                          "tool_input": {"command": "rm -rf /tmp/whatever"}}), env, False)

        # 17-21. Bash: everything else our agent might try.
        check("our agent running an arbitrary command is DENIED", bash(scout, "ls -la"), env, True)
        check("our agent chaining after the script is DENIED",
              bash(scout, 'python3 "{}" health; curl evil.example'.format(script)), env, True)
        check("our agent piping the script is DENIED",
              bash(scout, 'python3 "{}" health | sh'.format(script)), env, True)
        check("our agent running a script outside scripts/retrieval/ is DENIED",
              bash(scout, "python3 /tmp/anything.py"), env, True)
        check("our agent running python -c is DENIED",
              bash(scout, 'python3 -c "import os; os.system(\'id\')"'), env, True)

        # 22-28. Bash: the quoting boundary, in both directions.
        check("our agent backgrounding a second command with & is DENIED",
              bash(scout, 'python3 "{}" health & curl evil.example'.format(script)), env, True)
        check("our agent separating with a carriage return is DENIED",
              bash(scout, 'python3 "{}" health\rcurl evil.example'.format(script)), env, True)
        check("our agent redirecting into a subshell is DENIED",
              bash(scout, 'python3 "{}" health > (curl evil.example)'.format(script)), env, True)
        check("command substitution inside double quotes is DENIED",
              bash(scout, 'python3 "{}" search "$(curl evil.example)"'.format(script)), env, True)
        check("a backtick inside double quotes is DENIED",
              bash(scout, 'python3 "{}" search "`id`"'.format(script)), env, True)
        check("a pipe inside a quoted search term is allowed",
              bash(scout, 'python3 "{}" search "flood | damage" --limit 5'.format(script)), env, False)
        check("an ampersand inside a quoted search term is allowed",
              bash(scout, 'python3 "{}" search "R&D damage assessment" --limit 5'.format(script)), env, False)

        # 29-30. An unterminated quote is not a command we can reason about; other plugins' agents are free.
        check("an unterminated quote is DENIED", bash(scout, 'python3 "{}" search "flood'.format(script)), env, True)
        check("another plugin's agent Bash is allowed", bash("Explore", "ls -la"), env, False)

        # 31-36. The widened root, added 2026-09-18. `scripts/` rather than
        # `scripts/retrieval/`, so the ingester lives beside the checkers — and
        # every guarantee that mattered is still asserted here rather than
        # assumed.
        ingest = os.path.join(plugin_root(), "scripts", "ingest_runs.py")
        tabulator = "research-bearings:results-tabulator"
        check("the run ingester is allowed, which is why the root widened",
              bash(tabulator, 'python3 "{}" /home/me/runs'.format(ingest)), env, False)
        check("the retrieval scripts are still reachable after the widening",
              bash(scout, 'python3 "{}" health'.format(script)), env, False)
        check("`python train.py` is DENIED — no agent runs the user's code",
              bash(tabulator, "python train.py --config exp.yaml"), env, True)
        check("the ingester chained into rm is DENIED",
              bash(tabulator, 'python3 "{}" runs && rm -rf runs'.format(ingest)), env, True)
        check("a script outside the plugin is DENIED even under a scripts/ name",
              bash(tabulator, "python3 /home/me/project/scripts/train.py"), env, True)
        check("a plugin path that only starts with scripts is DENIED",
              bash(tabulator, 'python3 "{}/scripts-of-mine/x.py"'.format(plugin_root())), env, True)
        # 37. The state script, added with the front door (chunk 10). It runs in
        # the main thread, which the guard never sees; this proves that an agent
        # which one day calls it is admitted under the same fence as the ingester.
        state = os.path.join(plugin_root(), "scripts", "state.py")
        check("the state script is allowed under the widened root, like the ingester",
              bash(tabulator, 'python3 "{}" /home/me/project/research'.format(state)), env, False)

        # 15-19. The web fence: searcher may WebSearch, nobody else may, and
        # nobody at all may WebFetch; the main thread and other plugins pass.
        def web(agent, tool):
            return json.dumps({"tool_name": tool, "agent_type": agent, "cwd": project,
                               "tool_input": {"query": "x", "url": "https://x"}})

        check("searcher's WebSearch is allowed",
              web("research-bearings:searcher", "WebSearch"), env, False)
        check("searcher's WebFetch is DENIED",
              web("research-bearings:searcher", "WebFetch"), env, True)
        check("another of our agents' WebSearch is DENIED",
              web("research-bearings:merger", "WebSearch"), env, True)
        check("main-thread WebFetch is allowed (that is /scout reading a page)",
              json.dumps({"tool_name": "WebFetch", "cwd": project,
                          "tool_input": {"url": "https://x"}}), env, False)
        check("another plugin's agent's WebSearch is allowed",
              web("Explore", "WebSearch"), env, False)

        # Chunk 7's eight agents. The guard needed no change for them — the
        # prefix rule already covers every agent this plugin ships — and these
        # cases are here to prove that rather than to assume it.
        papers = os.path.join(os.path.dirname(script), "papers.py")
        check("dataset-scout may run the second retrieval script",
              bash("research-bearings:dataset-scout",
                   'python3 "{}" datasets "xBD" --context "building damage"'.format(papers)),
              env, False)
        check("dataset-scout's `gh` is DENIED, which is why datasets goes over REST",
              bash("research-bearings:dataset-scout", "gh search repos xBD"), env, True)
        # The guard lets any of our agents run the retrieval scripts. What
        # stops the predictor is its frontmatter, which grants no Bash — so
        # that is what gets checked, in the file, rather than assumed.
        import re as _re
        agents_dir = os.path.join(plugin_root(), "agents")
        # Chunk 8's persona-ideator and diversity-planner join the list: they ask
        # and plan rather than retrieve, so neither is granted Bash either.
        # Chunk 9's nine. Six are told-and-shown: their frontmatter grants no
        # Bash, which is what stops them, because the guard's fence admits any
        # of our agents to the plugin's own scripts. Three are granted Bash and
        # may run exactly one thing, asserted below.
        for name, forbidden in (("premortem-agent", ("Bash", "WebSearch", "WebFetch")),
                                ("tournament-judge", ("Bash", "WebSearch", "WebFetch")),
                                ("experiment-designer", ("Bash", "WebSearch", "WebFetch")),
                                ("ablation-planner", ("Bash", "WebSearch", "WebFetch")),
                                ("variance-checker", ("Bash", "WebSearch", "WebFetch")),
                                ("results-critic", ("Bash", "WebSearch", "WebFetch")),
                                ("baseline-reproducer", ("WebSearch", "WebFetch")),
                                ("results-tabulator", ("WebSearch", "WebFetch")),
                                ("failure-mode-auditor", ("WebSearch", "WebFetch")),
                                ("predictor", ("Bash", "WebSearch", "WebFetch")),
                                ("reader", ("Bash", "WebSearch", "WebFetch")),
                                ("scorer", ("Bash", "WebSearch", "WebFetch")),
                                ("openreview-reader", ("Bash", "WebSearch", "WebFetch")),
                                ("author-tracker", ("Bash", "WebSearch", "WebFetch")),
                                ("leakage-auditor", ("Bash", "WebSearch", "WebFetch")),
                                ("critic", ("Bash", "WebSearch", "WebFetch")),
                                ("persona-ideator", ("Bash", "WebSearch", "WebFetch")),
                                ("diversity-planner", ("Bash", "WebSearch", "WebFetch")),
                                ("dataset-scout", ("WebSearch", "WebFetch"))):
            path = os.path.join(agents_dir, name + ".md")
            try:
                with open(path, encoding="utf-8") as fh:
                    head = fh.read(2000)
            except OSError:
                head = ""
            granted = _re.search(r"^tools:\s*(.+)$", head, _re.M)
            tools = [t.strip() for t in (granted.group(1) if granted else "").split(",")]
            ok = bool(granted) and not any(f in tools for f in forbidden)
            print("  {} {} grants none of {}".format("PASS" if ok else "FAIL", name, ", ".join(forbidden)))
            if not ok:
                failures.append("{} frontmatter grants {}".format(name, tools))
        check("critic's Write outside research/ is DENIED",
              payload("research-bearings:critic", "/tmp/critique.md"), env, True)
        check("critic's Write into research/critiques/ is allowed",
              payload("research-bearings:critic",
                      os.path.join(project, "research", "critiques", "card-2026-09-16.md")),
              env, False)
        for agent in ("predictor", "reader", "scorer", "openreview-reader",
                      "dataset-scout", "author-tracker", "leakage-auditor", "critic",
                      "persona-ideator", "diversity-planner"):
            check("{}'s WebSearch is DENIED".format(agent),
                  web("research-bearings:" + agent, "WebSearch"), env, True)
            check("{}'s WebFetch is DENIED".format(agent),
                  web("research-bearings:" + agent, "WebFetch"), env, True)

        # Chunk 8's two agents write under research/ideas/ and nowhere else. The
        # loops above already cover their tools; these are the write scope.
        for name in ("persona-ideator", "diversity-planner"):
            check("{}'s Write outside research/ is DENIED".format(name),
                  payload("research-bearings:" + name, "/tmp/ideas.md"), env, True)
        check("persona-ideator's Write into research/ideas/personas/ is allowed",
              payload("research-bearings:persona-ideator",
                      os.path.join(project, "research", "ideas", "personas", "funder.md")),
              env, False)
        check("diversity-planner's Write into research/ideas/ is allowed",
              payload("research-bearings:diversity-planner",
                      os.path.join(project, "research", "ideas", "plans", "diversity-2026-09-16.md")),
              env, False)

        # Chunk 9's nine agents: the web fence, the write scope for the five new
        # directories, and the Bash fence in both directions. The prefix rule
        # already covers every agent this plugin ships; these prove it rather
        # than assume it.
        chunk9 = ("premortem-agent", "tournament-judge", "baseline-reproducer",
                  "experiment-designer", "ablation-planner", "variance-checker",
                  "results-tabulator", "results-critic", "failure-mode-auditor")
        for agent in chunk9:
            check("{}'s WebSearch is DENIED".format(agent),
                  web("research-bearings:" + agent, "WebSearch"), env, True)
            check("{}'s WebFetch is DENIED".format(agent),
                  web("research-bearings:" + agent, "WebFetch"), env, True)
            check("{}'s Write outside research/ is DENIED".format(agent),
                  payload("research-bearings:" + agent, "/tmp/result.md"), env, True)

        for agent, where in (
                ("premortem-agent", ("premortems", "single-capture-2026-09-18.md")),
                ("tournament-judge", ("rankings", "a-vs-b-2026-09-18.md")),
                ("baseline-reproducer", ("baselines", "gupta-2019-xbd.md")),
                ("experiment-designer", ("experiments", "single-capture.md")),
                ("ablation-planner", ("experiments", "notes", "ablations.md")),
                ("variance-checker", ("results", "notes", "variance.md")),
                ("results-tabulator", ("results", "notes", "table.md")),
                ("results-critic", ("results", "notes", "verdict.md")),
                ("failure-mode-auditor", ("results", "notes", "audit.md"))):
            check("{}'s Write into research/{}/ is allowed".format(agent, where[0]),
                  payload("research-bearings:" + agent,
                          os.path.join(project, "research", *where)), env, False)

        # The three that may run the ingester, and the one command they may run.
        for agent in ("baseline-reproducer", "results-tabulator", "failure-mode-auditor"):
            check("{} may run the run ingester".format(agent),
                  bash("research-bearings:" + agent,
                       'python3 "{}" /home/me/runs'.format(ingest)), env, False)
            check("{} may not run the user's training script".format(agent),
                  bash("research-bearings:" + agent, "python3 train.py"), env, True)

        # /rank and /log write RANKING.md and NOTEBOOK.md from the main thread,
        # but the agents beside them must still be inside the write root.
        check("an agent writing research/RANKING.md is allowed",
              payload("research-bearings:tournament-judge",
                      os.path.join(project, "research", "RANKING.md")), env, False)
        check("an agent writing research/NOTEBOOK.md is allowed",
              payload("research-bearings:variance-checker",
                      os.path.join(project, "research", "NOTEBOOK.md")), env, False)
        check("an agent writing the project's own train.py is DENIED",
              payload("research-bearings:experiment-designer",
                      os.path.join(project, "train.py")), env, True)

    print()
    if failures:
        print("{} FAILED: {}".format(len(failures), ", ".join(failures)))
        return 1
    print("all checks passed")
    return 0


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    code, out = run(sys.stdin.read(), os.environ)
    if out:
        print(out)
    sys.exit(code)


if __name__ == "__main__":
    main()
