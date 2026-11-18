"""Rebuild ontology_cache/ from local ontology databases.

Run with network access (oaklib downloads the semantic-sql databases on first
use, about 8 GB):

    uv run python scripts/refresh_ontology_cache.py

It caches the label of every `meaning` term in the schema and the full
expansion of every dynamic enum reachable from the dataset class, so that
validation in CI can run offline against the committed cache.

Two vocabularies are not available through oaklib. LOINC labels are looked up
on the public HL7 FHIR terminology server (tx.fhir.org); PROV-O labels are the
rdfs:label values of the W3C PROV-O ontology.
"""

import csv
import json
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView

from pd_biomarker_model.validation import SCHEMA_PATH, TARGET_CLASS, DatasetDynamicEnumPlugin

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "ontology_cache"
CONFIG = CACHE / "oak_config.yaml"

PROV_LABELS = {"prov:Person": "Person", "prov:SoftwareAgent": "SoftwareAgent"}  # W3C PROV-O rdfs:label


def loinc_label(code: str) -> str:
    query = urllib.parse.urlencode({"system": "http://loinc.org", "code": code})
    request = urllib.request.Request(
        f"https://tx.fhir.org/r4/CodeSystem/$lookup?{query}",
        headers={"Accept": "application/fhir+json"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        params = json.load(response)["parameter"]
    return next(p["valueString"] for p in params if p["name"] == "display")


def cache_external_labels(sv: SchemaView) -> None:
    """Write label caches for the LOINC and PROV meanings used in the schema."""
    rows: dict[str, list[tuple[str, str]]] = {}
    for enum_def in sv.all_enums().values():
        for pv in enum_def.permissible_values.values():
            meaning = pv.meaning or ""
            prefix = meaning.split(":", 1)[0]
            if prefix == "LOINC":
                rows.setdefault("loinc", []).append((meaning, loinc_label(meaning.split(":", 1)[1])))
            elif prefix == "prov":
                rows.setdefault("prov", []).append((meaning, PROV_LABELS[meaning]))
    now = datetime.now().isoformat()
    for folder, entries in rows.items():
        (CACHE / folder).mkdir(exist_ok=True)
        with open(CACHE / folder / "terms.csv", "w", newline="") as fh:
            writer = csv.writer(fh, lineterminator="\n")
            writer.writerow(["curie", "label", "retrieved_at"])
            for curie, label in sorted(set(entries)):
                writer.writerow([curie, label, now])


def dynamic_enums_in_use(sv: SchemaView, class_name: str, seen: set[str] | None = None) -> set[str]:
    """Names of dynamic enums used by the class and every class it inlines or references."""
    seen = seen if seen is not None else set()
    if class_name in seen:
        return set()
    seen.add(class_name)
    found = set()
    for slot in sv.class_induced_slots(class_name):
        if slot.range in sv.all_classes():
            found |= dynamic_enums_in_use(sv, slot.range, seen)
        elif slot.range in sv.all_enums():
            enum_def = sv.get_enum(slot.range)
            if enum_def.reachable_from or enum_def.matches or enum_def.concepts:
                found.add(enum_def.name)
    return found


def main() -> None:
    for sub in CACHE.iterdir():
        if sub.is_dir():
            shutil.rmtree(sub)

    sv = SchemaView(str(SCHEMA_PATH))
    cache_external_labels(sv)

    # Labels of every other `meaning` term in both schema files.
    for schema in sorted((SCHEMA_PATH.parent).glob("*.yaml")):
        subprocess.run(
            ["linkml-term-validator", "validate-schema", "--config", str(CONFIG),
             "--cache-dir", str(CACHE), str(schema)],
            check=True,
        )

    # Full closure of each dynamic enum the dataset can use.
    plugin = DatasetDynamicEnumPlugin(
        cache_dir=CACHE, oak_config_path=CONFIG, saturate_enum_caches=True
    )
    for name in sorted(dynamic_enums_in_use(sv, TARGET_CLASS)):
        terms = plugin.expand_enum(sv.get_enum(name), sv)
        print(f"{name}: {len(terms)} terms", file=sys.stderr)


if __name__ == "__main__":
    main()
