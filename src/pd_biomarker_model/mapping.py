"""SSSOM mapping sets for the source dictionary: gold standard, agent proposals, review and scoring.

Every mapping set is written as SSSOM/TSV. A review never overwrites a
mapping: it adds `reviewer_id` and `reviewer_agreement` (1.0 accept, -1.0
reject), and a correction adds a new mapping authored by the reviewer. The
mappings that hold after review are those not rejected; `accepted()` returns
them, one per source variable.
"""

from __future__ import annotations

import csv
from pathlib import Path

NO_TERM = "sssom:NoTermFound"
PREDICATES = ("skos:exactMatch", "skos:broadMatch", "skos:narrowMatch", "skos:relatedMatch")
DECISIONS = ("ACCEPT", "CHANGE", "REJECT")
AGENT_JUSTIFICATION = "semapv:CompositeMatching"
PERSON_JUSTIFICATION = "semapv:ManualMappingCuration"

CURIE_MAP = {
    "HP": "http://purl.obolibrary.org/obo/HP_",
    "LOINC": "https://loinc.org/",
    "MONDO": "http://purl.obolibrary.org/obo/MONDO_",
    "NCIT": "http://purl.obolibrary.org/obo/NCIT_",
    "OBI": "http://purl.obolibrary.org/obo/OBI_",
    "PATO": "http://purl.obolibrary.org/obo/PATO_",
    "STATO": "http://purl.obolibrary.org/obo/STATO_",
    "UBERON": "http://purl.obolibrary.org/obo/UBERON_",
    "UO": "http://purl.obolibrary.org/obo/UO_",
    "orcid": "https://orcid.org/",
    "pdbm": "https://w3id.org/pd-biomarker-model/",
    "src": "https://w3id.org/pd-biomarker-model/source/",
}
COLUMNS = [
    "subject_id", "subject_label", "predicate_id", "object_id", "object_label",
    "mapping_justification", "author_id", "author_label", "reviewer_id", "reviewer_label",
    "reviewer_agreement", "confidence", "mapping_tool", "mapping_tool_version",
    "mapping_date", "comment", "curator_type",
]
EXTENSIONS = """#extension_definitions:
#  - slot_name: curator_type
#    property: pdbm:curator_type
#    type_hint: xsd:string
"""


def _row(values: dict) -> dict:
    """A mapping row with every SSSOM column, empty where not used."""
    return {column: str(values.get(column, "")) for column in COLUMNS}


def read_tsv(path: Path) -> list[dict]:
    """Rows of a TSV file, skipping SSSOM `#` metadata lines."""
    with Path(path).open(encoding="utf-8") as fh:
        lines = [line for line in fh if not line.startswith("#")]
    return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(lines, delimiter="\t")]


def write_tsv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, columns, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_sssom(path: Path, mapping_set_id: str, title: str, description: str, rows: list[dict]) -> None:
    """Write SSSOM/TSV with a metadata block; columns that are empty in every row are left out."""
    columns = [c for c in COLUMNS if any(str(row.get(c, "")) for row in rows)]
    used = {value.split(":", 1)[0] for row in rows for c in ("subject_id", "object_id", "author_id", "reviewer_id")
            for value in str(row.get(c, "")).split("|") if ":" in value}
    curie_map = {p: CURIE_MAP[p] for p in sorted(used) if p in CURIE_MAP}
    curie_map.setdefault("pdbm", CURIE_MAP["pdbm"])  # the curator_type extension property
    header = "#curie_map:\n" + "".join(f"#  {p}: {u}\n" for p, u in curie_map.items())
    header += (
        f"#mapping_set_id: {mapping_set_id}\n"
        f"#mapping_set_title: {title}\n"
        f"#mapping_set_description: {description}\n"
        "#license: https://spdx.org/licenses/MIT\n"
    )
    if "curator_type" in columns:
        header += EXTENSIONS
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        fh.write(header)
        writer = csv.DictWriter(fh, columns, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _check_mapping(subject: str, predicate: str, obj: str) -> None:
    if predicate not in PREDICATES:
        raise ValueError(f"{subject}: predicate {predicate!r} is not one of {', '.join(PREDICATES)}")
    if obj == NO_TERM and predicate != "skos:exactMatch":
        raise ValueError(f"{subject}: {NO_TERM} must use skos:exactMatch")
    if obj != NO_TERM and (":" not in obj or obj.split(":", 1)[0] not in CURIE_MAP):
        raise ValueError(f"{subject}: object {obj!r} is not a CURIE with a known prefix")


def freeze_gold_standard(review_rows: list[dict], draft: dict, reviewer: dict, date: str,
                         dictionary: list[dict] | None = None, lookup_label=None) -> list[dict]:
    """Gold-standard mappings from the reviewed draft.

    `draft` describes the drafting agent (author_id, author_label,
    mapping_tool, mapping_tool_version, mapping_date); `reviewer` the person
    (id as an ORCID CURIE, label). Every row must carry ACCEPT, CHANGE or
    REJECT. CHANGE gives a corrected term and/or predicate; REJECT means no
    term applies. Draft rows keep their original values; rejected or changed
    ones get agreement -1.0 and a reviewer-authored replacement. With a
    `dictionary`, the review must cover exactly its variables.
    `lookup_label(curie)`, if given, fills in the label of a corrected term.
    """
    if dictionary is not None:
        expected = [r["variable_id"] for r in dictionary]
        if [r["variable_id"] for r in review_rows] != expected:
            raise ValueError("The review must have one row per dictionary variable, in dictionary order")
    out = []
    for row in review_rows:
        subject, decision = row["variable_id"], row["decision"].upper()
        if decision not in DECISIONS:
            raise ValueError(f"{subject}: decision {row['decision']!r} must be one of {', '.join(DECISIONS)}")
        _check_mapping(subject, row["predicate_id"], row["object_id"])
        drafted = {
            "subject_id": subject, "subject_label": row["variable_name"],
            "predicate_id": row["predicate_id"], "object_id": row["object_id"],
            "object_label": row["object_label"] if row["object_id"] != NO_TERM else "",
            "mapping_justification": AGENT_JUSTIFICATION,
            "author_id": draft["author_id"], "author_label": draft["author_label"],
            "mapping_tool": draft["mapping_tool"], "mapping_tool_version": draft["mapping_tool_version"],
            "mapping_date": draft["mapping_date"], "comment": row["rationale"], "curator_type": "AI_AGENT",
            "reviewer_id": reviewer["id"], "reviewer_label": reviewer["label"],
            "reviewer_agreement": "1.0" if decision == "ACCEPT" else "-1.0",
        }
        out.append(_row(drafted))
        if decision == "ACCEPT":
            continue
        if decision == "CHANGE":
            obj = row.get("corrected_object_id", "") or row["object_id"]
            predicate = row.get("corrected_predicate_id", "") or row["predicate_id"]
            if (obj, predicate) == (row["object_id"], row["predicate_id"]):
                raise ValueError(f"{subject}: CHANGE needs a corrected term or predicate")
            label = row["object_label"] if obj == row["object_id"] else (lookup_label(obj) if lookup_label else "")
        else:
            obj, predicate, label = NO_TERM, "skos:exactMatch", ""
        _check_mapping(subject, predicate, obj)
        out.append(_row({
            "subject_id": subject, "subject_label": row["variable_name"],
            "predicate_id": predicate, "object_id": obj, "object_label": label,
            "mapping_justification": PERSON_JUSTIFICATION,
            "author_id": reviewer["id"], "author_label": reviewer["label"],
            "mapping_date": date, "comment": row.get("reviewer_note", ""), "curator_type": "PERSON",
        }))
    return out


def import_proposals(proposal_rows: list[dict], dictionary: list[dict], agent: dict) -> list[dict]:
    """Agent proposals as SSSOM rows, checked against the source dictionary.

    `agent` gives author_id, author_label, mapping_tool, mapping_tool_version
    and mapping_date for the run.
    """
    expected = [row["variable_id"] for row in dictionary]
    found = [row["subject_id"] for row in proposal_rows]
    if sorted(found) != sorted(expected) or len(set(found)) != len(found):
        missing = sorted(set(expected) - set(found))
        extra = sorted(set(found) - set(expected))
        raise ValueError(f"Need one proposal per variable; missing {missing}, unexpected {extra}")
    names = {row["variable_id"]: row["variable_name"] for row in dictionary}
    out = []
    for row in proposal_rows:
        subject = row["subject_id"]
        _check_mapping(subject, row["predicate_id"], row["object_id"])
        confidence = float(row["confidence"])
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"{subject}: confidence {confidence} is outside 0-1")
        out.append(_row({
            "subject_id": subject, "subject_label": names[subject],
            "predicate_id": row["predicate_id"], "object_id": row["object_id"],
            "object_label": row["object_label"] if row["object_id"] != NO_TERM else "",
            "mapping_justification": AGENT_JUSTIFICATION,
            "author_id": agent["author_id"], "author_label": agent["author_label"],
            "confidence": f"{confidence:.2f}",
            "mapping_tool": agent["mapping_tool"], "mapping_tool_version": agent["mapping_tool_version"],
            "mapping_date": agent["mapping_date"], "comment": row.get("comment", ""), "curator_type": "AI_AGENT",
        }))
    order = {s: i for i, s in enumerate(expected)}
    return sorted(out, key=lambda r: order[r["subject_id"]])


def accepted(rows: list[dict]) -> dict[str, dict]:
    """The mapping that holds for each subject: rows a reviewer did not reject."""
    held = {}
    for row in rows:
        if row.get("reviewer_agreement") in ("-1.0", "-1"):
            continue
        if row["subject_id"] in held:
            raise ValueError(f"{row['subject_id']} has more than one accepted mapping")
        held[row["subject_id"]] = row
    return held


REVIEW_COLUMNS = [
    "subject_id", "variable_name", "description", "unit", "object_id", "object_label",
    "predicate_id", "confidence", "agent_comment", "matches_gold_standard",
    "decision", "corrected_object_id", "corrected_object_label", "corrected_predicate_id", "reviewer_note",
]


def review_sheet(proposals: list[dict], dictionary: list[dict], gold: dict[str, dict] | None) -> list[dict]:
    """A sheet for reviewing agent proposals. Where a gold standard is given, a
    proposal identical to it (term and predicate) is pre-filled ACCEPT."""
    info = {row["variable_id"]: row for row in dictionary}
    sheet = []
    for row in proposals:
        variable = info[row["subject_id"]]
        same = None
        if gold is not None:
            g = gold[row["subject_id"]]
            same = (row["object_id"], row["predicate_id"]) == (g["object_id"], g["predicate_id"])
        sheet.append(dict.fromkeys(REVIEW_COLUMNS, "") | {
            "subject_id": row["subject_id"], "variable_name": variable["variable_name"],
            "description": variable["description"], "unit": variable["unit"],
            "object_id": row["object_id"], "object_label": row["object_label"],
            "predicate_id": row["predicate_id"], "confidence": row["confidence"],
            "agent_comment": row["comment"],
            "matches_gold_standard": "" if same is None else ("yes" if same else "no"),
            "decision": "ACCEPT" if same else "",
            "reviewer_note": "Same as the gold standard." if same else "",
        })
    return sheet


def apply_review(proposals: list[dict], sheet: list[dict], reviewer: dict, date: str,
                 lookup_label=None) -> list[dict]:
    """Proposals with the reviewer's decisions recorded, plus reviewer-authored corrections."""
    decisions = {row["subject_id"]: row for row in sheet}
    out = []
    for row in proposals:
        review = decisions[row["subject_id"]]
        decision = review["decision"].upper()
        if decision not in DECISIONS:
            raise ValueError(f"{row['subject_id']}: decision {review['decision']!r} must be one of {', '.join(DECISIONS)}")
        reviewed = dict(row, reviewer_id=reviewer["id"], reviewer_label=reviewer["label"],
                        reviewer_agreement="1.0" if decision == "ACCEPT" else "-1.0")
        out.append(_row(reviewed))
        if decision == "ACCEPT":
            continue
        if decision == "CHANGE":
            obj = review.get("corrected_object_id", "") or row["object_id"]
            predicate = review.get("corrected_predicate_id", "") or row["predicate_id"]
            label = review.get("corrected_object_label", "")
            if not label:
                label = row["object_label"] if obj == row["object_id"] else (lookup_label(obj) if lookup_label else "")
        else:
            obj, predicate, label = NO_TERM, "skos:exactMatch", ""
        _check_mapping(row["subject_id"], predicate, obj)
        out.append(_row({
            "subject_id": row["subject_id"], "subject_label": row["subject_label"],
            "predicate_id": predicate, "object_id": obj, "object_label": label,
            "mapping_justification": PERSON_JUSTIFICATION,
            "author_id": reviewer["id"], "author_label": reviewer["label"],
            "mapping_date": date, "comment": review.get("reviewer_note", ""), "curator_type": "PERSON",
        }))
    return out


def _ratio(numerator: int, denominator: int) -> float | None:
    return round(numerator / denominator, 3) if denominator else None


def score(proposals: list[dict], gold: dict[str, dict], relation=None) -> tuple[dict, list[dict]]:
    """Score agent proposals against the gold standard.

    - precision: share of proposed terms that are the gold term;
    - recall: share of gold terms the agent proposed;
    - predicate agreement: share of correct terms with the gold predicate;
    - no-term agreement: share of gold `NoTermFound` rows where the agent also
      proposed no term.

    Each disagreement gets an error type. `relation(a, b)`, if given, returns
    "ancestor" or "descendant" when term a is above or below term b in its
    ontology, which separates too-broad and too-narrow terms from wrong ones.
    """
    agent = {row["subject_id"]: row for row in proposals}
    if set(agent) != set(gold):
        raise ValueError("Proposals and gold standard cover different variables")
    proposed = {s for s, r in agent.items() if r["object_id"] != NO_TERM}
    mapped = {s for s, r in gold.items() if r["object_id"] != NO_TERM}
    correct = {s for s in proposed & mapped if agent[s]["object_id"] == gold[s]["object_id"]}
    same_predicate = {s for s in correct if agent[s]["predicate_id"] == gold[s]["predicate_id"]}
    no_term = set(gold) - mapped
    both_no_term = no_term - proposed
    precision, recall = _ratio(len(correct), len(proposed)), _ratio(len(correct), len(mapped))
    f1 = round(2 * precision * recall / (precision + recall), 3) if precision and recall else None

    errors, confidence = [], {"right": [], "wrong": []}
    for s in sorted(gold):
        a, g = agent[s], gold[s]
        right = s in same_predicate or s in both_no_term
        if a.get("confidence"):
            confidence["right" if right else "wrong"].append(float(a["confidence"]))
        if right:
            continue
        if a["object_id"] == NO_TERM:
            kind = "missed"
        elif g["object_id"] == NO_TERM:
            kind = "spurious"
        elif a["object_id"] == g["object_id"]:
            kind = "wrong predicate"
        elif a["object_id"].split(":")[0] != g["object_id"].split(":")[0]:
            kind = "wrong ontology"
        else:
            kind = {"ancestor": "too broad", "descendant": "too narrow"}.get(
                relation(a["object_id"], g["object_id"]) if relation else None, "wrong term")
        errors.append({
            "subject_id": s, "subject_label": a["subject_label"], "error_type": kind,
            "agent_object_id": a["object_id"], "agent_object_label": a["object_label"],
            "agent_predicate_id": a["predicate_id"], "agent_confidence": a.get("confidence", ""),
            "gold_object_id": g["object_id"], "gold_object_label": g["object_label"],
            "gold_predicate_id": g["predicate_id"], "agent_comment": a.get("comment", ""), "note": "",
        })

    def mean(values):
        return round(sum(values) / len(values), 3) if values else None

    metrics = {
        "variables": len(gold),
        "gold_mapped": len(mapped),
        "gold_no_term": len(no_term),
        "agent_proposed": len(proposed),
        "correct_terms": len(correct),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "predicate_agreement": _ratio(len(same_predicate), len(correct)),
        "no_term_agreement": _ratio(len(both_no_term), len(no_term)),
        "fully_correct": _ratio(len(same_predicate) + len(both_no_term), len(gold)),
        "mean_confidence_correct": mean(confidence["right"]),
        "mean_confidence_wrong": mean(confidence["wrong"]),
        "errors_by_type": {k: sum(e["error_type"] == k for e in errors) for k in sorted({e["error_type"] for e in errors})},
    }
    return metrics, errors


ERROR_COLUMNS = [
    "subject_id", "subject_label", "error_type", "agent_object_id", "agent_object_label",
    "agent_predicate_id", "agent_confidence", "gold_object_id", "gold_object_label",
    "gold_predicate_id", "agent_comment", "note",
]


def term_label(curie: str) -> str:
    """Current label of a term: LOINC from the FHIR terminology server, others from local oaklib databases."""
    prefix, local = curie.split(":", 1)
    if prefix == "LOINC":
        import json
        import urllib.parse
        import urllib.request

        query = urllib.parse.urlencode({"system": "http://loinc.org", "code": local})
        request = urllib.request.Request(f"https://tx.fhir.org/r4/CodeSystem/$lookup?{query}",
                                         headers={"Accept": "application/fhir+json"})
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.load(response)
        return next((p["valueString"] for p in data.get("parameter", []) if p["name"] == "display"), "")
    from oaklib import get_adapter

    return get_adapter(f"sqlite:obo:{prefix.lower()}").label(curie) or ""


def ontology_relation(a: str, b: str) -> str | None:
    """'ancestor' if a is above b, 'descendant' if below, in a local oaklib ontology; else None."""
    prefix = a.split(":")[0]
    if prefix != b.split(":")[0] or prefix in ("LOINC", "sssom"):
        return None
    from oaklib import get_adapter

    oak = get_adapter(f"sqlite:obo:{prefix.lower()}")
    if a in set(oak.ancestors(b, predicates=["rdfs:subClassOf"], reflexive=False)):
        return "ancestor"
    if b in set(oak.ancestors(a, predicates=["rdfs:subClassOf"], reflexive=False)):
        return "descendant"
    return None
