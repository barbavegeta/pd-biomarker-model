"""Export the schema's value sets as standalone vocabularies.

    uv run python scripts/export_vocabularies.py

Each enum with a fixed list of permissible values becomes a vocabulary that a
terminology system can load without LinkML:

- vocabularies/skos/<Enum>.ttl: a SKOS concept scheme (Turtle)
- vocabularies/owl/<Enum>.ttl: an OWL ontology with one class per value (Turtle)
- vocabularies/value_sets.tsv: every value of every vocabulary, one row each

Every value gets its own IRI under the schema's w3id namespace. Ontology terms
are linked to it with SKOS mapping properties: `meaning` and exact_mappings
become skos:exactMatch, and close, broad, narrow and related mappings keep
their SKOS predicate.

Dynamic enums are not copied, because their members follow each ontology
release. vocabularies/dynamic_value_sets.tsv records the query that defines
each one (source ontology, root terms, relationships), so a terminology system
can register it as an intensional value set.

The output contains no dates or other run-dependent values, and rdflib's
Turtle writer sorts subjects and predicates (its RDF/XML writer does not), so
CI can regenerate the files and compare them with the committed copy.
"""

import csv
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "src" / "pd_biomarker_model" / "schema" / "pd_biomarker_model.yaml"
OUT = ROOT / "vocabularies"

OBO = Namespace("http://purl.obolibrary.org/obo/")
DEFINITION = OBO.IAO_0000115  # IAO "definition", the OBO annotation for definitions

MAPPING_PREDICATES = [
    ("exact_mappings", "exact_match", SKOS.exactMatch),
    ("close_mappings", "close_match", SKOS.closeMatch),
    ("broad_mappings", "broad_match", SKOS.broadMatch),
    ("narrow_mappings", "narrow_match", SKOS.narrowMatch),
    ("related_mappings", "related_match", SKOS.relatedMatch),
]
VALUE_COLUMNS = [
    "value_set", "module", "code", "label", "definition", "iri",
    *(column for _, column, _ in MAPPING_PREDICATES), "see_also",
]
DYNAMIC_COLUMNS = [
    "value_set", "module", "description", "source_ontology",
    "source_nodes", "relationship_types", "include_self",
]


def mappings(pv) -> dict[str, list[str]]:
    """The value's mapping CURIEs per SKOS predicate; `meaning` counts as exact."""
    found = {column: list(getattr(pv, slot) or []) for slot, column, _ in MAPPING_PREDICATES}
    if pv.meaning:
        found["exact_match"].insert(0, pv.meaning)
    return found


def concept_graph(sv, enum, scheme_iri, value_iris) -> Graph:
    graph = Graph()
    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)
    graph.bind("owl", OWL)
    scheme = URIRef(scheme_iri)
    graph.add((scheme, RDF.type, SKOS.ConceptScheme))
    graph.add((scheme, SKOS.prefLabel, Literal(enum.name, lang="en")))
    graph.add((scheme, DCTERMS.title, Literal(enum.name, lang="en")))
    graph.add((scheme, DCTERMS.description, Literal(enum.description, lang="en")))
    graph.add((scheme, OWL.versionInfo, Literal(sv.schema.version)))
    graph.add((scheme, DCTERMS.license, URIRef(f"https://spdx.org/licenses/{sv.schema.license}")))
    graph.add((scheme, DCTERMS.source, URIRef(enum.from_schema)))
    for code, pv in enum.permissible_values.items():
        concept = URIRef(value_iris[code])
        graph.add((scheme, SKOS.hasTopConcept, concept))
        graph.add((concept, RDF.type, SKOS.Concept))
        graph.add((concept, SKOS.inScheme, scheme))
        graph.add((concept, SKOS.topConceptOf, scheme))
        graph.add((concept, SKOS.notation, Literal(code)))
        graph.add((concept, SKOS.prefLabel, Literal(pv.title or code, lang="en")))
        graph.add((concept, SKOS.definition, Literal(pv.description, lang="en")))
        add_links(sv, graph, concept, pv)
    return graph


def class_graph(sv, enum, scheme_iri, value_iris) -> Graph:
    graph = Graph()
    graph.bind("skos", SKOS)
    graph.bind("dcterms", DCTERMS)
    graph.bind("obo", OBO)
    ontology = URIRef(f"{scheme_iri}.owl")
    graph.add((ontology, RDF.type, OWL.Ontology))
    graph.add((ontology, DCTERMS.title, Literal(enum.name, lang="en")))
    graph.add((ontology, DCTERMS.description, Literal(enum.description, lang="en")))
    graph.add((ontology, OWL.versionInfo, Literal(sv.schema.version)))
    graph.add((ontology, DCTERMS.license, URIRef(f"https://spdx.org/licenses/{sv.schema.license}")))
    graph.add((ontology, DCTERMS.source, URIRef(enum.from_schema)))
    for prop in (DEFINITION, SKOS.notation, *(p for _, _, p in MAPPING_PREDICATES),
                 DCTERMS.title, DCTERMS.description, DCTERMS.license, DCTERMS.source):
        graph.add((prop, RDF.type, OWL.AnnotationProperty))
    root = URIRef(scheme_iri)
    graph.add((root, RDF.type, OWL.Class))
    graph.add((root, RDFS.label, Literal(enum.name, lang="en")))
    graph.add((root, DEFINITION, Literal(enum.description, lang="en")))
    for code, pv in enum.permissible_values.items():
        cls = URIRef(value_iris[code])
        graph.add((cls, RDF.type, OWL.Class))
        graph.add((cls, RDFS.subClassOf, root))
        graph.add((cls, SKOS.notation, Literal(code)))
        graph.add((cls, RDFS.label, Literal(pv.title or code, lang="en")))
        graph.add((cls, DEFINITION, Literal(pv.description, lang="en")))
        add_links(sv, graph, cls, pv)
    return graph


def add_links(sv, graph, subject, pv) -> None:
    for (_, column, predicate) in MAPPING_PREDICATES:
        for curie in mappings(pv)[column]:
            graph.add((subject, predicate, URIRef(sv.expand_curie(curie))))
    for curie in pv.see_also or []:
        graph.add((subject, RDFS.seeAlso, URIRef(sv.expand_curie(curie))))


def main() -> int:
    sv = SchemaView(str(SCHEMA))
    base = sv.schema.prefixes["pdbm"].prefix_reference + "vocab/"
    shutil.rmtree(OUT / "skos", ignore_errors=True)
    shutil.rmtree(OUT / "owl", ignore_errors=True)
    (OUT / "skos").mkdir(parents=True)
    (OUT / "owl").mkdir(parents=True)

    value_rows, dynamic_rows = [], []
    for name in sorted(sv.all_enums()):
        enum = sv.get_enum(name)
        module = "core" if enum.from_schema.endswith("/core") else "pd_biomarker_model"
        if enum.reachable_from:
            query = enum.reachable_from
            dynamic_rows.append({
                "value_set": name,
                "module": module,
                "description": " ".join(enum.description.split()),
                "source_ontology": query.source_ontology,
                "source_nodes": "|".join(query.source_nodes),
                "relationship_types": "|".join(query.relationship_types),
                "include_self": str(bool(query.include_self)).lower(),
            })
            continue
        if not enum.permissible_values:
            continue
        scheme_iri = base + name
        value_iris = {code: f"{scheme_iri}/{quote(code, safe='')}" for code in enum.permissible_values}
        concept_graph(sv, enum, scheme_iri, value_iris).serialize(
            OUT / "skos" / f"{name}.ttl", format="turtle", encoding="utf-8")
        class_graph(sv, enum, scheme_iri, value_iris).serialize(
            OUT / "owl" / f"{name}.ttl", format="turtle", encoding="utf-8")
        for code, pv in enum.permissible_values.items():
            links = mappings(pv)
            value_rows.append({
                "value_set": name,
                "module": module,
                "code": code,
                "label": pv.title or code,
                "definition": " ".join(pv.description.split()),
                "iri": value_iris[code],
                **{column: "|".join(curies) for column, curies in links.items()},
                "see_also": "|".join(pv.see_also or []),
            })

    for path, columns, rows in (
        (OUT / "value_sets.tsv", VALUE_COLUMNS, value_rows),
        (OUT / "dynamic_value_sets.tsv", DYNAMIC_COLUMNS, dynamic_rows),
    ):
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, columns, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    vocabularies = len({row["value_set"] for row in value_rows})
    print(f"{vocabularies} vocabularies ({len(value_rows)} values), "
          f"{len(dynamic_rows)} dynamic value sets -> {OUT.relative_to(ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
