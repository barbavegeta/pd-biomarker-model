"""Validation plugins for checks that JSON Schema cannot express.

Both plugins run inside ``linkml-validate`` (see ``validation.yaml``) and
through :func:`validate_file`.

- :class:`DatasetDynamicEnumPlugin` checks values of dynamic (``reachable_from``)
  enums in every record of a dataset, not only in the top-level object.
- :class:`CrossRecordPlugin` checks rules that compare values, or that span
  more than one record: referential integrity, unique identifiers, visit
  dates against enrolment, specimen and measurement visits, and symptom
  onset against diagnosis.
"""

from __future__ import annotations

from collections.abc import Iterator
from datetime import date
from pathlib import Path
from typing import Any

import yaml
from linkml.validator import Validator
from linkml.validator.plugins import JsonschemaValidationPlugin, ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext
from linkml_runtime.utils.schemaview import SchemaView
from linkml_term_validator.plugins import DynamicEnumPlugin

PACKAGE_DIR = Path(__file__).parent
SCHEMA_PATH = PACKAGE_DIR / "schema" / "pd_biomarker_model.yaml"
TARGET_CLASS = "ParkinsonsStudyDataset"


class DatasetDynamicEnumPlugin(DynamicEnumPlugin):
    """Check dynamic enum values in every record nested inside a dataset.

    ``DynamicEnumPlugin`` validates only the slots of the top-level object.
    This subclass walks inlined records, resolving each record's class from
    the range of the slot that holds it, and applies the same ontology check
    (and the same file cache) to every dynamic-enum slot it finds.
    """

    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        if self.schema_view is None or not context.target_class:
            return
        yield from self._walk(instance, context.target_class)

    def _walk(self, record: dict, class_name: str) -> Iterator[ValidationResult]:
        sv = self.schema_view
        classes = sv.all_classes()
        for slot_name, value in record.items():
            try:
                slot = sv.induced_slot(slot_name, class_name)
            except (KeyError, AttributeError, ValueError):
                continue  # unknown slots are reported by the JSON Schema plugin
            if slot.range in classes:
                for item in value if isinstance(value, list) else [value]:
                    if isinstance(item, dict):
                        yield from self._walk(item, slot.range)
                continue
            enum_def = sv.get_enum(slot.range) if slot.range else None
            if enum_def is not None and self.is_dynamic_enum(enum_def):
                yield from self._validate_enum_value_progressive(
                    slot_name=slot_name,
                    value=value,
                    enum_def=enum_def,
                    instance=record,
                    target_class=class_name,
                )


class CrossRecordPlugin(ValidationPlugin):
    """Rules that compare values or follow references between records."""

    def pre_process(self, context: ValidationContext) -> None:
        self.schema_view: SchemaView = context.schema_view

    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        sv = self.schema_view
        target = context.target_class
        collections = self._collections(target)
        index: dict[str, dict[str, dict]] = {}

        # Unique identifiers, and an index of every record by collection.
        seen: dict[str, str] = {}
        for coll, _ in collections.items():
            index[coll] = {}
            for record in instance.get(coll) or []:
                rid = record.get("id")
                if rid in seen:
                    yield self._error(
                        "unique_identifier",
                        f"{coll}: identifier {rid} is already used in {seen[rid]}",
                        record,
                    )
                seen[rid] = coll
                index[coll][rid] = record

        # Referential integrity: every reference resolves to a record of the right class.
        for coll, cls in collections.items():
            for record in index[coll].values():
                for slot_name, value in record.items():
                    try:
                        slot = sv.induced_slot(slot_name, cls)
                    except (KeyError, AttributeError, ValueError):
                        continue
                    if slot.range not in sv.all_classes() or slot.inlined or slot.inlined_as_list:
                        continue
                    targets = [c for c, r in collections.items() if r in sv.class_descendants(slot.range)]
                    for ref in value if isinstance(value, list) else [value]:
                        if not any(ref in index[t] for t in targets):
                            yield self._error(
                                "referential_integrity",
                                f"{coll}/{record.get('id')}: {slot_name} {ref} does not match any "
                                f"{slot.range} in the dataset",
                                record,
                            )

        participants = index.get("participants", {})
        visits = index.get("visits", {})
        specimens = index.get("specimens", {})

        # A visit cannot take place before the participant was enrolled.
        for vid, visit in visits.items():
            participant = participants.get(visit.get("participant"))
            if not participant:
                continue
            visit_date = _as_date(visit.get("visit_date"))
            enrolled = _as_date(participant.get("enrolment_date"))
            if visit_date and enrolled and visit_date < enrolled:
                yield self._error(
                    "visit_after_enrolment",
                    f"visits/{vid}: visit_date {visit_date} is before enrolment_date "
                    f"{enrolled} of {participant['id']}",
                    visit,
                )

        # A measurement's specimen must have been collected at the measurement's visit.
        for mid, measurement in index.get("biomarker_measurements", {}).items():
            specimen = specimens.get(measurement.get("specimen"))
            if specimen and specimen.get("visit") != measurement.get("visit"):
                yield self._error(
                    "specimen_visit",
                    f"biomarker_measurements/{mid}: visit {measurement.get('visit')} differs from "
                    f"the visit {specimen.get('visit')} at which specimen {specimen['id']} was collected",
                    measurement,
                )

        # Symptoms start before (or when) the condition is diagnosed.
        for did, diagnosis in index.get("diagnoses", {}).items():
            onset = diagnosis.get("age_at_symptom_onset")
            diagnosed = diagnosis.get("age_at_diagnosis")
            if onset is not None and diagnosed is not None and onset > diagnosed:
                yield self._error(
                    "onset_before_diagnosis",
                    f"diagnoses/{did}: age_at_symptom_onset {onset} is after age_at_diagnosis {diagnosed}",
                    diagnosis,
                )

    def _collections(self, target: str) -> dict[str, str]:
        """Map each inlined list slot of the target class to the class it holds."""
        sv = self.schema_view
        return {
            s.name: s.range
            for s in sv.class_induced_slots(target)
            if s.multivalued and s.inlined_as_list and s.range in sv.all_classes()
        }

    @staticmethod
    def _error(rule: str, message: str, record: dict) -> ValidationResult:
        return ValidationResult(
            type=f"cross_record:{rule}",
            severity=Severity.ERROR,
            message=message,
            instance=record,
        )


def _as_date(value: Any) -> date | None:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return None


def build_validator(cache_dir: Path | str = "ontology_cache", offline: bool = True) -> Validator:
    """Validator with the same plugins as ``validation.yaml``."""
    cache_dir = Path(cache_dir)
    return Validator(
        schema=str(SCHEMA_PATH),
        validation_plugins=[
            JsonschemaValidationPlugin(closed=True),
            DatasetDynamicEnumPlugin(
                cache_dir=cache_dir,
                oak_config_path=cache_dir / "oak_config.yaml",
                offline=offline,
            ),
            CrossRecordPlugin(),
        ],
    )


def validate_file(path: Path | str, validator: Validator | None = None) -> list[ValidationResult]:
    """Validate one dataset file and return its errors."""
    validator = validator or build_validator()
    with open(path) as fh:
        data = yaml.safe_load(fh)
    report = validator.validate(data, TARGET_CLASS)
    return [r for r in report.results if r.severity == Severity.ERROR]
