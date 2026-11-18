from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.12.0"
version = "0.1.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'pdbm',
     'default_range': 'string',
     'description': "Parkinson's disease module of the clinical biomarker core. It "
                    'narrows diagnoses to parkinsonian disorders, binds clinical '
                    'assessments to MDS-UPDRS, MoCA and Hoehn and Yahr, and adds '
                    'instrument-specific validation rules.',
     'id': 'https://w3id.org/pd-biomarker-model',
     'imports': ['linkml:types', 'core'],
     'license': 'MIT',
     'name': 'pd_biomarker_model',
     'prefixes': {'BFO': {'prefix_prefix': 'BFO',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/BFO_'},
                  'CHEBI': {'prefix_prefix': 'CHEBI',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/CHEBI_'},
                  'HGNC': {'prefix_prefix': 'HGNC',
                           'prefix_reference': 'http://identifiers.org/hgnc/'},
                  'HP': {'prefix_prefix': 'HP',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/HP_'},
                  'LOINC': {'prefix_prefix': 'LOINC',
                            'prefix_reference': 'https://loinc.org/'},
                  'MONDO': {'prefix_prefix': 'MONDO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/MONDO_'},
                  'NCIT': {'prefix_prefix': 'NCIT',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/NCIT_'},
                  'OBI': {'prefix_prefix': 'OBI',
                          'prefix_reference': 'http://purl.obolibrary.org/obo/OBI_'},
                  'ORCID': {'prefix_prefix': 'ORCID',
                            'prefix_reference': 'https://orcid.org/'},
                  'PATO': {'prefix_prefix': 'PATO',
                           'prefix_reference': 'http://purl.obolibrary.org/obo/PATO_'},
                  'PRIDE': {'prefix_prefix': 'PRIDE',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/PRIDE_'},
                  'STATO': {'prefix_prefix': 'STATO',
                            'prefix_reference': 'http://purl.obolibrary.org/obo/STATO_'},
                  'UBERON': {'prefix_prefix': 'UBERON',
                             'prefix_reference': 'http://purl.obolibrary.org/obo/UBERON_'},
                  'UO': {'prefix_prefix': 'UO',
                         'prefix_reference': 'http://purl.obolibrary.org/obo/UO_'},
                  'UniProtKB': {'prefix_prefix': 'UniProtKB',
                                'prefix_reference': 'http://purl.uniprot.org/uniprot/'},
                  'dcterms': {'prefix_prefix': 'dcterms',
                              'prefix_reference': 'http://purl.org/dc/terms/'},
                  'doi': {'prefix_prefix': 'doi',
                          'prefix_reference': 'https://doi.org/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'pdbm': {'prefix_prefix': 'pdbm',
                           'prefix_reference': 'https://w3id.org/pd-biomarker-model/'},
                  'prov': {'prefix_prefix': 'prov',
                           'prefix_reference': 'http://www.w3.org/ns/prov#'},
                  'rdfs': {'prefix_prefix': 'rdfs',
                           'prefix_reference': 'http://www.w3.org/2000/01/rdf-schema#'},
                  'schema': {'prefix_prefix': 'schema',
                             'prefix_reference': 'http://schema.org/'}},
     'see_also': ['https://barbavegeta.github.io/pd-biomarker-model'],
     'source_file': 'src/pd_biomarker_model/schema/pd_biomarker_model.yaml',
     'title': "Parkinson's disease biomarker model"} )

class CohortEnum(str, Enum):
    """
    Study arm a participant was enrolled in.
    """
    Participant_Case = "CASE"
    """
    Enrolled because they have the condition under study.
    """
    Healthy_Control = "HEALTHY_CONTROL"
    """
    Enrolled as a healthy comparison participant.
    """
    Prodromal_Phase_of_Disease = "PRODROMAL"
    """
    Enrolled with prodromal features but no diagnosis.
    """


class SexEnum(str, Enum):
    """
    Biological sex.
    """
    female = "FEMALE"
    """
    Female.
    """
    male = "MALE"
    """
    Male.
    """


class DiseaseEnum(str):
    """
    Any disease in MONDO.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class PhenotypeEnum(str):
    """
    Any phenotypic abnormality in HPO.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class SpecimenTypeEnum(str, Enum):
    """
    Anatomical material a specimen consists of.
    """
    cerebrospinal_fluid = "CSF"
    """
    Cerebrospinal fluid.
    """
    blood_plasma = "PLASMA"
    """
    Blood plasma.
    """
    blood_serum = "SERUM"
    """
    Blood serum.
    """
    blood = "WHOLE_BLOOD"
    """
    Whole blood.
    """
    skin_of_body = "SKIN"
    """
    Skin biopsy.
    """


class BrainRegionEnum(str):
    """
    Any part of the brain in UBERON.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class LateralityEnum(str, Enum):
    """
    Side of the body.
    """
    left = "LEFT"
    """
    Left side.
    """
    right = "RIGHT"
    """
    Right side.
    """
    bilateral = "BILATERAL"
    """
    Both sides, reported as the mean of left and right.
    """


class ModalityEnum(str, Enum):
    """
    Source of a biomarker value.
    """
    SPECIMEN = "SPECIMEN"
    """
    Measured in a fluid or tissue specimen.
    """
    imaging_assay = "IMAGING"
    """
    Measured from an imaging scan.
    """


class MeasurementTypeEnum(str, Enum):
    """
    Kind of quantity a biomarker value represents.
    """
    concentration_of = "CONCENTRATION"
    """
    Absolute amount per volume, e.g. pg/mL.
    """
    RELATIVE_ABUNDANCE = "RELATIVE_ABUNDANCE"
    """
    Platform-relative signal that is not an absolute concentration, e.g. SomaScan RFU or Olink NPX.
    """
    ratio = "RATIO"
    """
    Dimensionless ratio, e.g. a DaT-SPECT specific binding ratio.
    """
    CATEGORICAL = "CATEGORICAL"
    """
    Qualitative result, e.g. a seed amplification assay call.
    """


class UnitEnum(str, Enum):
    """
    Units as case-sensitive UCUM codes. Curly-brace codes are UCUM annotations for arbitrary, platform-specific units.
    """
    picogram_per_milliliter = "pg/mL"
    """
    Picograms per millilitre.
    """
    nanogram_per_milliliter = "ng/mL"
    """
    Nanograms per millilitre.
    """
    dimensionless_unit = "1"
    """
    Dimensionless (UCUM unity), used for ratios.
    """
    Relative_Fluorescence_Intensity_Unit = "{RFU}"
    """
    SomaScan relative fluorescence units.
    """
    LEFT_CURLY_BRACKETNPXRIGHT_CURLY_BRACKET = "{NPX}"
    """
    Olink normalised protein expression, an arbitrary log2 unit.
    """


class CategoricalResultEnum(str, Enum):
    """
    Result of a qualitative assay.
    """
    Positive_Finding = "POSITIVE"
    """
    The target was detected.
    """
    Negative_Finding = "NEGATIVE"
    """
    The target was not detected.
    """
    Indeterminate = "INDETERMINATE"
    """
    The result could not be called positive or negative.
    """


class AssayTechnologyEnum(str, Enum):
    """
    Assay technology.
    """
    enzyme_linked_immunosorbent_assay = "ELISA"
    """
    Enzyme-linked immunosorbent assay.
    """
    Single_Molecule_Array = "SIMOA"
    """
    Single-molecule array digital immunoassay.
    """
    SOMAscan_assay = "SOMASCAN"
    """
    SomaScan aptamer-based proteomic assay.
    """
    Olink_assay = "OLINK"
    """
    Olink proximity extension assay.
    """
    SEED_AMPLIFICATION_ASSAY = "SEED_AMPLIFICATION_ASSAY"
    """
    Alpha-synuclein seed amplification assay (e.g. RT-QuIC). No ontology has a specific term, so only a broad mapping is given.
    """
    Single_Photon_Emission_Computed_Tomography = "SPECT"
    """
    Single-photon emission computed tomography.
    """


class PlatformEnum(str, Enum):
    """
    Commercial platform and panel version.
    """
    SomaScan_5K = "SOMASCAN_5K"
    """
    SomaScan 5K panel (assay v4.0).
    """
    SomaScan_7K = "SOMASCAN_7K"
    """
    SomaScan 7K panel (assay v4.1).
    """
    Olink_Explore_3072SOLIDUS384 = "OLINK_EXPLORE_3072"
    """
    Olink Explore 3072 panel.
    """
    Olink_Explore_HT = "OLINK_EXPLORE_HT"
    """
    Olink Explore HT panel.
    """
    SIMOA_HD_X = "SIMOA_HD_X"
    """
    Quanterix Simoa HD-X analyser. No ontology term exists.
    """
    DAT_SPECT_IOFLUPANE = "DAT_SPECT_IOFLUPANE"
    """
    Dopamine transporter SPECT with the tracer ioflupane (123I).
    """


class CuratorTypeEnum(str, Enum):
    """
    Kind of agent that curated a record.
    """
    Person = "PERSON"
    """
    A human curator.
    """
    SoftwareAgent = "AI_AGENT"
    """
    An AI agent, such as an LLM-based curation tool.
    """


class ParkinsonianDisorderEnum(str):
    """
    Parkinson disease and the atypical parkinsonian disorders it is most often distinguished from. MONDO files multiple system atrophy and Lewy body dementia under synucleinopathy, and progressive supranuclear palsy under movement disorder, rather than under parkinsonian disorder, so each is listed as its own root.
    """

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any:
        from pydantic_core import core_schema

        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())


class ParkinsonsInstrumentEnum(str, Enum):
    """
    Rating scale totals recorded in Parkinson's studies. LOINC covers the MoCA total but not MDS-UPDRS: its UPDRS codes describe the original 1987 scale, which has different items and ranges.
    """
    MDS_UPDRS_PART_I = "MDS_UPDRS_PART_I"
    """
    MDS-UPDRS Part I (non-motor experiences of daily living) total, 0-52.
    """
    MDS_UPDRS_PART_II = "MDS_UPDRS_PART_II"
    """
    MDS-UPDRS Part II (motor experiences of daily living) total, 0-52.
    """
    MDS_UPDRS_PART_III = "MDS_UPDRS_PART_III"
    """
    MDS-UPDRS Part III (motor examination) total, 0-132.
    """
    MDS_UPDRS_PART_IV = "MDS_UPDRS_PART_IV"
    """
    MDS-UPDRS Part IV (motor complications) total, 0-24.
    """
    MDS_UPDRS___Hoehn_and_Yahr_Stage = "HOEHN_YAHR"
    """
    Hoehn and Yahr stage as rated in MDS-UPDRS, 0-5.
    """
    Total_score_LEFT_SQUARE_BRACKETMoCARIGHT_SQUARE_BRACKET = "MOCA"
    """
    Montreal Cognitive Assessment total score, 0-30.
    """


class DiagnosticCriteriaEnum(str, Enum):
    """
    Published clinical diagnostic criteria for parkinsonian disorders.
    """
    MDS_PD_2015 = "MDS_PD_2015"
    """
    MDS clinical diagnostic criteria for Parkinson's disease (Postuma et al., 2015).
    """
    UK_PDS_BRAIN_BANK = "UK_PDS_BRAIN_BANK"
    """
    UK Parkinson's Disease Society Brain Bank criteria (Hughes et al., 1992).
    """
    MDS_MSA_2022 = "MDS_MSA_2022"
    """
    MDS criteria for multiple system atrophy (Wenning et al., 2022).
    """
    MDS_PSP_2017 = "MDS_PSP_2017"
    """
    MDS criteria for progressive supranuclear palsy (Höglinger et al., 2017).
    """
    DLB_CONSORTIUM_2017 = "DLB_CONSORTIUM_2017"
    """
    Fourth consensus report of the DLB Consortium (McKeith et al., 2017).
    """


class DiagnosticCertaintyEnum(str, Enum):
    """
    Level of diagnostic certainty defined by the criteria.
    """
    CLINICALLY_ESTABLISHED = "CLINICALLY_ESTABLISHED"
    """
    Clinically established (MDS PD and MSA criteria).
    """
    PROBABLE = "PROBABLE"
    """
    Probable.
    """
    POSSIBLE = "POSSIBLE"
    """
    Possible (PSP and DLB criteria).
    """


class MedicationStateEnum(str, Enum):
    """
    Dopaminergic medication state during a motor examination.
    """
    ON = "ON"
    """
    Examined while responding to dopaminergic medication.
    """
    OFF = "OFF"
    """
    Examined after withholding dopaminergic medication.
    """
    UNTREATED = "UNTREATED"
    """
    Not yet taking dopaminergic medication.
    """



class NamedThing(ConfiguredBaseModel):
    """
    Any record with a globally unique identifier.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'class_uri': 'schema:Thing',
         'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class StudyDataset(NamedThing):
    """
    A versioned collection of cohort records with dataset-level metadata. Records refer to each other by identifier.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Dataset',
         'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    title: str = Field(default=..., description="""Human-readable title of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:description'} })
    dataset_version: str = Field(default=..., description="""Version of the dataset, in semantic versioning form.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'schema:version'} })
    license: str = Field(default=..., description="""Licence under which the dataset is released, as a URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:license'} })
    created_on: date = Field(default=..., description="""Date the dataset was created.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:created'} })
    conforms_to: str = Field(default=..., description="""Identifier of the schema version the dataset conforms to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:conformsTo'} })
    is_synthetic: bool = Field(default=..., description="""True when every record in the dataset is synthetic.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    participants: Optional[list[Participant]] = Field(default=None, description="""Participants in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    visits: Optional[list[Visit]] = Field(default=None, description="""Visits in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    diagnoses: Optional[list[Diagnosis]] = Field(default=None, description="""Diagnoses in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    phenotype_observations: Optional[list[PhenotypeObservation]] = Field(default=None, description="""Phenotype observations in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    clinical_assessments: Optional[list[ClinicalAssessment]] = Field(default=None, description="""Clinical assessments in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    specimens: Optional[list[Specimen]] = Field(default=None, description="""Specimens in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    analytes: Optional[list[Analyte]] = Field(default=None, description="""Analytes measured in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    assays: Optional[list[Assay]] = Field(default=None, description="""Assays used in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    biomarker_measurements: Optional[list[BiomarkerMeasurement]] = Field(default=None, description="""Biomarker measurements in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('dataset_version')
    def pattern_dataset_version(cls, v):
        pattern=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid dataset_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid dataset_version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Participant(NamedThing):
    """
    A person enrolled in the study.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:Person',
         'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    cohort: CohortEnum = Field(default=..., description="""Study arm the participant was enrolled in.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Participant']} })
    sex: Optional[SexEnum] = Field(default=None, description="""Biological sex of the participant.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Participant']} })
    year_of_birth: Optional[int] = Field(default=None, description="""Year of birth (full dates of birth are not recorded).""", ge=1900, le=2026, json_schema_extra = { "linkml_meta": {'domain_of': ['Participant']} })
    enrolment_date: date = Field(default=..., description="""Date the participant was enrolled.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Participant']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Visit(NamedThing):
    """
    A scheduled study visit at which data and specimens are collected.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    participant: str = Field(default=..., description="""The participant this record belongs to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Visit', 'Diagnosis']} })
    visit_code: str = Field(default=..., description="""Protocol visit code as months from baseline, e.g. M00 for baseline and M12 for month 12.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Visit']} })
    visit_date: date = Field(default=..., description="""Date the visit took place.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Visit']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('visit_code')
    def pattern_visit_code(cls, v):
        pattern=re.compile(r"^M[0-9]{2,3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid visit_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid visit_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Diagnosis(NamedThing):
    """
    A clinical diagnosis recorded for a participant.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    participant: str = Field(default=..., description="""The participant this record belongs to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Visit', 'Diagnosis']} })
    condition: DiseaseEnum = Field(default=..., description="""Diagnosed condition, as a MONDO term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis']} })
    age_at_symptom_onset: Optional[float] = Field(default=None, description="""Age in years at onset of the first symptom attributed to the condition.""", ge=0, le=120, json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis'], 'unit': {'ucum_code': 'a'}} })
    age_at_diagnosis: Optional[float] = Field(default=None, description="""Age in years when the condition was diagnosed.""", ge=0, le=120, json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis'], 'unit': {'ucum_code': 'a'}} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class PhenotypeObservation(NamedThing):
    """
    A phenotypic feature assessed at a visit, recorded as present or explicitly excluded.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    visit: str = Field(default=..., description="""The visit at which this record was collected.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation',
                       'ClinicalAssessment',
                       'Specimen',
                       'BiomarkerMeasurement']} })
    phenotype: PhenotypeEnum = Field(default=..., description="""Phenotypic feature, as an HPO term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation']} })
    excluded: Optional[bool] = Field(default=False, description="""True when the feature was looked for and found absent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation'], 'ifabsent': 'false'} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ClinicalAssessment(NamedThing):
    """
    The total score of a clinical rating scale administered at a visit. Disease modules subclass this and bind the instrument to their own value set.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True, 'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    visit: str = Field(default=..., description="""The visit at which this record was collected.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation',
                       'ClinicalAssessment',
                       'Specimen',
                       'BiomarkerMeasurement']} })
    instrument: str = Field(default=..., description="""The rating scale and score that was recorded. Disease modules bind this to their own value set.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    score: float = Field(default=..., description="""Total score on the instrument.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Specimen(NamedThing):
    """
    A biological sample collected at a visit.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    visit: str = Field(default=..., description="""The visit at which this record was collected.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation',
                       'ClinicalAssessment',
                       'Specimen',
                       'BiomarkerMeasurement']} })
    specimen_type: SpecimenTypeEnum = Field(default=..., description="""Anatomical material of the specimen, as an UBERON term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Specimen']} })
    freeze_thaw_cycles: Optional[int] = Field(default=None, description="""Number of freeze-thaw cycles before analysis.""", ge=0, le=20, json_schema_extra = { "linkml_meta": {'domain_of': ['Specimen']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Analyte(NamedThing):
    """
    The molecular entity a measurement quantifies, identified by its UniProtKB accession so that values from different platforms can be linked to the same protein.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core',
         'slot_usage': {'id': {'name': 'id',
                               'pattern': '^UniProtKB:([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$'}}})

    label: str = Field(default=..., description="""Human-readable name of the record.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analyte', 'Assay'], 'slot_uri': 'rdfs:label'} })
    gene_symbol: Optional[str] = Field(default=None, description="""HGNC-approved symbol of the gene encoding the analyte.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analyte']} })
    hgnc_id: Optional[str] = Field(default=None, description="""HGNC identifier of the gene encoding the analyte.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analyte']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('gene_symbol')
    def pattern_gene_symbol(cls, v):
        pattern=re.compile(r"^[A-Z][A-Z0-9-]*$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid gene_symbol format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid gene_symbol format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('hgnc_id')
    def pattern_hgnc_id(cls, v):
        pattern=re.compile(r"^HGNC:[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid hgnc_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid hgnc_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^UniProtKB:([OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2})$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class Assay(NamedThing):
    """
    A measurement procedure, defined by its technology and platform.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core'})

    label: str = Field(default=..., description="""Human-readable name of the record.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Analyte', 'Assay'], 'slot_uri': 'rdfs:label'} })
    technology: AssayTechnologyEnum = Field(default=..., description="""Assay technology, as an OBI or NCIT term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assay']} })
    platform: Optional[PlatformEnum] = Field(default=None, description="""Commercial platform and panel version, where one applies.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Assay']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ProvenanceMixin(ConfiguredBaseModel):
    """
    Who curated a record, when, from which source, and whether the curator was a person or an AI agent.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'https://w3id.org/pd-biomarker-model/core',
         'mixin': True})

    source: str = Field(default=..., description="""Identifier or name of the source dataset, file or system the record was taken from.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:hadPrimarySource'} })
    curation_date: date = Field(default=..., description="""Date the record was curated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:generatedAtTime'} })
    curator: str = Field(default=..., description="""Who curated the record: an ORCID for a person, or a versioned agent identifier for an AI agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:wasAttributedTo'} })
    curator_type: CuratorTypeEnum = Field(default=..., description="""Whether the curator was a person or an AI agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin']} })


class BiomarkerMeasurement(ProvenanceMixin, NamedThing):
    """
    One biomarker value for one analyte at one visit, from a specimen (fluid or tissue) or from imaging.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model/core',
         'mixins': ['ProvenanceMixin'],
         'rules': [{'description': 'A ratio is dimensionless, so its unit must be the '
                                   'UCUM unity "1".',
                    'postconditions': {'slot_conditions': {'unit': {'equals_string': '1',
                                                                    'name': 'unit'}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string': 'RATIO',
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'A concentration must use a mass-concentration '
                                   'unit.',
                    'postconditions': {'slot_conditions': {'unit': {'equals_string_in': ['pg/mL',
                                                                                         'ng/mL'],
                                                                    'name': 'unit'}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string': 'CONCENTRATION',
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'A relative abundance must use a platform-relative '
                                   'unit (SomaScan RFU or Olink NPX), never a mass '
                                   'concentration.',
                    'postconditions': {'slot_conditions': {'unit': {'equals_string_in': ['{RFU}',
                                                                                         '{NPX}'],
                                                                    'name': 'unit'}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string': 'RELATIVE_ABUNDANCE',
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'A quantitative measurement needs a numeric value '
                                   'and a unit.',
                    'postconditions': {'slot_conditions': {'unit': {'name': 'unit',
                                                                    'required': True},
                                                           'value': {'name': 'value',
                                                                     'required': True}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string_in': ['CONCENTRATION',
                                                                                                    'RELATIVE_ABUNDANCE',
                                                                                                    'RATIO'],
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'A categorical measurement needs a categorical '
                                   'result and must not carry a numeric value.',
                    'postconditions': {'slot_conditions': {'categorical_result': {'name': 'categorical_result',
                                                                                  'required': True},
                                                           'value': {'name': 'value',
                                                                     'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string': 'CATEGORICAL',
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'A categorical measurement must not carry a unit.',
                    'postconditions': {'slot_conditions': {'unit': {'name': 'unit',
                                                                    'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'measurement_type': {'equals_string': 'CATEGORICAL',
                                                                               'name': 'measurement_type'}}}},
                   {'description': 'An imaging measurement needs a brain region and '
                                   'laterality and has no specimen.',
                    'postconditions': {'slot_conditions': {'brain_region': {'name': 'brain_region',
                                                                            'required': True},
                                                           'laterality': {'name': 'laterality',
                                                                          'required': True},
                                                           'specimen': {'name': 'specimen',
                                                                        'value_presence': 'ABSENT'}}},
                    'preconditions': {'slot_conditions': {'modality': {'equals_string': 'IMAGING',
                                                                       'name': 'modality'}}}},
                   {'description': 'A specimen-based measurement needs a specimen and '
                                   'has no brain region.',
                    'postconditions': {'slot_conditions': {'brain_region': {'name': 'brain_region',
                                                                            'value_presence': 'ABSENT'},
                                                           'specimen': {'name': 'specimen',
                                                                        'required': True}}},
                    'preconditions': {'slot_conditions': {'modality': {'equals_string': 'SPECIMEN',
                                                                       'name': 'modality'}}}},
                   {'description': 'A human curator is identified by an ORCID.',
                    'postconditions': {'slot_conditions': {'curator': {'name': 'curator',
                                                                       'pattern': '^ORCID:[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$'}}},
                    'preconditions': {'slot_conditions': {'curator_type': {'equals_string': 'PERSON',
                                                                           'name': 'curator_type'}}}}]})

    visit: str = Field(default=..., description="""The visit at which this record was collected.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation',
                       'ClinicalAssessment',
                       'Specimen',
                       'BiomarkerMeasurement']} })
    specimen: Optional[str] = Field(default=None, description="""The specimen that was assayed. Absent for imaging measurements.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    assay: str = Field(default=..., description="""The assay that produced the value.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    analyte: str = Field(default=..., description="""The analyte that was measured.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    platform_probe_id: Optional[str] = Field(default=None, description="""Platform-specific reagent identifier: a SomaScan SeqId (e.g. seq.12345.6) or an Olink assay ID (e.g. OID12345).""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    loinc_code: Optional[str] = Field(default=None, description="""LOINC code of the laboratory test, where one exists.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    modality: ModalityEnum = Field(default=..., description="""Whether the value comes from a specimen or from imaging.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    measurement_type: MeasurementTypeEnum = Field(default=..., description="""Kind of quantity the value represents.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    value: Optional[float] = Field(default=None, description="""Numeric value of a quantitative measurement.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    unit: Optional[UnitEnum] = Field(default=None, description="""Unit of the value, as a UCUM code.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    categorical_result: Optional[CategoricalResultEnum] = Field(default=None, description="""Result of a qualitative assay.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    below_lloq: Optional[bool] = Field(default=None, description="""True when the value is below the assay's lower limit of quantification.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    brain_region: Optional[BrainRegionEnum] = Field(default=None, description="""Brain region of an imaging measurement, as an UBERON term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    laterality: Optional[LateralityEnum] = Field(default=None, description="""Side of the body the imaging value refers to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['BiomarkerMeasurement']} })
    source: str = Field(default=..., description="""Identifier or name of the source dataset, file or system the record was taken from.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:hadPrimarySource'} })
    curation_date: date = Field(default=..., description="""Date the record was curated.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:generatedAtTime'} })
    curator: str = Field(default=..., description="""Who curated the record: an ORCID for a person, or a versioned agent identifier for an AI agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin'], 'slot_uri': 'prov:wasAttributedTo'} })
    curator_type: CuratorTypeEnum = Field(default=..., description="""Whether the curator was a person or an AI agent.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ProvenanceMixin']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('platform_probe_id')
    def pattern_platform_probe_id(cls, v):
        pattern=re.compile(r"^(seq\.[0-9]{4,5}\.[0-9]{1,3}|OID[0-9]{5})$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid platform_probe_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid platform_probe_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('loinc_code')
    def pattern_loinc_code(cls, v):
        pattern=re.compile(r"^LOINC:[0-9]{1,7}-[0-9]$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid loinc_code format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid loinc_code format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ParkinsonsStudyDataset(StudyDataset):
    """
    A study dataset whose diagnoses and assessments follow the Parkinson's module.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model',
         'slot_usage': {'clinical_assessments': {'name': 'clinical_assessments',
                                                 'range': 'ParkinsonsClinicalAssessment'},
                        'diagnoses': {'name': 'diagnoses',
                                      'range': 'ParkinsonsDiagnosis'}},
         'tree_root': True})

    title: str = Field(default=..., description="""Human-readable title of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:title'} })
    description: Optional[str] = Field(default=None, description="""Free-text description of the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:description'} })
    dataset_version: str = Field(default=..., description="""Version of the dataset, in semantic versioning form.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'schema:version'} })
    license: str = Field(default=..., description="""Licence under which the dataset is released, as a URI.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:license'} })
    created_on: date = Field(default=..., description="""Date the dataset was created.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:created'} })
    conforms_to: str = Field(default=..., description="""Identifier of the schema version the dataset conforms to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset'], 'slot_uri': 'dcterms:conformsTo'} })
    is_synthetic: bool = Field(default=..., description="""True when every record in the dataset is synthetic.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    participants: Optional[list[Participant]] = Field(default=None, description="""Participants in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    visits: Optional[list[Visit]] = Field(default=None, description="""Visits in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    diagnoses: Optional[list[ParkinsonsDiagnosis]] = Field(default=None, description="""Diagnoses in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    phenotype_observations: Optional[list[PhenotypeObservation]] = Field(default=None, description="""Phenotype observations in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    clinical_assessments: Optional[list[ParkinsonsClinicalAssessment]] = Field(default=None, description="""Clinical assessments in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    specimens: Optional[list[Specimen]] = Field(default=None, description="""Specimens in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    analytes: Optional[list[Analyte]] = Field(default=None, description="""Analytes measured in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    assays: Optional[list[Assay]] = Field(default=None, description="""Assays used in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    biomarker_measurements: Optional[list[BiomarkerMeasurement]] = Field(default=None, description="""Biomarker measurements in the dataset.""", json_schema_extra = { "linkml_meta": {'domain_of': ['StudyDataset']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('dataset_version')
    def pattern_dataset_version(cls, v):
        pattern=re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid dataset_version format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid dataset_version format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ParkinsonsDiagnosis(Diagnosis):
    """
    Diagnosis of a parkinsonian disorder, with the clinical criteria used and their level of certainty.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model',
         'slot_usage': {'condition': {'name': 'condition',
                                      'range': 'ParkinsonianDisorderEnum'}}})

    diagnostic_criteria: DiagnosticCriteriaEnum = Field(default=..., description="""Published clinical diagnostic criteria applied.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ParkinsonsDiagnosis']} })
    diagnostic_certainty: Optional[DiagnosticCertaintyEnum] = Field(default=None, description="""Level of certainty reached under the diagnostic criteria.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ParkinsonsDiagnosis']} })
    participant: str = Field(default=..., description="""The participant this record belongs to.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Visit', 'Diagnosis']} })
    condition: ParkinsonianDisorderEnum = Field(default=..., description="""Diagnosed condition, as a MONDO term.""", json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis']} })
    age_at_symptom_onset: Optional[float] = Field(default=None, description="""Age in years at onset of the first symptom attributed to the condition.""", ge=0, le=120, json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis'], 'unit': {'ucum_code': 'a'}} })
    age_at_diagnosis: Optional[float] = Field(default=None, description="""Age in years when the condition was diagnosed.""", ge=0, le=120, json_schema_extra = { "linkml_meta": {'domain_of': ['Diagnosis'], 'unit': {'ucum_code': 'a'}} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


class ParkinsonsClinicalAssessment(ClinicalAssessment):
    """
    Total score on a Parkinson's rating scale, with the dopaminergic medication state at the time of a motor examination.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://w3id.org/pd-biomarker-model',
         'rules': [{'description': 'MDS-UPDRS Part I total ranges from 0 to 52.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 52,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'MDS_UPDRS_PART_I',
                                                                         'name': 'instrument'}}}},
                   {'description': 'MDS-UPDRS Part II total ranges from 0 to 52.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 52,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'MDS_UPDRS_PART_II',
                                                                         'name': 'instrument'}}}},
                   {'description': 'MDS-UPDRS Part III total ranges from 0 to 132.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 132,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'MDS_UPDRS_PART_III',
                                                                         'name': 'instrument'}}}},
                   {'description': 'MDS-UPDRS Part IV total ranges from 0 to 24.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 24,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'MDS_UPDRS_PART_IV',
                                                                         'name': 'instrument'}}}},
                   {'description': 'Hoehn and Yahr stage ranges from 0 to 5.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 5,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'HOEHN_YAHR',
                                                                         'name': 'instrument'}}}},
                   {'description': 'MoCA total ranges from 0 to 30.',
                    'postconditions': {'slot_conditions': {'score': {'maximum_value': 30,
                                                                     'minimum_value': 0,
                                                                     'name': 'score'}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string': 'MOCA',
                                                                         'name': 'instrument'}}}},
                   {'description': 'Motor examination scores depend on medication, so '
                                   'MDS-UPDRS Part III and Hoehn and Yahr need the '
                                   'medication state.',
                    'postconditions': {'slot_conditions': {'medication_state': {'name': 'medication_state',
                                                                                'required': True}}},
                    'preconditions': {'slot_conditions': {'instrument': {'equals_string_in': ['MDS_UPDRS_PART_III',
                                                                                              'HOEHN_YAHR'],
                                                                         'name': 'instrument'}}}}],
         'slot_usage': {'instrument': {'name': 'instrument',
                                       'range': 'ParkinsonsInstrumentEnum'}}})

    medication_state: Optional[MedicationStateEnum] = Field(default=None, description="""Dopaminergic medication state during a motor examination.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ParkinsonsClinicalAssessment']} })
    visit: str = Field(default=..., description="""The visit at which this record was collected.""", json_schema_extra = { "linkml_meta": {'domain_of': ['PhenotypeObservation',
                       'ClinicalAssessment',
                       'Specimen',
                       'BiomarkerMeasurement']} })
    instrument: ParkinsonsInstrumentEnum = Field(default=..., description="""The rating scale and score that was recorded. Disease modules bind this to their own value set.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    score: float = Field(default=..., description="""Total score on the instrument.""", json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    id: str = Field(default=..., description="""Globally unique identifier of the record, written as a CURIE.""", json_schema_extra = { "linkml_meta": {'domain_of': ['NamedThing'], 'slot_uri': 'schema:identifier'} })

    @field_validator('id')
    def pattern_id(cls, v):
        pattern=re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*:[A-Za-z0-9_./-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.search(element):
                    err_msg = f"Invalid id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.search(v):
            err_msg = f"Invalid id format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
NamedThing.model_rebuild()
StudyDataset.model_rebuild()
Participant.model_rebuild()
Visit.model_rebuild()
Diagnosis.model_rebuild()
PhenotypeObservation.model_rebuild()
ClinicalAssessment.model_rebuild()
Specimen.model_rebuild()
Analyte.model_rebuild()
Assay.model_rebuild()
ProvenanceMixin.model_rebuild()
BiomarkerMeasurement.model_rebuild()
ParkinsonsStudyDataset.model_rebuild()
ParkinsonsDiagnosis.model_rebuild()
ParkinsonsClinicalAssessment.model_rebuild()
