"""The exported vocabularies match the schema's value sets."""

import csv
from pathlib import Path

import pytest
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "vocabularies"
SV = SchemaView(str(ROOT / "src" / "pd_biomarker_model" / "schema" / "pd_biomarker_model.yaml"))
STATIC = sorted(n for n, e in SV.all_enums().items() if e.permissible_values and not e.reachable_from)
DYNAMIC = sorted(n for n, e in SV.all_enums().items() if e.reachable_from)


def read_tsv(name):
    with (VOCAB / name).open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_one_file_of_each_kind_per_static_value_set():
    assert sorted(p.stem for p in (VOCAB / "skos").glob("*.ttl")) == STATIC
    assert sorted(p.stem for p in (VOCAB / "owl").glob("*.ttl")) == STATIC


@pytest.mark.parametrize("name", STATIC)
def test_skos_scheme_has_one_concept_per_value(name):
    enum = SV.get_enum(name)
    graph = Graph().parse(VOCAB / "skos" / f"{name}.ttl")
    schemes = list(graph.subjects(RDF.type, SKOS.ConceptScheme))
    assert len(schemes) == 1
    concepts = set(graph.subjects(RDF.type, SKOS.Concept))
    assert len(concepts) == len(enum.permissible_values)
    notations = {}
    for concept in concepts:
        assert set(graph.objects(concept, SKOS.inScheme)) == {schemes[0]}
        assert (schemes[0], SKOS.hasTopConcept, concept) in graph
        labels = list(graph.objects(concept, SKOS.prefLabel))
        assert len(labels) == 1 and labels[0].language == "en"
        assert len(list(graph.objects(concept, SKOS.definition))) == 1
        (notation,) = graph.objects(concept, SKOS.notation)
        notations[str(notation)] = concept
    assert set(notations) == set(enum.permissible_values)
    for code, pv in enum.permissible_values.items():
        if pv.meaning:
            assert (notations[code], SKOS.exactMatch, URIRef(SV.expand_curie(pv.meaning))) in graph


@pytest.mark.parametrize("name", STATIC)
def test_owl_ontology_has_one_class_per_value(name):
    enum = SV.get_enum(name)
    graph = Graph().parse(VOCAB / "owl" / f"{name}.ttl")
    assert len(list(graph.subjects(RDF.type, OWL.Ontology))) == 1
    skos = Graph().parse(VOCAB / "skos" / f"{name}.ttl")
    (root,) = skos.subjects(RDF.type, SKOS.ConceptScheme)
    values = set(graph.subjects(RDFS.subClassOf, root))
    assert values == set(skos.subjects(RDF.type, SKOS.Concept))
    assert {str(graph.value(v, SKOS.notation)) for v in values} == set(enum.permissible_values)
    for value in values:
        assert (value, RDF.type, OWL.Class) in graph
        assert isinstance(graph.value(value, RDFS.label), Literal)


def test_value_table_lists_every_value_once():
    rows = read_tsv("value_sets.tsv")
    expected = {(n, code) for n in STATIC for code in SV.get_enum(n).permissible_values}
    assert {(r["value_set"], r["code"]) for r in rows} == expected
    assert len(rows) == len(expected)
    assert len({r["iri"] for r in rows}) == len(rows)


def test_dynamic_value_sets_are_listed_with_their_query():
    rows = read_tsv("dynamic_value_sets.tsv")
    assert [r["value_set"] for r in rows] == DYNAMIC
    for row in rows:
        query = SV.get_enum(row["value_set"]).reachable_from
        assert row["source_nodes"].split("|") == list(query.source_nodes)
