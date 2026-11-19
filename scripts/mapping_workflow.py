"""Mapping workflow: freeze the gold standard, import agent proposals, review and score them.

    uv run python scripts/mapping_workflow.py freeze-gold --orcid 0000-0000-0000-0000 --name "Your Name"
    uv run python scripts/mapping_workflow.py import-proposals v1 --tool-version 2.1.328 --model claude-opus-5-5
    uv run python scripts/mapping_workflow.py review-sheet v1
    uv run python scripts/mapping_workflow.py review-sheet v2 --previous v1
    uv run python scripts/mapping_workflow.py apply-review v1 --orcid 0000-0000-0000-0000 --name "Your Name"
    uv run python scripts/mapping_workflow.py score v1
    uv run python scripts/mapping_workflow.py validate mapping/gold_standard.sssom.tsv

Files of run <v> live in mapping/runs/<v>/: the agent's proposals.tsv, then
proposals.sssom.tsv, review.tsv (filled in by the reviewer), reviewed.sssom.tsv,
score.json and errors.tsv.
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from pd_biomarker_model import mapping

ROOT = Path(__file__).resolve().parents[1]
MAPPING = ROOT / "mapping"
BASE = "https://w3id.org/pd-biomarker-model/mapping/"
DICTIONARY = MAPPING / "source_dictionary.tsv"
GOLD_REVIEW = MAPPING / "gold_standard_review.tsv"
GOLD = MAPPING / "gold_standard.sssom.tsv"
GOLD_DRAFT = {  # the session that drafted the gold standard on 2026-11-18
    "author_id": "pdbm:agent/gold-standard-draft",
    "author_label": "Gold-standard draft (Claude Code agent, claude-opus-5-5)",
    "mapping_tool": "Claude Code",
    "mapping_tool_version": "2.1.327 (claude-opus-5-5)",
    "mapping_date": "2026-11-18",
}


def person(args) -> dict:
    return {"id": f"orcid:{args.orcid}", "label": args.name}


def validate(path: Path) -> None:
    """Parse with sssom-py and run its JSON Schema, prefix and CURIE checks."""
    from sssom.constants import SchemaValidationType
    from sssom.parsers import parse_sssom_table
    from sssom.validators import validate as sssom_validate

    msdf = parse_sssom_table(path)
    sssom_validate(msdf, [SchemaValidationType.JsonSchema, SchemaValidationType.PrefixMapCompleteness,
                          SchemaValidationType.StrictCurieFormat], fail_on_error=True)
    print(f"{path.relative_to(ROOT)}: valid SSSOM, {len(msdf.df)} mappings")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("freeze-gold", "apply-review"):
        p = sub.add_parser(name)
        if name == "apply-review":
            p.add_argument("run")
        p.add_argument("--orcid", required=True, help="the reviewer's ORCID iD, e.g. 0000-0002-1825-0097")
        p.add_argument("--name", required=True)
        p.add_argument("--date", default=date.today().isoformat())
    p = sub.add_parser("import-proposals")
    p.add_argument("run")
    p.add_argument("--tool-version", required=True, help="Claude Code version that ran the agent")
    p.add_argument("--model", required=True)
    p.add_argument("--date", default=date.today().isoformat())
    p = sub.add_parser("review-sheet")
    p.add_argument("run")
    p.add_argument("--previous", help="an earlier run whose reviewed mappings also count as accepted")
    sub.add_parser("score").add_argument("run")
    sub.add_parser("validate").add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()

    if args.command == "freeze-gold":
        rows = mapping.freeze_gold_standard(mapping.read_tsv(GOLD_REVIEW), GOLD_DRAFT, person(args), args.date,
                                            mapping.read_tsv(DICTIONARY), mapping.term_label)
        mapping.write_sssom(GOLD, BASE + "gold_standard.sssom.tsv", "Gold-standard mapping of the source dictionary",
                            "Drafted by a Claude Code agent and reviewed row by row by a curator. The mappings "
                            "that hold are those without reviewer_agreement -1.0.", rows)
        validate(GOLD)
        return 0
    if args.command == "validate":
        for path in args.files:
            validate(path.resolve())
        return 0

    run = MAPPING / "runs" / args.run
    if args.command == "import-proposals":
        agent = {
            "author_id": f"pdbm:agent/mapping-agent-{args.run}",
            "author_label": f"Mapping agent {args.run} (Claude Code agent, {args.model})",
            "mapping_tool": "Claude Code",
            "mapping_tool_version": f"{args.tool_version} ({args.model})",
            "mapping_date": args.date,
        }
        rows = mapping.import_proposals(mapping.read_tsv(run / "proposals.tsv"), mapping.read_tsv(DICTIONARY), agent)
        mapping.write_sssom(run / "proposals.sssom.tsv", BASE + f"runs/{args.run}/proposals.sssom.tsv",
                            f"Mapping agent {args.run} proposals",
                            f"Unreviewed proposals of the mapping agent, prompt {args.run}.", rows)
        validate(run / "proposals.sssom.tsv")
    elif args.command == "review-sheet":
        gold = mapping.accepted(mapping.read_tsv(GOLD)) if GOLD.exists() else None
        previous = (mapping.accepted(mapping.read_tsv(MAPPING / "runs" / args.previous / "reviewed.sssom.tsv"))
                    if args.previous else None)
        sheet = mapping.review_sheet(mapping.read_tsv(run / "proposals.sssom.tsv"), mapping.read_tsv(DICTIONARY),
                                     gold, previous)
        mapping.write_tsv(run / "review.tsv", mapping.REVIEW_COLUMNS, sheet)
        todo = sum(not row["decision"] for row in sheet)
        print(f"{(run / 'review.tsv').relative_to(ROOT)}: {len(sheet)} proposals, {todo} to review")
    elif args.command == "apply-review":
        rows = mapping.apply_review(mapping.read_tsv(run / "proposals.sssom.tsv"), mapping.read_tsv(run / "review.tsv"),
                                    person(args), args.date, mapping.term_label)
        mapping.write_sssom(run / "reviewed.sssom.tsv", BASE + f"runs/{args.run}/reviewed.sssom.tsv",
                            f"Mapping agent {args.run} proposals, reviewed",
                            "Agent proposals with the curator's decisions (reviewer_agreement) and "
                            "curator-authored corrections.", rows)
        validate(run / "reviewed.sssom.tsv")
    elif args.command == "score":
        gold = mapping.accepted(mapping.read_tsv(GOLD))
        metrics, errors = mapping.score(mapping.read_tsv(run / "proposals.sssom.tsv"), gold, mapping.ontology_relation)
        (run / "score.json").write_text(json.dumps(metrics, indent=2) + "\n")
        mapping.write_tsv(run / "errors.tsv", mapping.ERROR_COLUMNS, errors)
        print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
