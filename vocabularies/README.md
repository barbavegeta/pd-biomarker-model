# Vocabularies

The schema's value sets, exported as standalone vocabularies that a
terminology system can load without LinkML. `scripts/export_vocabularies.py`
generates every file here from the schema; run `just gen-vocabularies` after
changing an enum. CI regenerates the files and fails if they differ from the
committed copy.

- `skos/<Enum>.ttl`: one SKOS concept scheme per value set (Turtle).
- `owl/<Enum>.ttl`: the same value set as an OWL ontology, with one class per
  value under a root class for the value set (Turtle).
- `value_sets.tsv`: every value of every value set, one row each.
- `dynamic_value_sets.tsv`: the value sets defined by an ontology query
  rather than a fixed list (diseases, phenotypes, brain regions, parkinsonian
  disorders). Their members follow each ontology release, so only the query
  is exported: source ontology, root terms, relationships and whether the
  roots themselves are included.

## Identifiers and content

- Each value set has the IRI
  `https://w3id.org/pd-biomarker-model/vocab/<Enum>`, and each value the IRI
  `https://w3id.org/pd-biomarker-model/vocab/<Enum>/<code>`, with the code
  percent-encoded (`pg/mL` becomes `pg%2FmL`). The same IRIs are used in the
  SKOS and OWL files.
- The code is the permissible value as it appears in data (`skos:notation`).
  The label is the matched ontology term's label, or the code where the value
  has no ontology term. The definition is the value's description.
- Ontology terms are linked with SKOS mapping properties: the value's
  `meaning` and exact mappings become `skos:exactMatch`, and close, broad,
  narrow and related mappings keep their SKOS predicate. In the OWL files
  these are annotations, so no logical axioms are asserted about external
  terms.
- Each file records the schema version (`owl:versionInfo`), the licence and
  the schema module it comes from (`dcterms:source`).
