"""Plot the mapping agent's scores for each run.

    uv run --group figures python scripts/plot_mapping_scores.py docs/img/mapping-scores.png --title "..."

Reads mapping/runs/<version>/score.json and reviewed.sssom.tsv for every run
and draws one row per metric, one marker per run, with the values printed
beside the plot. Colours follow the portfolio site's chart style.
"""

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from pd_biomarker_model import mapping  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "mapping" / "runs"
INK, MUTED, GRID = "#383028", "#6b6150", "#e4dcd2"
STYLES = [  # earlier runs muted and hollow, the latest run in the accent colour
    {"color": "#9d9179", "marker": "D", "mfc": "white", "ms": 9},
    {"color": "#0b6e66", "marker": "o", "mfc": "#0b6e66", "ms": 9},
]
METRICS = [
    ("precision", "Precision", "proposed terms that are the gold term"),
    ("recall", "Recall", "gold terms the agent found"),
    ("fully_correct", "Fully correct", "term and predicate, all 68 variables"),
    ("accepted", "Accepted by the curator", "proposals accepted in review"),
]


def run_scores(run: Path) -> dict:
    scores = json.loads((run / "score.json").read_text())
    reviewed = run / "reviewed.sssom.tsv"
    if reviewed.exists():
        rows = mapping.read_tsv(reviewed)
        agent = [r for r in rows if r["curator_type"] == "AI_AGENT"]
        scores["accepted"] = round(sum(r["reviewer_agreement"] == "1.0" for r in agent) / len(agent), 3)
    return scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    runs = sorted(p for p in RUNS.iterdir() if (p / "score.json").exists())
    scores = {run.name: run_scores(run) for run in runs}
    styles = STYLES[-len(runs):] if len(runs) <= len(STYLES) else STYLES

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 13, "text.color": INK})
    fig, ax = plt.subplots(figsize=(9, 5.0625), dpi=160)
    rows = list(range(len(METRICS)))[::-1]
    offsets = [0.12 * (i - (len(runs) - 1) / 2) for i in range(len(runs))]
    for (name, s), style, off in zip(scores.items(), styles, offsets):
        xs = [s.get(key) for key, _, _ in METRICS]
        ys = [r + off for r in rows]
        pts = [(x, y) for x, y in zip(xs, ys) if x is not None]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], linestyle="none", marker=style["marker"],
                markersize=style["ms"], markerfacecolor=style["mfc"], markeredgecolor=style["color"],
                markeredgewidth=2, label=f"Prompt {name}", zorder=3)

    ax.set_yticks(rows)
    ax.set_yticklabels([label for _, label, _ in METRICS], fontsize=14, color=INK)
    for r, (_, _, note) in zip(rows, METRICS):
        ax.text(-0.01, r - 0.3, note, transform=ax.get_yaxis_transform(), ha="right", va="center",
                fontsize=10, color=MUTED)
    ax.set_xlim(0.75, 1.0)
    ax.set_ylim(-0.6, len(METRICS) - 0.4)
    ax.set_xticks([0.75, 0.8, 0.85, 0.9, 0.95, 1.0])
    ax.grid(axis="x", color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="x", colors=MUTED, labelsize=12)
    ax.tick_params(axis="y", length=0, pad=12)
    ax.set_xlabel("Share. The first three use the gold standard frozen before the agent ran.", color=MUTED,
                  fontsize=12)

    # value columns to the right of the plot
    for i, (name, s) in enumerate(scores.items()):
        x = 1.04 + 0.17 * i
        ax.text(x, len(METRICS) - 0.45, name, transform=ax.get_yaxis_transform(), ha="left",
                fontsize=11, color=MUTED)
        for r, (key, _, _) in zip(rows, METRICS):
            value = s.get(key)
            ax.text(x, r, "" if value is None else f"{value:.3f}", transform=ax.get_yaxis_transform(),
                    ha="left", va="center", fontsize=13, color=INK if i == len(scores) - 1 else MUTED)

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=len(runs), frameon=False, fontsize=12,
              handletextpad=0.4, columnspacing=1.6)
    fig.suptitle(args.title, fontsize=17, fontweight="bold", color=INK, y=0.985)
    fig.subplots_adjust(left=0.33, right=0.74, top=0.82, bottom=0.14)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, facecolor="white")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
