"""Every valid example passes and every invalid example fails for its own rule."""

import subprocess
import sys
from pathlib import Path

import pytest
from linkml_runtime.loaders import yaml_loader

from pd_biomarker_model.datamodel import pd_biomarker_model as dataclass_model
from pd_biomarker_model.datamodel import pd_biomarker_model_pydantic as pydantic_model
from pd_biomarker_model.validation import build_validator, validate_file

ROOT = Path(__file__).resolve().parents[1]
VALID = sorted((ROOT / "examples" / "valid").glob("*.yaml"))
INVALID = sorted((ROOT / "examples" / "invalid").glob("*.yaml"))
LINKML_VALIDATE = Path(sys.executable).with_name("linkml-validate")


def expected_error(path: Path) -> str:
    for line in path.read_text().splitlines():
        if line.startswith("# Expect:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"{path.name} has no '# Expect:' header")


@pytest.fixture(scope="module")
def validator():
    return build_validator(cache_dir=ROOT / "ontology_cache")


def test_example_sets_are_not_empty():
    assert VALID and INVALID


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_example_passes(path, validator):
    assert validate_file(path, validator) == []


@pytest.mark.parametrize("path", INVALID, ids=lambda p: p.stem)
def test_invalid_example_fails_for_its_rule(path, validator):
    errors = validate_file(path, validator)
    expected = expected_error(path)
    assert errors, f"{path.name} validated without errors"
    assert all(expected in e.message for e in errors), [e.message for e in errors]


@pytest.mark.parametrize("path", VALID + INVALID, ids=lambda p: f"{p.parent.name}-{p.stem}")
def test_linkml_validate_cli(path):
    """linkml-validate with validation.yaml exits 0 on valid and 1 on invalid files."""
    result = subprocess.run(
        [str(LINKML_VALIDATE), "--config", "validation.yaml", str(path)],
        cwd=ROOT, capture_output=True, text=True,
    )
    assert result.returncode == (0 if path.parent.name == "valid" else 1), result.stdout + result.stderr


@pytest.mark.parametrize("path", VALID, ids=lambda p: p.stem)
def test_valid_example_loads_into_python_models(path):
    assert yaml_loader.load(str(path), target_class=dataclass_model.ParkinsonsStudyDataset)
    import yaml

    data = yaml.safe_load(path.read_text())
    assert pydantic_model.ParkinsonsStudyDataset(**data)
