"""Audit a mapping-agent run from its Claude Code transcript.

    uv run python scripts/check_agent_transcript.py <agent transcript .jsonl> <workspace> mapping/runs/v1

Writes <run>/tool_calls.tsv, one row per tool call the agent made (tool and
command or path), and <run>/blindness_check.txt. The check fails if any call
reads, lists or searches outside the workspace, or names the repository or
the gold standard. Absolute paths in shell commands must be inside the
workspace or be the project's Python interpreter.
"""

import csv
import json
import re
import sys
from pathlib import Path

FORBIDDEN = ("gold_standard", "pd-biomarker-model", "GitHub_portfolio_fixes", ".claude/projects")
ABSOLUTE_PATH = re.compile(r"""(?:^|[\s"'=])((?:/|~/)[^\s"';|&<>()]+)""")
ALLOWED = (str(Path(sys.executable).parent), "/dev/null")


def tool_calls(transcript: Path):
    for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        message = record.get("message")
        if record.get("type") != "assistant" or not isinstance(message, dict):
            continue
        for block in message.get("content") or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield record.get("timestamp", ""), block.get("name", ""), block.get("input") or {}


def describe(tool: str, args: dict) -> str:
    for key in ("command", "file_path", "path", "pattern", "notebook_path", "url"):
        if key in args:
            extra = f" in {args['path']}" if key == "pattern" and "path" in args else ""
            return f"{args[key]}{extra}"
    return json.dumps(args)[:300]


def problems(tool: str, args: dict, workspace: str) -> list[str]:
    text = json.dumps(args)
    for allowed in ALLOWED:  # the interpreter's own path may contain the project name
        text = text.replace(allowed, "")
    found = [f"names {word!r}" for word in FORBIDDEN if word in text]
    for key in ("file_path", "path", "notebook_path"):
        value = args.get(key)
        if value and not str(value).startswith(workspace):
            found.append(f"{key} outside the workspace: {value}")
    for path in ABSOLUTE_PATH.findall(str(args.get("command", ""))):
        if not path.startswith((workspace, *ALLOWED)):
            found.append(f"command uses a path outside the workspace: {path}")
    if tool in ("Glob", "Grep") and "path" not in args:
        found.append("search without a path (defaults to the session folder)")
    return found


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    transcript, workspace, run = Path(sys.argv[1]), str(Path(sys.argv[2]).resolve()), Path(sys.argv[3])
    run.mkdir(parents=True, exist_ok=True)
    rows, flagged = [], []
    for timestamp, tool, args in tool_calls(transcript):
        issues = problems(tool, args, workspace)
        call = describe(tool, args).replace(workspace, "<workspace>")
        rows.append({"timestamp": timestamp, "tool": tool, "call": " ".join(call.split()), "flag": "; ".join(issues)})
        if issues:
            flagged.append(rows[-1])
    with (run / "tool_calls.tsv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, ["timestamp", "tool", "call", "flag"], delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    verdict = "PASS" if not flagged else "FAIL"
    lines = [f"Blindness check: {verdict}", f"Tool calls: {len(rows)}",
             f"Calls outside the workspace or naming the repository or gold standard: {len(flagged)}"]
    lines += [f"  {r['tool']}: {r['call']} ({r['flag']})" for r in flagged]
    (run / "blindness_check.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if not flagged else 1


if __name__ == "__main__":
    sys.exit(main())
