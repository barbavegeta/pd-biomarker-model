# Changelog

All notable changes to the schema are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the schema
uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html):

- **major**: a change that can make previously valid data invalid (removed or
  renamed classes, slots or permissible values; narrower ranges; new required
  slots or rules)
- **minor**: a backwards-compatible addition (new optional slots, classes or
  permissible values)
- **patch**: documentation, descriptions or mappings only

## [0.1.0] - 2026-11-18

### Added

- Disease-agnostic core schema (`core.yaml`): StudyDataset, Participant, Visit,
  Diagnosis, PhenotypeObservation, ClinicalAssessment, Specimen, Analyte, Assay,
  BiomarkerMeasurement and ProvenanceMixin.
- Parkinson's module (`pd_biomarker_model.yaml`): ParkinsonsStudyDataset,
  ParkinsonsDiagnosis and ParkinsonsClinicalAssessment.
- Value sets bound to MONDO, HPO, UBERON, OBI, PATO, NCIT, STATO, UO, PRIDE and
  LOINC; dynamic value sets for diseases, phenotypes, brain regions and
  parkinsonian disorders.
- Cross-field rules for units by measurement type, quantitative versus
  categorical results, imaging versus specimen measurements, curator
  identifiers, instrument score ranges and medication state.
