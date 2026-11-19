## Project recipes. This file is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

diagram_page := "docs/diagram.md"

# Generate the Mermaid ER diagram page from the schema
[group('model development')]
gen-diagram:
  printf '%s\n\n%s\n\n' '# Model diagram' 'Entity-relationship diagram of the Parkinson'"'"'s module and the core it imports, generated from the schema with `gen-erdiagram`. Records refer to each other by identifier; each line shows a reference slot and its cardinality.' > {{diagram_page}}
  uv run gen-erdiagram -f markdown {{source_schema_path}} >> {{diagram_page}}

# Build the documentation site locally (schema pages, diagram, MkDocs)
[group('model development')]
docs: gen-diagram gen-doc
  uv run mkdocs build --strict

artifact_dir := "artifacts"

# Generate the committed artifacts: JSON Schema, SQL DDL, Pydantic and dataclass models, diagram, vocabularies
[group('model development')]
gen-artifacts: gen-python gen-diagram gen-examples gen-vocabularies
  mkdir -p {{artifact_dir}}/jsonschema {{artifact_dir}}/sql
  uv run gen-json-schema --no-metadata {{source_schema_path}} > {{artifact_dir}}/jsonschema/{{schema_name}}.schema.json
  uv run gen-sqltables --no-metadata --generate_abstract_class_ddl false {{source_schema_path}} > {{artifact_dir}}/sql/{{schema_name}}.sql

# Fail if any committed artifact differs from what the schema generates
[group('model development')]
check-artifacts: gen-artifacts
  git add --intent-to-add {{artifact_dir}} {{pymodel}} {{diagram_page}} examples/valid examples/invalid vocabularies
  git diff --exit-code --stat -- {{artifact_dir}} {{pymodel}} {{diagram_page}} examples/valid examples/invalid vocabularies || (echo "Generated artifacts are out of date: run 'just gen-artifacts' and commit." && exit 1)

# Export the value sets as standalone SKOS, OWL and TSV vocabularies
[group('model development')]
gen-vocabularies:
  uv run python scripts/export_vocabularies.py

# Regenerate the synthetic example datasets
[group('model development')]
gen-examples:
  uv run python scripts/make_examples.py

# Validate every example with linkml-validate (valid must pass, invalid must fail)
[group('model development')]
validate-examples:
  for f in examples/valid/*.yaml; do uv run linkml-validate --config validation.yaml "$f" || exit 1; done
  for f in examples/invalid/*.yaml; do if uv run linkml-validate --config validation.yaml "$f" > /dev/null 2>&1; then echo "$f should be invalid"; exit 1; fi; done
  @echo "All examples behave as expected."

# Check every `meaning` term in the schema against the committed ontology cache
[group('model development')]
check-terms:
  for f in {{source_schema_dir}}/*.yaml; do uv run linkml-term-validator validate-schema --offline --config ontology_cache/oak_config.yaml --cache-dir ontology_cache "$f" || exit 1; done

# Rebuild the ontology cache from local ontology databases (needs network on first run)
[group('model development')]
refresh-ontology-cache:
  uv run python scripts/refresh_ontology_cache.py
