# Model diagram

Entity-relationship diagram of the Parkinson's module and the core it imports, generated from the schema with `gen-erdiagram`. Records refer to each other by identifier; each line shows a reference slot and its cardinality.

```mermaid
erDiagram
Analyte {
    uriorcurie id  
    string gene_symbol  
    uriorcurie hgnc_id  
    string label  
}
Assay {
    string label  
    PlatformEnum platform  
    AssayTechnologyEnum technology  
    uriorcurie id  
}
BiomarkerMeasurement {
    boolean below_lloq  
    BrainRegionEnum brain_region  
    CategoricalResultEnum categorical_result  
    LateralityEnum laterality  
    uriorcurie loinc_code  
    MeasurementTypeEnum measurement_type  
    ModalityEnum modality  
    string platform_probe_id  
    UnitEnum unit  
    float value  
    uriorcurie id  
    date curation_date  
    uriorcurie curator  
    CuratorTypeEnum curator_type  
    string source  
}
ParkinsonsClinicalAssessment {
    ParkinsonsInstrumentEnum instrument  
    MedicationStateEnum medication_state  
    uriorcurie id  
    float score  
}
ParkinsonsDiagnosis {
    ParkinsonianDisorderEnum condition  
    DiagnosticCertaintyEnum diagnostic_certainty  
    DiagnosticCriteriaEnum diagnostic_criteria  
    uriorcurie id  
    float age_at_diagnosis  
    float age_at_symptom_onset  
}
ParkinsonsStudyDataset {
    uriorcurie id  
    string description  
    uri conforms_to  
    date created_on  
    string dataset_version  
    boolean is_synthetic  
    uri license  
    string title  
}
Participant {
    CohortEnum cohort  
    date enrolment_date  
    SexEnum sex  
    integer year_of_birth  
    uriorcurie id  
}
PhenotypeObservation {
    boolean excluded  
    PhenotypeEnum phenotype  
    uriorcurie id  
}
Specimen {
    integer freeze_thaw_cycles  
    SpecimenTypeEnum specimen_type  
    uriorcurie id  
}
Visit {
    string visit_code  
    date visit_date  
    uriorcurie id  
}

BiomarkerMeasurement ||--|o Specimen : "specimen"
BiomarkerMeasurement ||--|| Analyte : "analyte"
BiomarkerMeasurement ||--|| Assay : "assay"
BiomarkerMeasurement ||--|| Visit : "visit"
ParkinsonsClinicalAssessment ||--|| Visit : "visit"
ParkinsonsDiagnosis ||--|| Participant : "participant"
ParkinsonsStudyDataset ||--}o Analyte : "analytes"
ParkinsonsStudyDataset ||--}o Assay : "assays"
ParkinsonsStudyDataset ||--}o BiomarkerMeasurement : "biomarker_measurements"
ParkinsonsStudyDataset ||--}o ParkinsonsClinicalAssessment : "clinical_assessments"
ParkinsonsStudyDataset ||--}o ParkinsonsDiagnosis : "diagnoses"
ParkinsonsStudyDataset ||--}o Participant : "participants"
ParkinsonsStudyDataset ||--}o PhenotypeObservation : "phenotype_observations"
ParkinsonsStudyDataset ||--}o Specimen : "specimens"
ParkinsonsStudyDataset ||--}o Visit : "visits"
PhenotypeObservation ||--|| Visit : "visit"
Specimen ||--|| Visit : "visit"
Visit ||--|| Participant : "participant"

```

