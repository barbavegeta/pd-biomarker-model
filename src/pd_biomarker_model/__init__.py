"""pd-biomarker-model.

LinkML data model for Parkinson's disease phenotypes and biomarkers, with ontology-bound value sets, validation and AI-assisted SSSOM mapping on synthetic data
"""

try:
    from pd_biomarker_model._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = "0.0.0"
    __version_tuple__ = (0, 0, 0)
