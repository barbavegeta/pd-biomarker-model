# Parkinson's disease biomarker model

A [LinkML](https://linkml.io) data model for Parkinson's disease cohort data:
participants, visits, diagnoses, phenotypes, clinical rating scales,
specimens, and fluid and imaging biomarkers. Value sets are bound to
ontologies, cross-field rules are enforced at validation time, and every
measurement carries provenance. All example data is synthetic.

## Structure

The model has two layers.

- **Core** (`core.yaml`): a disease-agnostic model of a cohort study. A
  `StudyDataset` holds flat lists of records that refer to each other by
  identifier, so each class maps to one table.
- **Parkinson's module** (`pd_biomarker_model.yaml`): imports the core and
  narrows it. `ParkinsonsDiagnosis` restricts the condition to parkinsonian
  disorders and adds diagnostic criteria; `ParkinsonsClinicalAssessment`
  binds the instrument to MDS-UPDRS, MoCA and Hoehn and Yahr and adds
  score-range and medication-state rules. Another disease area would add
  its own module in the same way, without changing the core.

See the [model diagram](diagram.md) and the [schema reference](elements/index.md).

## Value sets

- **Diseases**: MONDO, dynamic (descendants of parkinsonian disorder,
  multiple system atrophy, progressive supranuclear palsy and Lewy body
  dementia)
- **Phenotypes**: HPO, dynamic (descendants of *Phenotypic abnormality*)
- **Specimen types**: UBERON
- **Brain regions for imaging**: UBERON, dynamic (parts of *brain*)
- **Assay technologies**: OBI and NCIT
- **Platforms and panel versions**: PRIDE
- **Units**: UCUM codes, mapped to UO
- **Rating scales**: LOINC and NCIT
- **Sex, laterality and measurement type**: PATO and STATO

Each permissible value records its ontology term in `meaning` and the
term's label in `title`. Where no exact term exists, the value carries a
`broad_mappings`, `close_mappings` or `related_mappings` entry instead of a
`meaning`.

## Identifiers and versioning

- Schema URI: `https://w3id.org/pd-biomarker-model`; record identifiers are
  CURIEs in the `pdbm:` namespace.
- Analytes are identified by UniProtKB accession, so values from different
  proteomics platforms can be linked to the same protein, with the platform's
  own reagent identifier (SomaScan SeqId or Olink assay ID) kept on the
  measurement.
- The schema follows semantic versioning; see the [changelog](changelog.md).
