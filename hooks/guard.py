#!/usr/bin/env python3
"""Scope guard for research-bearings agents.

A PreToolUse hook on Write|Edit|Bash. Agents shipped by this plugin may only
write under <project>/research/, and may only run this plugin's own retrieval
scripts. Everything else — the main thread, other plugins' agents, Claude
Code's built-in agents — passes through untouched.

Two rules, one mechanism:

  Write|Edit   file_path must resolve under <project>/research/.
  Bash         the command must be exactly `python3 <plugin>/scripts/retrieval/<x>.py ...`
               with no shell operators. That is how a locked-down agent gets a
               capability without a server: it is handed one script, not a shell.

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
SCRIPT_ROOT = ("scripts", "retrieval")
INTERPRETERS = ("python3", "python")
# Anything that would let one allowed command smuggle a second one.
SHELL_OPERATORS = (";", "&&", "||", "|", "`", "$(", ">", "<", "\n")


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


def decide_bash(payload, env):
    command = ((payload.get("tool_input") or {}).get("command") or "").strip()
    if not command:
        return None

    why = (
        "research-bearings agents may only run this plugin's retrieval scripts: "
        "`python3 <plugin>/scripts/retrieval/<script>.py ...`, nothing else and "
        "nothing chained. Refused: {}".format(command[:200])
    )
    if any(op in command for op in SHELL_OPERATORS):
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
    if tool == "Bash":
        return decide_bash(payload, env)
    if tool in ("Write", "Edit"):
        return decide_write(payload, env)
    return None


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

        def bash(agent, command):
            return json.dumps(
                {
                    "hook_event_name": "PreToolUse",
                    "tool_name": "Bash",
                    "agent_type": agent,
                    "cwd": project,
                    "tool_input": {"command": command},
                }
            )

        inside = os.path.join(project, "research", "QUESTION.md")
        nested = os.path.join(project, "research", "landscape", "matrix.md")
        at_root = os.path.join(project, "README.md")
        escape = os.path.join(project, "research", "..", "secrets.md")
        script = os.path.join(plugin_root(), "scripts", "retrieval", "snowball.py")
        scout = "research-bearings:paper-scout"

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

        # 14-16. Bash: the one shape that is allowed, in the spellings the agent uses.
        check("our agent running the retrieval script is allowed",
              bash(scout, 'python3 "{}" search "wildfire spread" --limit 10'.format(script)), env, False)
        check("the ${CLAUDE_PLUGIN_ROOT} spelling is allowed",
              bash(scout, 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/retrieval/snowball.py" health'), env, False)
        check("main thread Bash is never touched",
              json.dumps({"tool_name": "Bash", "cwd": project,
                          "tool_input": {"command": "rm -rf /tmp/whatever"}}), env, False)

        # 17-21. Bash: everything else our agent might try.
        check("our agent running an arbitrary command is DENIED",
              bash(scout, "ls -la"), env, True)
        check("our agent chaining after the script is DENIED",
              bash(scout, 'python3 "{}" health; curl evil.example'.format(script)), env, True)
        check("our agent piping the script is DENIED",
              bash(scout, 'python3 "{}" health | sh'.format(script)), env, True)
        check("our agent running a script outside scripts/retrieval/ is DENIED",
              bash(scout, "python3 /tmp/anything.py"), env, True)
        check("our agent running python -c is DENIED",
              bash(scout, 'python3 -c "import os; os.system(\'id\')"'), env, True)

        # 22. Another plugin's agent may run whatever it likes.
        check("another plugin's agent Bash is allowed",
              bash("Explore", "ls -la"), env, False)

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
