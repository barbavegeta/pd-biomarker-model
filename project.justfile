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
