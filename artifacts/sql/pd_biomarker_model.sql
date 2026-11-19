-- # Class: ParkinsonsStudyDataset Description: A study dataset whose diagnoses and assessments follow the Parkinson's module.
--     * Slot: title Description: Human-readable title of the dataset.
--     * Slot: description Description: Free-text description of the dataset.
--     * Slot: dataset_version Description: Version of the dataset, in semantic versioning form.
--     * Slot: license Description: Licence under which the dataset is released, as a URI.
--     * Slot: created_on Description: Date the dataset was created.
--     * Slot: conforms_to Description: Identifier of the schema version the dataset conforms to.
--     * Slot: is_synthetic Description: True when every record in the dataset is synthetic.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
-- # Class: ParkinsonsDiagnosis Description: Diagnosis of a parkinsonian disorder, with the clinical criteria used and their level of certainty.
--     * Slot: diagnostic_criteria Description: Published clinical diagnostic criteria applied.
--     * Slot: diagnostic_certainty Description: Level of certainty reached under the diagnostic criteria.
--     * Slot: participant Description: The participant this record belongs to.
--     * Slot: condition Description: Diagnosed condition, as a MONDO term.
--     * Slot: age_at_symptom_onset Description: Age in years at onset of the first symptom attributed to the condition.
--     * Slot: age_at_diagnosis Description: Age in years when the condition was diagnosed.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Class: ParkinsonsClinicalAssessment Description: Total score on a Parkinson's rating scale, with the dopaminergic medication state at the time of a motor examination.
--     * Slot: medication_state Description: Dopaminergic medication state during a motor examination.
--     * Slot: visit Description: The visit at which this record was collected.
--     * Slot: instrument Description: The rating scale and score that was recorded. Disease modules bind this to their own value set.
--     * Slot: score Description: Total score on the instrument.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Abstract Class: NamedThing Description: Any record with a globally unique identifier.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
-- # Abstract Class: StudyDataset Description: A versioned collection of cohort records with dataset-level metadata. Records refer to each other by identifier. Disease modules subclass this and narrow the ranges of its record lists.
--     * Slot: title Description: Human-readable title of the dataset.
--     * Slot: description Description: Free-text description of the dataset.
--     * Slot: dataset_version Description: Version of the dataset, in semantic versioning form.
--     * Slot: license Description: Licence under which the dataset is released, as a URI.
--     * Slot: created_on Description: Date the dataset was created.
--     * Slot: conforms_to Description: Identifier of the schema version the dataset conforms to.
--     * Slot: is_synthetic Description: True when every record in the dataset is synthetic.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
-- # Class: Participant Description: A person enrolled in the study.
--     * Slot: cohort Description: Study arm the participant was enrolled in.
--     * Slot: sex Description: Biological sex of the participant.
--     * Slot: year_of_birth Description: Year of birth (full dates of birth are not recorded).
--     * Slot: enrolment_date Description: Date the participant was enrolled.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Class: Visit Description: A scheduled study visit at which data and specimens are collected.
--     * Slot: participant Description: The participant this record belongs to.
--     * Slot: visit_code Description: Protocol visit code as months from baseline, e.g. M00 for baseline and M12 for month 12.
--     * Slot: visit_date Description: Date the visit took place.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Abstract Class: Diagnosis Description: A clinical diagnosis recorded for a participant. Disease modules subclass this and bind the condition to their own value set.
--     * Slot: participant Description: The participant this record belongs to.
--     * Slot: condition Description: Diagnosed condition, as a MONDO term.
--     * Slot: age_at_symptom_onset Description: Age in years at onset of the first symptom attributed to the condition.
--     * Slot: age_at_diagnosis Description: Age in years when the condition was diagnosed.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
-- # Class: PhenotypeObservation Description: A phenotypic feature assessed at a visit, recorded as present or explicitly excluded.
--     * Slot: visit Description: The visit at which this record was collected.
--     * Slot: phenotype Description: Phenotypic feature, as an HPO term.
--     * Slot: excluded Description: True when the feature was looked for and found absent.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Abstract Class: ClinicalAssessment Description: The total score of a clinical rating scale administered at a visit. Disease modules subclass this and bind the instrument to their own value set.
--     * Slot: visit Description: The visit at which this record was collected.
--     * Slot: instrument Description: The rating scale and score that was recorded. Disease modules bind this to their own value set.
--     * Slot: score Description: Total score on the instrument.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
-- # Class: Specimen Description: A biological sample collected at a visit.
--     * Slot: visit Description: The visit at which this record was collected.
--     * Slot: specimen_type Description: Anatomical material of the specimen, as an UBERON term.
--     * Slot: freeze_thaw_cycles Description: Number of freeze-thaw cycles before analysis.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Class: Analyte Description: The molecular entity a measurement quantifies, identified by its UniProtKB accession so that values from different platforms can be linked to the same protein.
--     * Slot: label Description: Human-readable name of the record.
--     * Slot: gene_symbol Description: HGNC-approved symbol of the gene encoding the analyte.
--     * Slot: hgnc_id Description: HGNC identifier of the gene encoding the analyte.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Class: Assay Description: A measurement procedure, defined by its technology and platform.
--     * Slot: label Description: Human-readable name of the record.
--     * Slot: technology Description: Assay technology, as an OBI or NCIT term.
--     * Slot: platform Description: Commercial platform and panel version, where one applies.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Class: BiomarkerMeasurement Description: One biomarker value for one analyte at one visit, from a specimen (fluid or tissue) or from imaging.
--     * Slot: visit Description: The visit at which this record was collected.
--     * Slot: specimen Description: The specimen that was assayed. Absent for imaging measurements.
--     * Slot: assay Description: The assay that produced the value.
--     * Slot: analyte Description: The analyte that was measured.
--     * Slot: platform_probe_id Description: Platform-specific reagent identifier: a SomaScan SeqId (e.g. seq.12345.6) or an Olink assay ID (e.g. OID12345).
--     * Slot: loinc_code Description: LOINC code of the laboratory test, where one exists.
--     * Slot: modality Description: Whether the value comes from a specimen or from imaging.
--     * Slot: measurement_type Description: Kind of quantity the value represents.
--     * Slot: value Description: Numeric value of a quantitative measurement.
--     * Slot: unit Description: Unit of the value, as a UCUM code.
--     * Slot: categorical_result Description: Result of a qualitative assay.
--     * Slot: below_lloq Description: True when the value is below the assay's lower limit of quantification.
--     * Slot: brain_region Description: Brain region of an imaging measurement, as an UBERON term.
--     * Slot: laterality Description: Side of the body the imaging value refers to.
--     * Slot: source Description: Identifier or name of the source dataset, file or system the record was taken from.
--     * Slot: curation_date Description: Date the record was curated.
--     * Slot: curator Description: Who curated the record: an ORCID for a person, or a versioned agent identifier for an AI agent.
--     * Slot: curator_type Description: Whether the curator was a person or an AI agent.
--     * Slot: id Description: Globally unique identifier of the record, written as a CURIE.
--     * Slot: ParkinsonsStudyDataset_id Description: Autocreated FK slot
-- # Abstract Class: ProvenanceMixin Description: Who curated a record, when, from which source, and whether the curator was a person or an AI agent.
--     * Slot: id
--     * Slot: source Description: Identifier or name of the source dataset, file or system the record was taken from.
--     * Slot: curation_date Description: Date the record was curated.
--     * Slot: curator Description: Who curated the record: an ORCID for a person, or a versioned agent identifier for an AI agent.
--     * Slot: curator_type Description: Whether the curator was a person or an AI agent.

CREATE TABLE "ParkinsonsStudyDataset" (
	title TEXT NOT NULL,
	description TEXT,
	dataset_version TEXT NOT NULL,
	license TEXT NOT NULL,
	created_on DATE NOT NULL,
	conforms_to TEXT NOT NULL,
	is_synthetic BOOLEAN NOT NULL,
	id TEXT NOT NULL,
	PRIMARY KEY (id)
);
CREATE INDEX "ix_ParkinsonsStudyDataset_id" ON "ParkinsonsStudyDataset" (id);

CREATE TABLE "Participant" (
	cohort VARCHAR(15) NOT NULL,
	sex VARCHAR(6),
	year_of_birth INTEGER,
	enrolment_date DATE NOT NULL,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_Participant_id" ON "Participant" (id);

CREATE TABLE "Analyte" (
	label TEXT NOT NULL,
	gene_symbol TEXT,
	hgnc_id TEXT,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_Analyte_id" ON "Analyte" (id);

CREATE TABLE "Assay" (
	label TEXT NOT NULL,
	technology VARCHAR(24) NOT NULL,
	platform VARCHAR(19),
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_Assay_id" ON "Assay" (id);

CREATE TABLE "ParkinsonsDiagnosis" (
	diagnostic_criteria VARCHAR(19) NOT NULL,
	diagnostic_certainty VARCHAR(22),
	participant TEXT NOT NULL,
	condition VARCHAR NOT NULL,
	age_at_symptom_onset FLOAT,
	age_at_diagnosis FLOAT,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(participant) REFERENCES "Participant" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_ParkinsonsDiagnosis_id" ON "ParkinsonsDiagnosis" (id);

CREATE TABLE "Visit" (
	participant TEXT NOT NULL,
	visit_code TEXT NOT NULL,
	visit_date DATE NOT NULL,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(participant) REFERENCES "Participant" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_Visit_id" ON "Visit" (id);

CREATE TABLE "ParkinsonsClinicalAssessment" (
	medication_state VARCHAR(9),
	visit TEXT NOT NULL,
	instrument VARCHAR(18) NOT NULL,
	score FLOAT NOT NULL,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(visit) REFERENCES "Visit" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_ParkinsonsClinicalAssessment_id" ON "ParkinsonsClinicalAssessment" (id);

CREATE TABLE "PhenotypeObservation" (
	visit TEXT NOT NULL,
	phenotype VARCHAR NOT NULL,
	excluded BOOLEAN,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(visit) REFERENCES "Visit" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_PhenotypeObservation_id" ON "PhenotypeObservation" (id);

CREATE TABLE "Specimen" (
	visit TEXT NOT NULL,
	specimen_type VARCHAR(11) NOT NULL,
	freeze_thaw_cycles INTEGER,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(visit) REFERENCES "Visit" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_Specimen_id" ON "Specimen" (id);

CREATE TABLE "BiomarkerMeasurement" (
	visit TEXT NOT NULL,
	specimen TEXT,
	assay TEXT NOT NULL,
	analyte TEXT NOT NULL,
	platform_probe_id TEXT,
	loinc_code TEXT,
	modality VARCHAR(8) NOT NULL,
	measurement_type VARCHAR(18) NOT NULL,
	value FLOAT,
	unit VARCHAR(5),
	categorical_result VARCHAR(13),
	below_lloq BOOLEAN,
	brain_region VARCHAR,
	laterality VARCHAR(9),
	source TEXT NOT NULL,
	curation_date DATE NOT NULL,
	curator TEXT NOT NULL,
	curator_type VARCHAR(8) NOT NULL,
	id TEXT NOT NULL,
	"ParkinsonsStudyDataset_id" TEXT,
	PRIMARY KEY (id),
	FOREIGN KEY(visit) REFERENCES "Visit" (id),
	FOREIGN KEY(specimen) REFERENCES "Specimen" (id),
	FOREIGN KEY(assay) REFERENCES "Assay" (id),
	FOREIGN KEY(analyte) REFERENCES "Analyte" (id),
	FOREIGN KEY("ParkinsonsStudyDataset_id") REFERENCES "ParkinsonsStudyDataset" (id)
);
CREATE INDEX "ix_BiomarkerMeasurement_id" ON "BiomarkerMeasurement" (id);

