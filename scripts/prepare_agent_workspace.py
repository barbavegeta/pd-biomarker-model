"""Set up an isolated workspace for one run of the mapping agent.

    uv run python scripts/prepare_agent_workspace.py v1 ~/portfolio_work/mapping-agent/v1

The workspace receives only what the agent may see: the source dictionary,
the curation guidelines and the search tool. It must be a new folder outside
the repository, so the gold standard is not within reach. The script fills
the workspace path and the Python interpreter into mapping/agent/prompt_<v>.md
and writes the result to <workspace>/prompt.md; that text is the prompt the
agent is given.
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = [
    ROOT / "mapping" / "source_dictionary.tsv",
    ROOT / "docs" / "curation-guidelines.md",
    ROOT / "scripts" / "search_terms.py",
]


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    version, workspace = sys.argv[1], Path(sys.argv[2]).expanduser().resolve()
    template = ROOT / "mapping" / "agent" / f"prompt_{version}.md"
    if not template.exists():
        sys.exit(f"No prompt for version {version}: {template} is missing")
    if workspace == ROOT or ROOT in workspace.parents:
        sys.exit("The workspace must be outside the repository")
    if workspace.exists() and any(workspace.iterdir()):
        sys.exit(f"{workspace} is not empty; use a new folder for each run")

    workspace.mkdir(parents=True, exist_ok=True)
    for path in INPUTS:
        shutil.copy2(path, workspace / path.name)
    python = Path(sys.executable)  # the project interpreter, which has oaklib
    prompt = template.read_text().replace("{workspace}", str(workspace)).replace("{python}", str(python))
    (workspace / "prompt.md").write_text(prompt)
    print(f"Workspace ready: {workspace}")
    for path in sorted(workspace.iterdir()):
        print(f"  {path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
