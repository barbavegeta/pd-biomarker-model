"""Generate the SQL DDL for the schema, with no tables for abstract classes.

    uv run python scripts/gen_sql.py [schema.yaml] > artifacts/sql/pd_biomarker_model.sql

The output is that of `gen-sqltables --no-metadata --generate_abstract_class_ddl
false`, with one fix. LinkML 1.12.1 turns each list slot of an abstract class
(here the core StudyDataset's record lists) into a foreign-key column on the
record tables, but generates no table for the abstract class, so the DDL refers
to a missing table and SQLAlchemy rejects it. This script drops those
columns; each record keeps its key to the concrete dataset table
(ParkinsonsStudyDataset).
"""

import sys
from pathlib import Path

import linkml.generators.sqltablegen as sqltablegen
from linkml.transformers.relmodel_transformer import RelationalModelTransformer

SCHEMA = Path(__file__).resolve().parents[1] / "src" / "pd_biomarker_model" / "schema" / "pd_biomarker_model.yaml"


class AbstractBackrefPruningTransformer(RelationalModelTransformer):
    """Relational transformer that drops back-reference columns to abstract classes."""

    def transform(self, *args, **kwargs):
        result = super().transform(*args, **kwargs)
        classes = result.schema.classes
        abstract = {name for name, cls in classes.items() if cls.abstract}
        for cls in classes.values():
            for name, attribute in list(cls.attributes.items()):
                if attribute.range in abstract and "backref" in attribute.annotations:
                    del cls.attributes[name]
        return result


def main() -> int:
    schema = sys.argv[1] if len(sys.argv) > 1 else str(SCHEMA)
    sqltablegen.RelationalModelTransformer = AbstractBackrefPruningTransformer
    generator = sqltablegen.SQLTableGenerator(schema, metadata=False, generate_abstract_class_ddl=False)
    print(generator.generate_ddl())
    return 0


if __name__ == "__main__":
    sys.exit(main())
