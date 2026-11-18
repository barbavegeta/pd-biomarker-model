"""Data model package for pd-biomarker-model."""

from pathlib import Path
from .pd_biomarker_model import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "pd_biomarker_model.yaml"
