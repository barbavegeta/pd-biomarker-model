"""The agent-run audit flags any access outside the workspace."""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_agent_transcript", ROOT / "scripts" / "check_agent_transcript.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def transcript(tmp_path, calls):
    lines = [json.dumps({"type": "assistant", "timestamp": f"t{i}", "message": {"content": [
        {"type": "tool_use", "name": tool, "input": args}]}}) for i, (tool, args) in enumerate(calls)]
    path = tmp_path / "agent.jsonl"
    path.write_text("\n".join(lines))
    return path


def run(tmp_path, calls):
    workspace = tmp_path / "ws"
    workspace.mkdir()
    out = tmp_path / "run"
    sys.argv = ["check", str(transcript(tmp_path, calls(str(workspace)))), str(workspace), str(out)]
    return check.main(), (out / "blindness_check.txt").read_text()


def test_workspace_only_run_passes(tmp_path):
    python = sys.executable
    code, report = run(tmp_path, lambda ws: [
        ("Read", {"file_path": f"{ws}/source_dictionary.tsv"}),
        ("Bash", {"command": f'cd {ws} && {python} search_terms.py search "tremor" --in hp 2>/dev/null'}),
        ("Write", {"file_path": f"{ws}/proposals.tsv", "content": "x"}),
    ])
    assert code == 0 and report.startswith("Blindness check: PASS")


def test_access_outside_the_workspace_fails(tmp_path):
    code, report = run(tmp_path, lambda ws: [
        ("Read", {"file_path": "/mnt/d/GitHub_portfolio_fixes/pd-biomarker-model/mapping/gold_standard_review.tsv"}),
        ("Bash", {"command": "ls /home/someone/projects"}),
        ("Grep", {"pattern": "NoTermFound"}),
    ])
    assert code == 1
    assert "Calls outside the workspace or naming the repository or gold standard: 3" in report
