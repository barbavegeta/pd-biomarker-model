# Auto generated from pd_biomarker_model.yaml by pythongen.py version: 0.0.1
# Schema: pd_biomarker_model
#
# id: https://w3id.org/pd-biomarker-model
# description: Parkinson's disease module of the clinical biomarker core. It narrows diagnoses to parkinsonian disorders, binds clinical assessments to MDS-UPDRS, MoCA and Hoehn and Yahr, and adds instrument-specific validation rules.
# license: MIT

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Float, Integer, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URI, URIorCURIE, XSDDate

metamodel_version = "1.12.0"
version = "0.2.0"

# Namespaces
BFO = CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
HGNC = CurieNamespace('HGNC', 'http://identifiers.org/hgnc/')
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
LOINC = CurieNamespace('LOINC', 'https://loinc.org/')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
ORCID = CurieNamespace('ORCID', 'https://orcid.org/')
PATO = CurieNamespace('PATO', 'http://purl.obolibrary.org/obo/PATO_')
PRIDE = CurieNamespace('PRIDE', 'http://purl.obolibrary.org/obo/PRIDE_')
STATO = CurieNamespace('STATO', 'http://purl.obolibrary.org/obo/STATO_')
UBERON = CurieNamespace('UBERON', 'http://purl.obolibrary.org/obo/UBERON_')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
UNIPROTKB = CurieNamespace('UniProtKB', 'http://purl.uniprot.org/uniprot/')
DCTERMS = CurieNamespace('dcterms', 'http://purl.org/dc/terms/')
DOI = CurieNamespace('doi', 'https://doi.org/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PDBM = CurieNamespace('pdbm', 'https://w3id.org/pd-biomarker-model/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = PDBM


# Types

# Class references
class NamedThingId(URIorCURIE):
    pass


class StudyDatasetId(NamedThingId):
    pass


class ParkinsonsStudyDatasetId(StudyDatasetId):
    pass


class ParticipantId(NamedThingId):
    pass


class VisitId(NamedThingId):
    pass


class DiagnosisId(NamedThingId):
    pass


class ParkinsonsDiagnosisId(DiagnosisId):
    pass


class PhenotypeObservationId(NamedThingId):
    pass


class ClinicalAssessmentId(NamedThingId):
    pass


class ParkinsonsClinicalAssessmentId(ClinicalAssessmentId):
    pass


class SpecimenId(NamedThingId):
    pass


class AnalyteId(NamedThingId):
    pass


class AssayId(NamedThingId):
    pass


class BiomarkerMeasurementId(NamedThingId):
    pass


@dataclass(repr=False)
class NamedThing(YAMLRoot):
    """
    Any record with a globally unique identifier.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Thing"]
    class_class_curie: ClassVar[str] = "schema:Thing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = PDBM.NamedThing

    id: Union[str, NamedThingId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StudyDataset(NamedThing):
    """
    A versioned collection of cohort records with dataset-level metadata. Records refer to each other by identifier.
    Disease modules subclass this and narrow the ranges of its record lists.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Dataset"]
    class_class_curie: ClassVar[str] = "schema:Dataset"
    class_name: ClassVar[str] = "StudyDataset"
    class_model_uri: ClassVar[URIRef] = PDBM.StudyDataset

    id: Union[str, StudyDatasetId] = None
    title: str = None
    dataset_version: str = None
    license: Union[str, URI] = None
    created_on: Union[str, XSDDate] = None
    conforms_to: Union[str, URI] = None
    is_synthetic: Union[bool, Bool] = None
    description: Optional[str] = None
    participants: Optional[Union[dict[Union[str, ParticipantId], Union[dict, "Participant"]], list[Union[dict, "Participant"]]]] = empty_dict()
    visits: Optional[Union[dict[Union[str, VisitId], Union[dict, "Visit"]], list[Union[dict, "Visit"]]]] = empty_dict()
    diagnoses: Optional[Union[dict[Union[str, DiagnosisId], Union[dict, "Diagnosis"]], list[Union[dict, "Diagnosis"]]]] = empty_dict()
    phenotype_observations: Optional[Union[dict[Union[str, PhenotypeObservationId], Union[dict, "PhenotypeObservation"]], list[Union[dict, "PhenotypeObservation"]]]] = empty_dict()
    clinical_assessments: Optional[Union[dict[Union[str, ClinicalAssessmentId], Union[dict, "ClinicalAssessment"]], list[Union[dict, "ClinicalAssessment"]]]] = empty_dict()
    specimens: Optional[Union[dict[Union[str, SpecimenId], Union[dict, "Specimen"]], list[Union[dict, "Specimen"]]]] = empty_dict()
    analytes: Optional[Union[dict[Union[str, AnalyteId], Union[dict, "Analyte"]], list[Union[dict, "Analyte"]]]] = empty_dict()
    assays: Optional[Union[dict[Union[str, AssayId], Union[dict, "Assay"]], list[Union[dict, "Assay"]]]] = empty_dict()
    biomarker_measurements: Optional[Union[dict[Union[str, BiomarkerMeasurementId], Union[dict, "BiomarkerMeasurement"]], list[Union[dict, "BiomarkerMeasurement"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.title):
            self.MissingRequiredField("title")
        if not isinstance(self.title, str):
            self.title = str(self.title)

        if self._is_empty(self.dataset_version):
            self.MissingRequiredField("dataset_version")
        if not isinstance(self.dataset_version, str):
            self.dataset_version = str(self.dataset_version)

        if self._is_empty(self.license):
            self.MissingRequiredField("license")
        if not isinstance(self.license, URI):
            self.license = URI(self.license)

        if self._is_empty(self.created_on):
            self.MissingRequiredField("created_on")
        if not isinstance(self.created_on, XSDDate):
            self.created_on = XSDDate(self.created_on)

        if self._is_empty(self.conforms_to):
            self.MissingRequiredField("conforms_to")
        if not isinstance(self.conforms_to, URI):
            self.conforms_to = URI(self.conforms_to)

        if self._is_empty(self.is_synthetic):
            self.MissingRequiredField("is_synthetic")
        if not isinstance(self.is_synthetic, Bool):
            self.is_synthetic = Bool(self.is_synthetic)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        self._normalize_inlined_as_list(slot_name="participants", slot_type=Participant, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="visits", slot_type=Visit, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="diagnoses", slot_type=Diagnosis, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="phenotype_observations", slot_type=PhenotypeObservation, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="clinical_assessments", slot_type=ClinicalAssessment, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="specimens", slot_type=Specimen, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="analytes", slot_type=Analyte, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="assays", slot_type=Assay, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="biomarker_measurements", slot_type=BiomarkerMeasurement, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ParkinsonsStudyDataset(StudyDataset):
    """
    A study dataset whose diagnoses and assessments follow the Parkinson's module.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["ParkinsonsStudyDataset"]
    class_class_curie: ClassVar[str] = "pdbm:ParkinsonsStudyDataset"
    class_name: ClassVar[str] = "ParkinsonsStudyDataset"
    class_model_uri: ClassVar[URIRef] = PDBM.ParkinsonsStudyDataset

    id: Union[str, ParkinsonsStudyDatasetId] = None
    title: str = None
    dataset_version: str = None
    license: Union[str, URI] = None
    created_on: Union[str, XSDDate] = None
    conforms_to: Union[str, URI] = None
    is_synthetic: Union[bool, Bool] = None
    diagnoses: Optional[Union[dict[Union[str, ParkinsonsDiagnosisId], Union[dict, "ParkinsonsDiagnosis"]], list[Union[dict, "ParkinsonsDiagnosis"]]]] = empty_dict()
    clinical_assessments: Optional[Union[dict[Union[str, ParkinsonsClinicalAssessmentId], Union[dict, "ParkinsonsClinicalAssessment"]], list[Union[dict, "ParkinsonsClinicalAssessment"]]]] = empty_dict()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ParkinsonsStudyDatasetId):
            self.id = ParkinsonsStudyDatasetId(self.id)

        self._normalize_inlined_as_list(slot_name="diagnoses", slot_type=ParkinsonsDiagnosis, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="clinical_assessments", slot_type=ParkinsonsClinicalAssessment, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Participant(NamedThing):
    """
    A person enrolled in the study.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["Person"]
    class_class_curie: ClassVar[str] = "schema:Person"
    class_name: ClassVar[str] = "Participant"
    class_model_uri: ClassVar[URIRef] = PDBM.Participant

    id: Union[str, ParticipantId] = None
    cohort: Union[str, "CohortEnum"] = None
    enrolment_date: Union[str, XSDDate] = None
    sex: Optional[Union[str, "SexEnum"]] = None
    year_of_birth: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ParticipantId):
            self.id = ParticipantId(self.id)

        if self._is_empty(self.cohort):
            self.MissingRequiredField("cohort")
        if not isinstance(self.cohort, CohortEnum):
            self.cohort = CohortEnum(self.cohort)

        if self._is_empty(self.enrolment_date):
            self.MissingRequiredField("enrolment_date")
        if not isinstance(self.enrolment_date, XSDDate):
            self.enrolment_date = XSDDate(self.enrolment_date)

        if self.sex is not None and not isinstance(self.sex, SexEnum):
            self.sex = SexEnum(self.sex)

        if self.year_of_birth is not None and not isinstance(self.year_of_birth, int):
            self.year_of_birth = int(self.year_of_birth)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Visit(NamedThing):
    """
    A scheduled study visit at which data and specimens are collected.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["Visit"]
    class_class_curie: ClassVar[str] = "pdbm:Visit"
    class_name: ClassVar[str] = "Visit"
    class_model_uri: ClassVar[URIRef] = PDBM.Visit

    id: Union[str, VisitId] = None
    participant: Union[str, ParticipantId] = None
    visit_code: str = None
    visit_date: Union[str, XSDDate] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VisitId):
            self.id = VisitId(self.id)

        if self._is_empty(self.participant):
            self.MissingRequiredField("participant")
        if not isinstance(self.participant, ParticipantId):
            self.participant = ParticipantId(self.participant)

        if self._is_empty(self.visit_code):
            self.MissingRequiredField("visit_code")
        if not isinstance(self.visit_code, str):
            self.visit_code = str(self.visit_code)

        if self._is_empty(self.visit_date):
            self.MissingRequiredField("visit_date")
        if not isinstance(self.visit_date, XSDDate):
            self.visit_date = XSDDate(self.visit_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Diagnosis(NamedThing):
    """
    A clinical diagnosis recorded for a participant. Disease modules subclass this and bind the condition to their own
    value set.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["Diagnosis"]
    class_class_curie: ClassVar[str] = "pdbm:Diagnosis"
    class_name: ClassVar[str] = "Diagnosis"
    class_model_uri: ClassVar[URIRef] = PDBM.Diagnosis

    id: Union[str, DiagnosisId] = None
    participant: Union[str, ParticipantId] = None
    condition: Union[str, "DiseaseEnum"] = None
    age_at_symptom_onset: Optional[float] = None
    age_at_diagnosis: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.participant):
            self.MissingRequiredField("participant")
        if not isinstance(self.participant, ParticipantId):
            self.participant = ParticipantId(self.participant)

        if self.age_at_symptom_onset is not None and not isinstance(self.age_at_symptom_onset, float):
            self.age_at_symptom_onset = float(self.age_at_symptom_onset)

        if self.age_at_diagnosis is not None and not isinstance(self.age_at_diagnosis, float):
            self.age_at_diagnosis = float(self.age_at_diagnosis)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ParkinsonsDiagnosis(Diagnosis):
    """
    Diagnosis of a parkinsonian disorder, with the clinical criteria used and their level of certainty.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["ParkinsonsDiagnosis"]
    class_class_curie: ClassVar[str] = "pdbm:ParkinsonsDiagnosis"
    class_name: ClassVar[str] = "ParkinsonsDiagnosis"
    class_model_uri: ClassVar[URIRef] = PDBM.ParkinsonsDiagnosis

    id: Union[str, ParkinsonsDiagnosisId] = None
    participant: Union[str, ParticipantId] = None
    diagnostic_criteria: Union[str, "DiagnosticCriteriaEnum"] = None
    condition: Union[str, "ParkinsonianDisorderEnum"] = None
    diagnostic_certainty: Optional[Union[str, "DiagnosticCertaintyEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ParkinsonsDiagnosisId):
            self.id = ParkinsonsDiagnosisId(self.id)

        if self._is_empty(self.diagnostic_criteria):
            self.MissingRequiredField("diagnostic_criteria")
        if not isinstance(self.diagnostic_criteria, DiagnosticCriteriaEnum):
            self.diagnostic_criteria = DiagnosticCriteriaEnum(self.diagnostic_criteria)

        if self.diagnostic_certainty is not None and not isinstance(self.diagnostic_certainty, DiagnosticCertaintyEnum):
            self.diagnostic_certainty = DiagnosticCertaintyEnum(self.diagnostic_certainty)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhenotypeObservation(NamedThing):
    """
    A phenotypic feature assessed at a visit, recorded as present or explicitly excluded.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["PhenotypeObservation"]
    class_class_curie: ClassVar[str] = "pdbm:PhenotypeObservation"
    class_name: ClassVar[str] = "PhenotypeObservation"
    class_model_uri: ClassVar[URIRef] = PDBM.PhenotypeObservation

    id: Union[str, PhenotypeObservationId] = None
    visit: Union[str, VisitId] = None
    phenotype: Union[str, "PhenotypeEnum"] = None
    excluded: Optional[Union[bool, Bool]] = False

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhenotypeObservationId):
            self.id = PhenotypeObservationId(self.id)

        if self._is_empty(self.visit):
            self.MissingRequiredField("visit")
        if not isinstance(self.visit, VisitId):
            self.visit = VisitId(self.visit)

        if self.excluded is not None and not isinstance(self.excluded, Bool):
            self.excluded = Bool(self.excluded)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClinicalAssessment(NamedThing):
    """
    The total score of a clinical rating scale administered at a visit. Disease modules subclass this and bind the
    instrument to their own value set.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["ClinicalAssessment"]
    class_class_curie: ClassVar[str] = "pdbm:ClinicalAssessment"
    class_name: ClassVar[str] = "ClinicalAssessment"
    class_model_uri: ClassVar[URIRef] = PDBM.ClinicalAssessment

    id: Union[str, ClinicalAssessmentId] = None
    visit: Union[str, VisitId] = None
    instrument: str = None
    score: float = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.visit):
            self.MissingRequiredField("visit")
        if not isinstance(self.visit, VisitId):
            self.visit = VisitId(self.visit)

        if self._is_empty(self.instrument):
            self.MissingRequiredField("instrument")
        if not isinstance(self.instrument, str):
            self.instrument = str(self.instrument)

        if self._is_empty(self.score):
            self.MissingRequiredField("score")
        if not isinstance(self.score, float):
            self.score = float(self.score)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ParkinsonsClinicalAssessment(ClinicalAssessment):
    """
    Total score on a Parkinson's rating scale, with the dopaminergic medication state at the time of a motor
    examination.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["ParkinsonsClinicalAssessment"]
    class_class_curie: ClassVar[str] = "pdbm:ParkinsonsClinicalAssessment"
    class_name: ClassVar[str] = "ParkinsonsClinicalAssessment"
    class_model_uri: ClassVar[URIRef] = PDBM.ParkinsonsClinicalAssessment

    id: Union[str, ParkinsonsClinicalAssessmentId] = None
    visit: Union[str, VisitId] = None
    score: float = None
    instrument: Union[str, "ParkinsonsInstrumentEnum"] = None
    medication_state: Optional[Union[str, "MedicationStateEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ParkinsonsClinicalAssessmentId):
            self.id = ParkinsonsClinicalAssessmentId(self.id)

        if self._is_empty(self.instrument):
            self.MissingRequiredField("instrument")
        if not isinstance(self.instrument, ParkinsonsInstrumentEnum):
            self.instrument = ParkinsonsInstrumentEnum(self.instrument)

        if self.medication_state is not None and not isinstance(self.medication_state, MedicationStateEnum):
            self.medication_state = MedicationStateEnum(self.medication_state)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Specimen(NamedThing):
    """
    A biological sample collected at a visit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["Specimen"]
    class_class_curie: ClassVar[str] = "pdbm:Specimen"
    class_name: ClassVar[str] = "Specimen"
    class_model_uri: ClassVar[URIRef] = PDBM.Specimen

    id: Union[str, SpecimenId] = None
    visit: Union[str, VisitId] = None
    specimen_type: Union[str, "SpecimenTypeEnum"] = None
    freeze_thaw_cycles: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SpecimenId):
            self.id = SpecimenId(self.id)

        if self._is_empty(self.visit):
            self.MissingRequiredField("visit")
        if not isinstance(self.visit, VisitId):
            self.visit = VisitId(self.visit)

        if self._is_empty(self.specimen_type):
            self.MissingRequiredField("specimen_type")
        if not isinstance(self.specimen_type, SpecimenTypeEnum):
            self.specimen_type = SpecimenTypeEnum(self.specimen_type)

        if self.freeze_thaw_cycles is not None and not isinstance(self.freeze_thaw_cycles, int):
            self.freeze_thaw_cycles = int(self.freeze_thaw_cycles)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Analyte(NamedThing):
    """
    The molecular entity a measurement quantifies, identified by its UniProtKB accession so that values from different
    platforms can be linked to the same protein.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["Analyte"]
    class_class_curie: ClassVar[str] = "pdbm:Analyte"
    class_name: ClassVar[str] = "Analyte"
    class_model_uri: ClassVar[URIRef] = PDBM.Analyte

    id: Union[str, AnalyteId] = None
    label: str = None
    gene_symbol: Optional[str] = None
    hgnc_id: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnalyteId):
            self.id = AnalyteId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self.gene_symbol is not None and not isinstance(self.gene_symbol, str):
            self.gene_symbol = str(self.gene_symbol)

        if self.hgnc_id is not None and not isinstance(self.hgnc_id, URIorCURIE):
            self.hgnc_id = URIorCURIE(self.hgnc_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Assay(NamedThing):
    """
    A measurement procedure, defined by its technology and platform.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["Assay"]
    class_class_curie: ClassVar[str] = "pdbm:Assay"
    class_name: ClassVar[str] = "Assay"
    class_model_uri: ClassVar[URIRef] = PDBM.Assay

    id: Union[str, AssayId] = None
    label: str = None
    technology: Union[str, "AssayTechnologyEnum"] = None
    platform: Optional[Union[str, "PlatformEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AssayId):
            self.id = AssayId(self.id)

        if self._is_empty(self.label):
            self.MissingRequiredField("label")
        if not isinstance(self.label, str):
            self.label = str(self.label)

        if self._is_empty(self.technology):
            self.MissingRequiredField("technology")
        if not isinstance(self.technology, AssayTechnologyEnum):
            self.technology = AssayTechnologyEnum(self.technology)

        if self.platform is not None and not isinstance(self.platform, PlatformEnum):
            self.platform = PlatformEnum(self.platform)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BiomarkerMeasurement(NamedThing):
    """
    One biomarker value for one analyte at one visit, from a specimen (fluid or tissue) or from imaging.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["BiomarkerMeasurement"]
    class_class_curie: ClassVar[str] = "pdbm:BiomarkerMeasurement"
    class_name: ClassVar[str] = "BiomarkerMeasurement"
    class_model_uri: ClassVar[URIRef] = PDBM.BiomarkerMeasurement

    id: Union[str, BiomarkerMeasurementId] = None
    visit: Union[str, VisitId] = None
    assay: Union[str, AssayId] = None
    analyte: Union[str, AnalyteId] = None
    modality: Union[str, "ModalityEnum"] = None
    measurement_type: Union[str, "MeasurementTypeEnum"] = None
    source: str = None
    curation_date: Union[str, XSDDate] = None
    curator: Union[str, URIorCURIE] = None
    curator_type: Union[str, "CuratorTypeEnum"] = None
    specimen: Optional[Union[str, SpecimenId]] = None
    platform_probe_id: Optional[str] = None
    loinc_code: Optional[Union[str, URIorCURIE]] = None
    value: Optional[float] = None
    unit: Optional[Union[str, "UnitEnum"]] = None
    categorical_result: Optional[Union[str, "CategoricalResultEnum"]] = None
    below_lloq: Optional[Union[bool, Bool]] = None
    brain_region: Optional[Union[str, "BrainRegionEnum"]] = None
    laterality: Optional[Union[str, "LateralityEnum"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiomarkerMeasurementId):
            self.id = BiomarkerMeasurementId(self.id)

        if self._is_empty(self.visit):
            self.MissingRequiredField("visit")
        if not isinstance(self.visit, VisitId):
            self.visit = VisitId(self.visit)

        if self._is_empty(self.assay):
            self.MissingRequiredField("assay")
        if not isinstance(self.assay, AssayId):
            self.assay = AssayId(self.assay)

        if self._is_empty(self.analyte):
            self.MissingRequiredField("analyte")
        if not isinstance(self.analyte, AnalyteId):
            self.analyte = AnalyteId(self.analyte)

        if self._is_empty(self.modality):
            self.MissingRequiredField("modality")
        if not isinstance(self.modality, ModalityEnum):
            self.modality = ModalityEnum(self.modality)

        if self._is_empty(self.measurement_type):
            self.MissingRequiredField("measurement_type")
        if not isinstance(self.measurement_type, MeasurementTypeEnum):
            self.measurement_type = MeasurementTypeEnum(self.measurement_type)

        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, str):
            self.source = str(self.source)

        if self._is_empty(self.curation_date):
            self.MissingRequiredField("curation_date")
        if not isinstance(self.curation_date, XSDDate):
            self.curation_date = XSDDate(self.curation_date)

        if self._is_empty(self.curator):
            self.MissingRequiredField("curator")
        if not isinstance(self.curator, URIorCURIE):
            self.curator = URIorCURIE(self.curator)

        if self._is_empty(self.curator_type):
            self.MissingRequiredField("curator_type")
        if not isinstance(self.curator_type, CuratorTypeEnum):
            self.curator_type = CuratorTypeEnum(self.curator_type)

        if self.specimen is not None and not isinstance(self.specimen, SpecimenId):
            self.specimen = SpecimenId(self.specimen)

        if self.platform_probe_id is not None and not isinstance(self.platform_probe_id, str):
            self.platform_probe_id = str(self.platform_probe_id)

        if self.loinc_code is not None and not isinstance(self.loinc_code, URIorCURIE):
            self.loinc_code = URIorCURIE(self.loinc_code)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.unit is not None and not isinstance(self.unit, UnitEnum):
            self.unit = UnitEnum(self.unit)

        if self.categorical_result is not None and not isinstance(self.categorical_result, CategoricalResultEnum):
            self.categorical_result = CategoricalResultEnum(self.categorical_result)

        if self.below_lloq is not None and not isinstance(self.below_lloq, Bool):
            self.below_lloq = Bool(self.below_lloq)

        if self.laterality is not None and not isinstance(self.laterality, LateralityEnum):
            self.laterality = LateralityEnum(self.laterality)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProvenanceMixin(YAMLRoot):
    """
    Who curated a record, when, from which source, and whether the curator was a person or an AI agent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = PDBM["ProvenanceMixin"]
    class_class_curie: ClassVar[str] = "pdbm:ProvenanceMixin"
    class_name: ClassVar[str] = "ProvenanceMixin"
    class_model_uri: ClassVar[URIRef] = PDBM.ProvenanceMixin

    source: str = None
    curation_date: Union[str, XSDDate] = None
    curator: Union[str, URIorCURIE] = None
    curator_type: Union[str, "CuratorTypeEnum"] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.source):
            self.MissingRequiredField("source")
        if not isinstance(self.source, str):
            self.source = str(self.source)

        if self._is_empty(self.curation_date):
            self.MissingRequiredField("curation_date")
        if not isinstance(self.curation_date, XSDDate):
            self.curation_date = XSDDate(self.curation_date)

        if self._is_empty(self.curator):
            self.MissingRequiredField("curator")
        if not isinstance(self.curator, URIorCURIE):
            self.curator = URIorCURIE(self.curator)

        if self._is_empty(self.curator_type):
            self.MissingRequiredField("curator_type")
        if not isinstance(self.curator_type, CuratorTypeEnum):
            self.curator_type = CuratorTypeEnum(self.curator_type)

        super().__post_init__(**kwargs)


# Enumerations
class ParkinsonianDisorderEnum(EnumDefinitionImpl):
    """
    Parkinson disease and the atypical parkinsonian disorders it is most often distinguished from. MONDO files
    multiple system atrophy and Lewy body dementia under synucleinopathy, and progressive supranuclear palsy under
    movement disorder, rather than under parkinsonian disorder, so each is listed as its own root.
    """
    _defn = EnumDefinition(
        name="ParkinsonianDisorderEnum",
        description="""Parkinson disease and the atypical parkinsonian disorders it is most often distinguished from. MONDO files multiple system atrophy and Lewy body dementia under synucleinopathy, and progressive supranuclear palsy under movement disorder, rather than under parkinsonian disorder, so each is listed as its own root.""",
    )

class ParkinsonsInstrumentEnum(EnumDefinitionImpl):
    """
    Rating scale totals recorded in Parkinson's studies. LOINC covers the MoCA total but not MDS-UPDRS: its UPDRS
    codes describe the original 1987 scale, which has different items and ranges.
    """
    MDS_UPDRS_PART_I = PermissibleValue(
        text="MDS_UPDRS_PART_I",
        description="MDS-UPDRS Part I (non-motor experiences of daily living) total, 0-52.")
    MDS_UPDRS_PART_II = PermissibleValue(
        text="MDS_UPDRS_PART_II",
        description="MDS-UPDRS Part II (motor experiences of daily living) total, 0-52.")
    MDS_UPDRS_PART_III = PermissibleValue(
        text="MDS_UPDRS_PART_III",
        description="MDS-UPDRS Part III (motor examination) total, 0-132.")
    MDS_UPDRS_PART_IV = PermissibleValue(
        text="MDS_UPDRS_PART_IV",
        description="MDS-UPDRS Part IV (motor complications) total, 0-24.")
    HOEHN_YAHR = PermissibleValue(
        text="HOEHN_YAHR",
        title="MDS-UPDRS - Hoehn and Yahr Stage",
        description="Hoehn and Yahr stage as rated in MDS-UPDRS, 0-5.",
        meaning=NCIT["C100535"])
    MOCA = PermissibleValue(
        text="MOCA",
        title="Total score [MoCA]",
        description="Montreal Cognitive Assessment total score, 0-30.",
        meaning=LOINC["72172-0"])

    _defn = EnumDefinition(
        name="ParkinsonsInstrumentEnum",
        description="""Rating scale totals recorded in Parkinson's studies. LOINC covers the MoCA total but not MDS-UPDRS: its UPDRS codes describe the original 1987 scale, which has different items and ranges.""",
    )

class DiagnosticCriteriaEnum(EnumDefinitionImpl):
    """
    Published clinical diagnostic criteria for parkinsonian disorders.
    """
    MDS_PD_2015 = PermissibleValue(
        text="MDS_PD_2015",
        description="MDS clinical diagnostic criteria for Parkinson's disease (Postuma et al., 2015).")
    UK_PDS_BRAIN_BANK = PermissibleValue(
        text="UK_PDS_BRAIN_BANK",
        description="UK Parkinson's Disease Society Brain Bank criteria (Hughes et al., 1992).")
    MDS_MSA_2022 = PermissibleValue(
        text="MDS_MSA_2022",
        description="MDS criteria for multiple system atrophy (Wenning et al., 2022).")
    MDS_PSP_2017 = PermissibleValue(
        text="MDS_PSP_2017",
        description="MDS criteria for progressive supranuclear palsy (Höglinger et al., 2017).")
    DLB_CONSORTIUM_2017 = PermissibleValue(
        text="DLB_CONSORTIUM_2017",
        description="Fourth consensus report of the DLB Consortium (McKeith et al., 2017).")

    _defn = EnumDefinition(
        name="DiagnosticCriteriaEnum",
        description="Published clinical diagnostic criteria for parkinsonian disorders.",
    )

class DiagnosticCertaintyEnum(EnumDefinitionImpl):
    """
    Level of diagnostic certainty defined by the criteria.
    """
    CLINICALLY_ESTABLISHED = PermissibleValue(
        text="CLINICALLY_ESTABLISHED",
        description="Clinically established (MDS PD and MSA criteria).")
    PROBABLE = PermissibleValue(
        text="PROBABLE",
        description="Probable.")
    POSSIBLE = PermissibleValue(
        text="POSSIBLE",
        description="Possible (PSP and DLB criteria).")

    _defn = EnumDefinition(
        name="DiagnosticCertaintyEnum",
        description="Level of diagnostic certainty defined by the criteria.",
    )

class MedicationStateEnum(EnumDefinitionImpl):
    """
    Dopaminergic medication state during a motor examination.
    """
    ON = PermissibleValue(
        text="ON",
        description="Examined while responding to dopaminergic medication.")
    OFF = PermissibleValue(
        text="OFF",
        description="Examined after withholding dopaminergic medication.")
    UNTREATED = PermissibleValue(
        text="UNTREATED",
        description="Not yet taking dopaminergic medication.")

    _defn = EnumDefinition(
        name="MedicationStateEnum",
        description="Dopaminergic medication state during a motor examination.",
    )

class CohortEnum(EnumDefinitionImpl):
    """
    Study arm a participant was enrolled in.
    """
    CASE = PermissibleValue(
        text="CASE",
        title="Participant Case",
        description="Enrolled because they have the condition under study.",
        meaning=NCIT["C216103"])
    HEALTHY_CONTROL = PermissibleValue(
        text="HEALTHY_CONTROL",
        title="Healthy Control",
        description="Enrolled as a healthy comparison participant.",
        meaning=NCIT["C94342"])
    PRODROMAL = PermissibleValue(
        text="PRODROMAL",
        title="Prodromal Phase of Disease",
        description="Enrolled with prodromal features but no diagnosis.",
        meaning=NCIT["C209884"])

    _defn = EnumDefinition(
        name="CohortEnum",
        description="Study arm a participant was enrolled in.",
    )

class SexEnum(EnumDefinitionImpl):
    """
    Biological sex.
    """
    FEMALE = PermissibleValue(
        text="FEMALE",
        title="female",
        description="Female.",
        meaning=PATO["0000383"])
    MALE = PermissibleValue(
        text="MALE",
        title="male",
        description="Male.",
        meaning=PATO["0000384"])

    _defn = EnumDefinition(
        name="SexEnum",
        description="Biological sex.",
    )

class DiseaseEnum(EnumDefinitionImpl):
    """
    Any disease in MONDO.
    """
    _defn = EnumDefinition(
        name="DiseaseEnum",
        description="Any disease in MONDO.",
    )

class PhenotypeEnum(EnumDefinitionImpl):
    """
    Any phenotypic abnormality in HPO.
    """
    _defn = EnumDefinition(
        name="PhenotypeEnum",
        description="Any phenotypic abnormality in HPO.",
    )

class SpecimenTypeEnum(EnumDefinitionImpl):
    """
    Anatomical material a specimen consists of.
    """
    CSF = PermissibleValue(
        text="CSF",
        title="cerebrospinal fluid",
        description="Cerebrospinal fluid.",
        meaning=UBERON["0001359"])
    PLASMA = PermissibleValue(
        text="PLASMA",
        title="blood plasma",
        description="Blood plasma.",
        meaning=UBERON["0001969"])
    SERUM = PermissibleValue(
        text="SERUM",
        title="blood serum",
        description="Blood serum.",
        meaning=UBERON["0001977"])
    WHOLE_BLOOD = PermissibleValue(
        text="WHOLE_BLOOD",
        title="blood",
        description="Whole blood.",
        meaning=UBERON["0000178"])
    SKIN = PermissibleValue(
        text="SKIN",
        title="skin of body",
        description="Skin biopsy.",
        meaning=UBERON["0002097"])

    _defn = EnumDefinition(
        name="SpecimenTypeEnum",
        description="Anatomical material a specimen consists of.",
    )

class BrainRegionEnum(EnumDefinitionImpl):
    """
    Any part of the brain in UBERON.
    """
    _defn = EnumDefinition(
        name="BrainRegionEnum",
        description="Any part of the brain in UBERON.",
    )

class LateralityEnum(EnumDefinitionImpl):
    """
    Side of the body.
    """
    LEFT = PermissibleValue(
        text="LEFT",
        title="left",
        description="Left side.",
        meaning=PATO["0000366"])
    RIGHT = PermissibleValue(
        text="RIGHT",
        title="right",
        description="Right side.",
        meaning=PATO["0000367"])
    BILATERAL = PermissibleValue(
        text="BILATERAL",
        title="bilateral",
        description="Both sides, reported as the mean of left and right.",
        meaning=PATO["0000618"])

    _defn = EnumDefinition(
        name="LateralityEnum",
        description="Side of the body.",
    )

class ModalityEnum(EnumDefinitionImpl):
    """
    Source of a biomarker value.
    """
    SPECIMEN = PermissibleValue(
        text="SPECIMEN",
        description="Measured in a fluid or tissue specimen.")
    IMAGING = PermissibleValue(
        text="IMAGING",
        title="imaging assay",
        description="Measured from an imaging scan.",
        meaning=OBI["0000185"])

    _defn = EnumDefinition(
        name="ModalityEnum",
        description="Source of a biomarker value.",
    )

class MeasurementTypeEnum(EnumDefinitionImpl):
    """
    Kind of quantity a biomarker value represents.
    """
    CONCENTRATION = PermissibleValue(
        text="CONCENTRATION",
        title="concentration of",
        description="Absolute amount per volume, e.g. pg/mL.",
        meaning=PATO["0000033"])
    RELATIVE_ABUNDANCE = PermissibleValue(
        text="RELATIVE_ABUNDANCE",
        description="""Platform-relative signal that is not an absolute concentration, e.g. SomaScan RFU or Olink NPX.""")
    RATIO = PermissibleValue(
        text="RATIO",
        title="ratio",
        description="Dimensionless ratio, e.g. a DaT-SPECT specific binding ratio.",
        meaning=STATO["0000184"])
    CATEGORICAL = PermissibleValue(
        text="CATEGORICAL",
        description="Qualitative result, e.g. a seed amplification assay call.")

    _defn = EnumDefinition(
        name="MeasurementTypeEnum",
        description="Kind of quantity a biomarker value represents.",
    )

class UnitEnum(EnumDefinitionImpl):
    """
    Units as case-sensitive UCUM codes. Curly-brace codes are UCUM annotations for arbitrary, platform-specific units.
    """
    _defn = EnumDefinition(
        name="UnitEnum",
        description="""Units as case-sensitive UCUM codes. Curly-brace codes are UCUM annotations for arbitrary, platform-specific units.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "pg/mL",
            PermissibleValue(
                text="pg/mL",
                title="picogram per milliliter",
                description="Picograms per millilitre.",
                meaning=UO["0010070"]))
        setattr(cls, "ng/mL",
            PermissibleValue(
                text="ng/mL",
                title="nanogram per milliliter",
                description="Nanograms per millilitre.",
                meaning=UO["0000275"]))
        setattr(cls, "1",
            PermissibleValue(
                text="1",
                title="dimensionless unit",
                description="Dimensionless (UCUM unity), used for ratios.",
                meaning=UO["0000186"]))
        setattr(cls, "{RFU}",
            PermissibleValue(
                text="{RFU}",
                title="Relative Fluorescence Intensity Unit",
                description="SomaScan relative fluorescence units.",
                meaning=NCIT["C77535"]))
        setattr(cls, "{NPX}",
            PermissibleValue(
                text="{NPX}",
                description="Olink normalised protein expression, an arbitrary log2 unit."))

class CategoricalResultEnum(EnumDefinitionImpl):
    """
    Result of a qualitative assay.
    """
    POSITIVE = PermissibleValue(
        text="POSITIVE",
        title="Positive Finding",
        description="The target was detected.",
        meaning=NCIT["C38758"])
    NEGATIVE = PermissibleValue(
        text="NEGATIVE",
        title="Negative Finding",
        description="The target was not detected.",
        meaning=NCIT["C38757"])
    INDETERMINATE = PermissibleValue(
        text="INDETERMINATE",
        title="Indeterminate",
        description="The result could not be called positive or negative.",
        meaning=NCIT["C48658"])

    _defn = EnumDefinition(
        name="CategoricalResultEnum",
        description="Result of a qualitative assay.",
    )

class AssayTechnologyEnum(EnumDefinitionImpl):
    """
    Assay technology.
    """
    ELISA = PermissibleValue(
        text="ELISA",
        title="enzyme-linked immunosorbent assay",
        description="Enzyme-linked immunosorbent assay.",
        meaning=OBI["0000661"])
    SIMOA = PermissibleValue(
        text="SIMOA",
        title="Single-Molecule Array",
        description="Single-molecule array digital immunoassay.",
        meaning=NCIT["C161406"])
    SOMASCAN = PermissibleValue(
        text="SOMASCAN",
        title="SOMAscan assay",
        description="SomaScan aptamer-based proteomic assay.",
        meaning=OBI["0003111"])
    OLINK = PermissibleValue(
        text="OLINK",
        title="Olink assay",
        description="Olink proximity extension assay.",
        meaning=OBI["0003112"])
    SEED_AMPLIFICATION_ASSAY = PermissibleValue(
        text="SEED_AMPLIFICATION_ASSAY",
        description="""Alpha-synuclein seed amplification assay (e.g. RT-QuIC). No ontology has a specific term, so only a broad mapping is given.""")
    SPECT = PermissibleValue(
        text="SPECT",
        title="Single Photon Emission Computed Tomography",
        description="Single-photon emission computed tomography.",
        meaning=NCIT["C17203"])

    _defn = EnumDefinition(
        name="AssayTechnologyEnum",
        description="Assay technology.",
    )

class PlatformEnum(EnumDefinitionImpl):
    """
    Commercial platform and panel version.
    """
    SOMASCAN_5K = PermissibleValue(
        text="SOMASCAN_5K",
        title="SomaScan 5K",
        description="SomaScan 5K panel (assay v4.0).",
        meaning=PRIDE["0000933"])
    SOMASCAN_7K = PermissibleValue(
        text="SOMASCAN_7K",
        title="SomaScan 7K",
        description="SomaScan 7K panel (assay v4.1).",
        meaning=PRIDE["0000934"])
    OLINK_EXPLORE_3072 = PermissibleValue(
        text="OLINK_EXPLORE_3072",
        title="Olink Explore 3072/384",
        description="Olink Explore 3072 panel.",
        meaning=PRIDE["0000657"])
    OLINK_EXPLORE_HT = PermissibleValue(
        text="OLINK_EXPLORE_HT",
        title="Olink Explore HT",
        description="Olink Explore HT panel.",
        meaning=PRIDE["0000673"])
    SIMOA_HD_X = PermissibleValue(
        text="SIMOA_HD_X",
        description="Quanterix Simoa HD-X analyser. No ontology term exists.")
    DAT_SPECT_IOFLUPANE = PermissibleValue(
        text="DAT_SPECT_IOFLUPANE",
        description="Dopamine transporter SPECT with the tracer ioflupane (123I).")

    _defn = EnumDefinition(
        name="PlatformEnum",
        description="Commercial platform and panel version.",
    )

class CuratorTypeEnum(EnumDefinitionImpl):
    """
    Kind of agent that curated a record.
    """
    PERSON = PermissibleValue(
        text="PERSON",
        title="Person",
        description="A human curator.",
        meaning=PROV["Person"])
    AI_AGENT = PermissibleValue(
        text="AI_AGENT",
        title="SoftwareAgent",
        description="An AI agent, such as an LLM-based curation tool.",
        meaning=PROV["SoftwareAgent"])

    _defn = EnumDefinition(
        name="CuratorTypeEnum",
        description="Kind of agent that curated a record.",
    )

# Slots
class slots:
    pass

slots.diagnostic_criteria = Slot(uri=PDBM.diagnostic_criteria, name="diagnostic_criteria", curie=PDBM.curie('diagnostic_criteria'),
                   model_uri=PDBM.diagnostic_criteria, domain=None, range=Union[str, "DiagnosticCriteriaEnum"])

slots.diagnostic_certainty = Slot(uri=PDBM.diagnostic_certainty, name="diagnostic_certainty", curie=PDBM.curie('diagnostic_certainty'),
                   model_uri=PDBM.diagnostic_certainty, domain=None, range=Optional[Union[str, "DiagnosticCertaintyEnum"]])

slots.medication_state = Slot(uri=PDBM.medication_state, name="medication_state", curie=PDBM.curie('medication_state'),
                   model_uri=PDBM.medication_state, domain=None, range=Optional[Union[str, "MedicationStateEnum"]])

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=PDBM.id, domain=None, range=URIRef,
                   pattern=re.compile(r'^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$'))

slots.title = Slot(uri=DCTERMS.title, name="title", curie=DCTERMS.curie('title'),
                   model_uri=PDBM.title, domain=None, range=str)

slots.description = Slot(uri=DCTERMS.description, name="description", curie=DCTERMS.curie('description'),
                   model_uri=PDBM.description, domain=None, range=Optional[str])

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=PDBM.label, domain=None, range=str)

slots.dataset_version = Slot(uri=SCHEMA.version, name="dataset_version", curie=SCHEMA.curie('version'),
                   model_uri=PDBM.dataset_version, domain=None, range=str,
                   pattern=re.compile(r'^[0-9]+\.[0-9]+\.[0-9]+$'))

slots.license = Slot(uri=DCTERMS.license, name="license", curie=DCTERMS.curie('license'),
                   model_uri=PDBM.license, domain=None, range=Union[str, URI])

slots.created_on = Slot(uri=DCTERMS.created, name="created_on", curie=DCTERMS.curie('created'),
                   model_uri=PDBM.created_on, domain=None, range=Union[str, XSDDate])

slots.conforms_to = Slot(uri=DCTERMS.conformsTo, name="conforms_to", curie=DCTERMS.curie('conformsTo'),
                   model_uri=PDBM.conforms_to, domain=None, range=Union[str, URI])

slots.is_synthetic = Slot(uri=PDBM.is_synthetic, name="is_synthetic", curie=PDBM.curie('is_synthetic'),
                   model_uri=PDBM.is_synthetic, domain=None, range=Union[bool, Bool])

slots.participants = Slot(uri=PDBM.participants, name="participants", curie=PDBM.curie('participants'),
                   model_uri=PDBM.participants, domain=None, range=Optional[Union[dict[Union[str, ParticipantId], Union[dict, Participant]], list[Union[dict, Participant]]]])

slots.visits = Slot(uri=PDBM.visits, name="visits", curie=PDBM.curie('visits'),
                   model_uri=PDBM.visits, domain=None, range=Optional[Union[dict[Union[str, VisitId], Union[dict, Visit]], list[Union[dict, Visit]]]])

slots.diagnoses = Slot(uri=PDBM.diagnoses, name="diagnoses", curie=PDBM.curie('diagnoses'),
                   model_uri=PDBM.diagnoses, domain=None, range=Optional[Union[dict[Union[str, DiagnosisId], Union[dict, Diagnosis]], list[Union[dict, Diagnosis]]]])

slots.phenotype_observations = Slot(uri=PDBM.phenotype_observations, name="phenotype_observations", curie=PDBM.curie('phenotype_observations'),
                   model_uri=PDBM.phenotype_observations, domain=None, range=Optional[Union[dict[Union[str, PhenotypeObservationId], Union[dict, PhenotypeObservation]], list[Union[dict, PhenotypeObservation]]]])

slots.clinical_assessments = Slot(uri=PDBM.clinical_assessments, name="clinical_assessments", curie=PDBM.curie('clinical_assessments'),
                   model_uri=PDBM.clinical_assessments, domain=None, range=Optional[Union[dict[Union[str, ClinicalAssessmentId], Union[dict, ClinicalAssessment]], list[Union[dict, ClinicalAssessment]]]])

slots.specimens = Slot(uri=PDBM.specimens, name="specimens", curie=PDBM.curie('specimens'),
                   model_uri=PDBM.specimens, domain=None, range=Optional[Union[dict[Union[str, SpecimenId], Union[dict, Specimen]], list[Union[dict, Specimen]]]])

slots.analytes = Slot(uri=PDBM.analytes, name="analytes", curie=PDBM.curie('analytes'),
                   model_uri=PDBM.analytes, domain=None, range=Optional[Union[dict[Union[str, AnalyteId], Union[dict, Analyte]], list[Union[dict, Analyte]]]])

slots.assays = Slot(uri=PDBM.assays, name="assays", curie=PDBM.curie('assays'),
                   model_uri=PDBM.assays, domain=None, range=Optional[Union[dict[Union[str, AssayId], Union[dict, Assay]], list[Union[dict, Assay]]]])

slots.biomarker_measurements = Slot(uri=PDBM.biomarker_measurements, name="biomarker_measurements", curie=PDBM.curie('biomarker_measurements'),
                   model_uri=PDBM.biomarker_measurements, domain=None, range=Optional[Union[dict[Union[str, BiomarkerMeasurementId], Union[dict, BiomarkerMeasurement]], list[Union[dict, BiomarkerMeasurement]]]])

slots.cohort = Slot(uri=PDBM.cohort, name="cohort", curie=PDBM.curie('cohort'),
                   model_uri=PDBM.cohort, domain=None, range=Union[str, "CohortEnum"])

slots.sex = Slot(uri=PDBM.sex, name="sex", curie=PDBM.curie('sex'),
                   model_uri=PDBM.sex, domain=None, range=Optional[Union[str, "SexEnum"]])

slots.year_of_birth = Slot(uri=PDBM.year_of_birth, name="year_of_birth", curie=PDBM.curie('year_of_birth'),
                   model_uri=PDBM.year_of_birth, domain=None, range=Optional[int])

slots.enrolment_date = Slot(uri=PDBM.enrolment_date, name="enrolment_date", curie=PDBM.curie('enrolment_date'),
                   model_uri=PDBM.enrolment_date, domain=None, range=Union[str, XSDDate])

slots.participant = Slot(uri=PDBM.participant, name="participant", curie=PDBM.curie('participant'),
                   model_uri=PDBM.participant, domain=None, range=Union[str, ParticipantId])

slots.visit = Slot(uri=PDBM.visit, name="visit", curie=PDBM.curie('visit'),
                   model_uri=PDBM.visit, domain=None, range=Union[str, VisitId])

slots.visit_code = Slot(uri=PDBM.visit_code, name="visit_code", curie=PDBM.curie('visit_code'),
                   model_uri=PDBM.visit_code, domain=None, range=str,
                   pattern=re.compile(r'^M[0-9]{2,3}$'))

slots.visit_date = Slot(uri=PDBM.visit_date, name="visit_date", curie=PDBM.curie('visit_date'),
                   model_uri=PDBM.visit_date, domain=None, range=Union[str, XSDDate])

slots.condition = Slot(uri=PDBM.condition, name="condition", curie=PDBM.curie('condition'),
                   model_uri=PDBM.condition, domain=None, range=Union[str, "DiseaseEnum"])

slots.age_at_symptom_onset = Slot(uri=PDBM.age_at_symptom_onset, name="age_at_symptom_onset", curie=PDBM.curie('age_at_symptom_onset'),
                   model_uri=PDBM.age_at_symptom_onset, domain=None, range=Optional[float])

slots.age_at_diagnosis = Slot(uri=PDBM.age_at_diagnosis, name="age_at_diagnosis", curie=PDBM.curie('age_at_diagnosis'),
                   model_uri=PDBM.age_at_diagnosis, domain=None, range=Optional[float])

slots.phenotype = Slot(uri=PDBM.phenotype, name="phenotype", curie=PDBM.curie('phenotype'),
                   model_uri=PDBM.phenotype, domain=None, range=Union[str, "PhenotypeEnum"])

slots.excluded = Slot(uri=PDBM.excluded, name="excluded", curie=PDBM.curie('excluded'),
                   model_uri=PDBM.excluded, domain=None, range=Optional[Union[bool, Bool]])

slots.instrument = Slot(uri=PDBM.instrument, name="instrument", curie=PDBM.curie('instrument'),
                   model_uri=PDBM.instrument, domain=None, range=str)

slots.score = Slot(uri=PDBM.score, name="score", curie=PDBM.curie('score'),
                   model_uri=PDBM.score, domain=None, range=float)

slots.specimen_type = Slot(uri=PDBM.specimen_type, name="specimen_type", curie=PDBM.curie('specimen_type'),
                   model_uri=PDBM.specimen_type, domain=None, range=Union[str, "SpecimenTypeEnum"])

slots.freeze_thaw_cycles = Slot(uri=PDBM.freeze_thaw_cycles, name="freeze_thaw_cycles", curie=PDBM.curie('freeze_thaw_cycles'),
                   model_uri=PDBM.freeze_thaw_cycles, domain=None, range=Optional[int])

slots.gene_symbol = Slot(uri=PDBM.gene_symbol, name="gene_symbol", curie=PDBM.curie('gene_symbol'),
                   model_uri=PDBM.gene_symbol, domain=None, range=Optional[str],
                   pattern=re.compile(r'^[A-Z][A-Z0-9-]*$'))

slots.hgnc_id = Slot(uri=PDBM.hgnc_id, name="hgnc_id", curie=PDBM.curie('hgnc_id'),
                   model_uri=PDBM.hgnc_id, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^HGNC:[0-9]+$'))

slots.technology = Slot(uri=PDBM.technology, name="technology", curie=PDBM.curie('technology'),
                   model_uri=PDBM.technology, domain=None, range=Union[str, "AssayTechnologyEnum"])

slots.platform = Slot(uri=PDBM.platform, name="platform", curie=PDBM.curie('platform'),
                   model_uri=PDBM.platform, domain=None, range=Optional[Union[str, "PlatformEnum"]])

slots.specimen = Slot(uri=PDBM.specimen, name="specimen", curie=PDBM.curie('specimen'),
                   model_uri=PDBM.specimen, domain=None, range=Optional[Union[str, SpecimenId]])

slots.assay = Slot(uri=PDBM.assay, name="assay", curie=PDBM.curie('assay'),
                   model_uri=PDBM.assay, domain=None, range=Union[str, AssayId])

slots.analyte = Slot(uri=PDBM.analyte, name="analyte", curie=PDBM.curie('analyte'),
                   model_uri=PDBM.analyte, domain=None, range=Union[str, AnalyteId])

slots.platform_probe_id = Slot(uri=PDBM.platform_probe_id, name="platform_probe_id", curie=PDBM.curie('platform_probe_id'),
                   model_uri=PDBM.platform_probe_id, domain=None, range=Optional[str],
                   pattern=re.compile(r'^(seq\.[0-9]{4,5}\.[0-9]{1,3}|OID[0-9]{5})$'))

slots.loinc_code = Slot(uri=PDBM.loinc_code, name="loinc_code", curie=PDBM.curie('loinc_code'),
                   model_uri=PDBM.loinc_code, domain=None, range=Optional[Union[str, URIorCURIE]],
                   pattern=re.compile(r'^LOINC:[0-9]{1,7}-[0-9]$'))

slots.modality = Slot(uri=PDBM.modality, name="modality", curie=PDBM.curie('modality'),
                   model_uri=PDBM.modality, domain=None, range=Union[str, "ModalityEnum"])

slots.measurement_type = Slot(uri=PDBM.measurement_type, name="measurement_type", curie=PDBM.curie('measurement_type'),
                   model_uri=PDBM.measurement_type, domain=None, range=Union[str, "MeasurementTypeEnum"])

slots.value = Slot(uri=PDBM.value, name="value", curie=PDBM.curie('value'),
                   model_uri=PDBM.value, domain=None, range=Optional[float])

slots.unit = Slot(uri=PDBM.unit, name="unit", curie=PDBM.curie('unit'),
                   model_uri=PDBM.unit, domain=None, range=Optional[Union[str, "UnitEnum"]])

slots.categorical_result = Slot(uri=PDBM.categorical_result, name="categorical_result", curie=PDBM.curie('categorical_result'),
                   model_uri=PDBM.categorical_result, domain=None, range=Optional[Union[str, "CategoricalResultEnum"]])

slots.below_lloq = Slot(uri=PDBM.below_lloq, name="below_lloq", curie=PDBM.curie('below_lloq'),
                   model_uri=PDBM.below_lloq, domain=None, range=Optional[Union[bool, Bool]])

slots.brain_region = Slot(uri=PDBM.brain_region, name="brain_region", curie=PDBM.curie('brain_region'),
                   model_uri=PDBM.brain_region, domain=None, range=Optional[Union[str, "BrainRegionEnum"]])

slots.laterality = Slot(uri=PDBM.laterality, name="laterality", curie=PDBM.curie('laterality'),
                   model_uri=PDBM.laterality, domain=None, range=Optional[Union[str, "LateralityEnum"]])

slots.source = Slot(uri=PROV.hadPrimarySource, name="source", curie=PROV.curie('hadPrimarySource'),
                   model_uri=PDBM.source, domain=None, range=str)

slots.curation_date = Slot(uri=PROV.generatedAtTime, name="curation_date", curie=PROV.curie('generatedAtTime'),
                   model_uri=PDBM.curation_date, domain=None, range=Union[str, XSDDate])

slots.curator = Slot(uri=PROV.wasAttributedTo, name="curator", curie=PROV.curie('wasAttributedTo'),
                   model_uri=PDBM.curator, domain=None, range=Union[str, URIorCURIE])

slots.curator_type = Slot(uri=PDBM.curator_type, name="curator_type", curie=PDBM.curie('curator_type'),
                   model_uri=PDBM.curator_type, domain=None, range=Union[str, "CuratorTypeEnum"])

slots.ParkinsonsStudyDataset_diagnoses = Slot(uri=PDBM.diagnoses, name="ParkinsonsStudyDataset_diagnoses", curie=PDBM.curie('diagnoses'),
                   model_uri=PDBM.ParkinsonsStudyDataset_diagnoses, domain=ParkinsonsStudyDataset, range=Optional[Union[dict[Union[str, ParkinsonsDiagnosisId], Union[dict, "ParkinsonsDiagnosis"]], list[Union[dict, "ParkinsonsDiagnosis"]]]])

slots.ParkinsonsStudyDataset_clinical_assessments = Slot(uri=PDBM.clinical_assessments, name="ParkinsonsStudyDataset_clinical_assessments", curie=PDBM.curie('clinical_assessments'),
                   model_uri=PDBM.ParkinsonsStudyDataset_clinical_assessments, domain=ParkinsonsStudyDataset, range=Optional[Union[dict[Union[str, ParkinsonsClinicalAssessmentId], Union[dict, "ParkinsonsClinicalAssessment"]], list[Union[dict, "ParkinsonsClinicalAssessment"]]]])

slots.ParkinsonsDiagnosis_condition = Slot(uri=PDBM.condition, name="ParkinsonsDiagnosis_condition", curie=PDBM.curie('condition'),
                   model_uri=PDBM.ParkinsonsDiagnosis_condition, domain=ParkinsonsDiagnosis, range=Union[str, "ParkinsonianDisorderEnum"])

slots.ParkinsonsClinicalAssessment_instrument = Slot(uri=PDBM.instrument, name="ParkinsonsClinicalAssessment_instrument", curie=PDBM.curie('instrument'),
                   model_uri=PDBM.ParkinsonsClinicalAssessment_instrument, domain=ParkinsonsClinicalAssessment, range=Union[str, "ParkinsonsInstrumentEnum"])

slots.Analyte_id = Slot(uri=SCHEMA.identifier, name="Analyte_id", curie=SCHEMA.curie('identifier'),
                   model_uri=PDBM.Analyte_id, domain=Analyte, range=Union[str, AnalyteId],
                   pattern=re.compile(r'^UniProtKB:([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$'))
