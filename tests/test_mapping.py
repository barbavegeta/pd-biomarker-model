"""Gold-standard freezing, proposal import, review and scoring of SSSOM mapping sets."""

from pathlib import Path

import pytest
from sssom.constants import SchemaValidationType
from sssom.parsers import parse_sssom_table
from sssom.validators import validate

from pd_biomarker_model import mapping

ROOT = Path(__file__).resolve().parents[1]
REVIEWER = {"id": "orcid:0000-0002-1825-0097", "label": "Test Curator"}
DRAFT = {"author_id": "pdbm:agent/gold-standard-draft", "author_label": "draft agent",
         "mapping_tool": "Claude Code", "mapping_tool_version": "test", "mapping_date": "2026-11-18"}
AGENT = dict(DRAFT, author_id="pdbm:agent/mapping-agent-test", author_label="test agent")
DICTIONARY = [
    {"variable_id": f"src:V00{i}", "variable_name": name, "description": name, "unit": ""}
    for i, name in enumerate(["rest tremor", "MoCA total", "plate", "UPSIT"], start=1)
]


def gold_row(i, obj, predicate, decision, corrected_object="", corrected_predicate=""):
    return {
        "variable_id": f"src:V00{i}", "variable_name": DICTIONARY[i - 1]["variable_name"],
        "object_id": obj, "object_label": "" if obj == mapping.NO_TERM else f"label {obj}",
        "predicate_id": predicate, "rationale": "draft", "decision": decision,
        "corrected_object_id": corrected_object, "corrected_predicate_id": corrected_predicate,
        "reviewer_note": "",
    }


GOLD_REVIEW = [
    gold_row(1, "HP:0002322", "skos:exactMatch", "ACCEPT"),
    gold_row(2, "LOINC:72172-0", "skos:broadMatch", "CHANGE", corrected_predicate="skos:exactMatch"),
    gold_row(3, "NCIT:C25364", "skos:exactMatch", "REJECT"),
    gold_row(4, mapping.NO_TERM, "skos:exactMatch", "ACCEPT"),
]


def proposal(i, obj, predicate, confidence):
    return {"subject_id": f"src:V00{i}", "predicate_id": predicate, "object_id": obj,
            "object_label": "" if obj == mapping.NO_TERM else f"label {obj}",
            "confidence": str(confidence), "comment": "test"}


PROPOSALS = [
    proposal(1, "HP:0002322", "skos:exactMatch", 0.9),
    proposal(2, "LOINC:72172-0", "skos:broadMatch", 0.6),
    proposal(3, "NCIT:C25364", "skos:exactMatch", 0.4),
    proposal(4, mapping.NO_TERM, "skos:exactMatch", 0.8),
]


@pytest.fixture
def gold():
    return mapping.freeze_gold_standard(GOLD_REVIEW, DRAFT, REVIEWER, "2026-11-20")


@pytest.fixture
def proposals():
    return mapping.import_proposals(PROPOSALS, DICTIONARY, AGENT)


def assert_valid_sssom(path):
    msdf = parse_sssom_table(path)
    validate(msdf, [SchemaValidationType.JsonSchema, SchemaValidationType.PrefixMapCompleteness,
                    SchemaValidationType.StrictCurieFormat], fail_on_error=True)
    return msdf


def test_frozen_gold_keeps_drafts_and_adds_corrections(gold):
    assert len(gold) == 6  # 4 drafts + 2 reviewer replacements
    held = mapping.accepted(gold)
    assert held["src:V001"]["curator_type"] == "AI_AGENT"
    assert held["src:V001"]["reviewer_agreement"] == "1.0"
    assert (held["src:V002"]["object_id"], held["src:V002"]["predicate_id"]) == ("LOINC:72172-0", "skos:exactMatch")
    assert held["src:V002"]["author_id"] == REVIEWER["id"]
    assert held["src:V003"]["object_id"] == mapping.NO_TERM
    rejected = [r for r in gold if r["reviewer_agreement"] == "-1.0"]
    assert {r["subject_id"] for r in rejected} == {"src:V002", "src:V003"}


def test_mapping_sets_are_valid_sssom(gold, proposals, tmp_path):
    for name, rows in (("gold", gold), ("proposals", proposals)):
        path = tmp_path / f"{name}.sssom.tsv"
        mapping.write_sssom(path, f"https://w3id.org/pd-biomarker-model/mapping/{name}.sssom.tsv", name, name, rows)
        msdf = assert_valid_sssom(path)
        assert len(msdf.df) == len(rows)
        assert mapping.read_tsv(path) == [{k: v for k, v in r.items() if k in mapping.read_tsv(path)[0]} for r in rows]


def test_score_counts(gold, proposals):
    metrics, errors = mapping.score(proposals, mapping.accepted(gold))
    assert metrics["precision"] == round(2 / 3, 3)
    assert metrics["recall"] == 1.0
    assert metrics["predicate_agreement"] == 0.5
    assert metrics["no_term_agreement"] == 0.5
    assert metrics["fully_correct"] == 0.5
    assert {e["subject_id"]: e["error_type"] for e in errors} == {
        "src:V002": "wrong predicate", "src:V003": "spurious"}
    assert metrics["mean_confidence_correct"] == round((0.9 + 0.8) / 2, 3)


def test_score_uses_ontology_relation(gold, proposals):
    proposals[0] = dict(proposals[0], object_id="HP:0001337", object_label="Tremor")
    _, errors = mapping.score(proposals, mapping.accepted(gold), relation=lambda a, b: "ancestor")
    assert {e["subject_id"]: e["error_type"] for e in errors}["src:V001"] == "too broad"
    proposals[0] = dict(proposals[0], object_id="NCIT:C182454")
    _, errors = mapping.score(proposals, mapping.accepted(gold))
    assert {e["subject_id"]: e["error_type"] for e in errors}["src:V001"] == "wrong ontology"


def test_review_sheet_prefills_gold_matches_and_review_is_recorded(gold, proposals):
    sheet = mapping.review_sheet(proposals, DICTIONARY, mapping.accepted(gold))
    assert [r["decision"] for r in sheet] == ["ACCEPT", "", "", "ACCEPT"]
    sheet[1].update(decision="CHANGE", corrected_predicate_id="skos:exactMatch")
    sheet[2].update(decision="REJECT")
    reviewed = mapping.apply_review(proposals, sheet, REVIEWER, "2026-11-21")
    held = mapping.accepted(reviewed)
    assert held["src:V002"]["predicate_id"] == "skos:exactMatch" and held["src:V002"]["curator_type"] == "PERSON"
    assert held["src:V003"]["object_id"] == mapping.NO_TERM
    assert len(reviewed) == 6


def test_corrected_terms_get_their_label_looked_up():
    review = [dict(GOLD_REVIEW[0], decision="CHANGE", corrected_object_id="HP:0001337")] + GOLD_REVIEW[1:]
    rows = mapping.freeze_gold_standard(review, DRAFT, REVIEWER, "2026-11-20", DICTIONARY,
                                        lookup_label=lambda curie: f"looked up {curie}")
    held = mapping.accepted(rows)
    assert held["src:V001"]["object_label"] == "looked up HP:0001337"
    assert held["src:V002"]["object_label"] == "label LOINC:72172-0"  # same term, new predicate


def test_invalid_input_is_rejected():
    with pytest.raises(ValueError, match="one row per dictionary variable"):
        mapping.freeze_gold_standard(GOLD_REVIEW[:3], DRAFT, REVIEWER, "2026-11-20", DICTIONARY)
    with pytest.raises(ValueError, match="decision"):
        mapping.freeze_gold_standard([dict(GOLD_REVIEW[0], decision="")], DRAFT, REVIEWER, "2026-11-20")
    with pytest.raises(ValueError, match="one proposal per variable"):
        mapping.import_proposals(PROPOSALS[:3], DICTIONARY, AGENT)
    with pytest.raises(ValueError, match="predicate"):
        mapping.import_proposals([dict(PROPOSALS[0], predicate_id="skos:closeMatch")] + PROPOSALS[1:], DICTIONARY, AGENT)
    with pytest.raises(ValueError, match="CURIE"):
        mapping.import_proposals([dict(PROPOSALS[0], object_id="tremor")] + PROPOSALS[1:], DICTIONARY, AGENT)


def test_draft_gold_standard_rows_are_well_formed():
    dictionary = mapping.read_tsv(ROOT / "mapping" / "source_dictionary.tsv")
    review = mapping.read_tsv(ROOT / "mapping" / "gold_standard_review.tsv")
    assert len({r["variable_id"] for r in dictionary}) == len(dictionary) == len(review)
    assert [r["variable_id"] for r in review] == [r["variable_id"] for r in dictionary]
    for row in review:
        mapping._check_mapping(row["variable_id"], row["predicate_id"], row["object_id"])
