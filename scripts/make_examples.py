"""Generate the synthetic example datasets in examples/.

    uv run python scripts/make_examples.py

- examples/valid/ParkinsonsStudyDataset-001.yaml: a small synthetic cohort
  (Parkinson's disease, multiple system atrophy, prodromal and healthy
  control participants) with clinical, fluid and imaging data.
- examples/valid/ParkinsonsStudyDataset-002.yaml: a minimal dataset.
- examples/invalid/*.yaml: copies of the minimal dataset that each break one
  rule. The header of each file names the rule and the error it must raise.

All values are invented. Identifiers of reference terms (MONDO, HPO, UBERON,
UniProtKB, HGNC, LOINC) are real; platform probe identifiers are invented
but follow the SomaScan and Olink formats.
"""

from __future__ import annotations

import copy
import random
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID = ROOT / "examples" / "valid"
INVALID = ROOT / "examples" / "invalid"

TODAY = "2026-11-18"
CURATOR = "ORCID:0000-0002-1825-0097"  # ORCID's documented example iD
AGENT = "pdbm:agent/harmonisation-agent-v1"

ANALYTES = [
    {"id": "UniProtKB:P37840", "label": "alpha-synuclein", "gene_symbol": "SNCA", "hgnc_id": "HGNC:11138"},
    {"id": "UniProtKB:P07196", "label": "neurofilament light polypeptide", "gene_symbol": "NEFL", "hgnc_id": "HGNC:7739"},
    {"id": "UniProtKB:Q14956", "label": "transmembrane glycoprotein NMB", "gene_symbol": "GPNMB", "hgnc_id": "HGNC:4462"},
    {"id": "UniProtKB:Q01959", "label": "sodium-dependent dopamine transporter", "gene_symbol": "SLC6A3", "hgnc_id": "HGNC:11049"},
]
ASSAYS = [
    {"id": "pdbm:AS0001", "label": "CSF alpha-synuclein seed amplification assay", "technology": "SEED_AMPLIFICATION_ASSAY"},
    {"id": "pdbm:AS0002", "label": "Serum neurofilament light chain, single-molecule array", "technology": "SIMOA", "platform": "SIMOA_HD_X"},
    {"id": "pdbm:AS0003", "label": "Plasma proteomics, SomaScan 7K", "technology": "SOMASCAN", "platform": "SOMASCAN_7K"},
    {"id": "pdbm:AS0004", "label": "Plasma proteomics, Olink Explore 3072", "technology": "OLINK", "platform": "OLINK_EXPLORE_3072"},
    {"id": "pdbm:AS0005", "label": "Dopamine transporter SPECT", "technology": "SPECT", "platform": "DAT_SPECT_IOFLUPANE"},
]

# (sex, year of birth, enrolment date, group)
PARTICIPANTS = [
    ("FEMALE", 1952, "2023-02-06", "PD"),
    ("MALE", 1958, "2023-03-13", "PD"),
    ("MALE", 1947, "2023-04-17", "PD"),
    ("FEMALE", 1961, "2023-05-22", "PD_UNTREATED"),
    ("MALE", 1955, "2023-06-26", "MSA"),
    ("FEMALE", 1954, "2023-02-20", "HC"),
    ("MALE", 1950, "2023-04-03", "HC"),
    ("MALE", 1957, "2023-05-08", "PRODROMAL"),
]
COHORT = {"PD": "CASE", "PD_UNTREATED": "CASE", "MSA": "CASE", "HC": "HEALTHY_CONTROL", "PRODROMAL": "PRODROMAL"}

PHENOTYPES = {  # (HPO term, excluded)
    "PD": [("HP:0002067", False), ("HP:0002322", False), ("HP:0002063", False), ("HP:0004409", False), ("HP:0002019", False)],
    "PD_UNTREATED": [("HP:0002067", False), ("HP:0002322", False), ("HP:0004409", False)],
    "MSA": [("HP:0002067", False), ("HP:0002063", False), ("HP:0001278", False), ("HP:5200291", False), ("HP:0002322", True)],
    "HC": [("HP:0004409", True), ("HP:5200291", True)],
    "PRODROMAL": [("HP:5200291", False), ("HP:0004409", False), ("HP:0002067", True)],
}

# Score centres per group: Part I, II, III, IV, Hoehn and Yahr, MoCA, NfL pg/mL, DaT SBR, SAA
PROFILE = {
    "PD": dict(p1=9, p2=11, p3=30, p4=3, hy=2, moca=26, nfl=15.0, sbr=1.1, saa="POSITIVE"),
    "PD_UNTREATED": dict(p1=5, p2=6, p3=19, p4=0, hy=1, moca=28, nfl=11.0, sbr=1.4, saa="POSITIVE"),
    "MSA": dict(p1=14, p2=20, p3=44, p4=2, hy=3, moca=25, nfl=46.0, sbr=0.9, saa="POSITIVE"),
    "HC": dict(p1=2, p2=0, p3=2, p4=0, hy=0, moca=28, nfl=9.0, sbr=2.5, saa="NEGATIVE"),
    "PRODROMAL": dict(p1=6, p2=1, p3=5, p4=0, hy=0, moca=27, nfl=11.5, sbr=1.8, saa="POSITIVE"),
}


def header(title: str, version: str = "1.0.0") -> dict:
    return {
        "id": "pdbm:DS0001",
        "title": title,
        "description": "Synthetic records generated for testing and documentation. No real participants.",
        "dataset_version": version,
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "created_on": TODAY,
        "conforms_to": "https://w3id.org/pd-biomarker-model/0.1.0",
        "is_synthetic": True,
    }


def provenance(source: str, ai: bool = False) -> dict:
    return {
        "source": source,
        "curation_date": TODAY,
        "curator": AGENT if ai else CURATOR,
        "curator_type": "AI_AGENT" if ai else "PERSON",
    }


def cohort_dataset() -> dict:
    rng = random.Random(2026)
    d = header("Synthetic Parkinson's disease biomarker cohort")
    d.update(participants=[], visits=[], diagnoses=[], phenotype_observations=[],
             clinical_assessments=[], specimens=[], analytes=copy.deepcopy(ANALYTES),
             assays=copy.deepcopy(ASSAYS), biomarker_measurements=[])
    n = {k: 0 for k in "VDOASM"}

    def new_id(kind: str) -> str:
        n[kind] += 1
        return f"pdbm:{kind}{n[kind]:04d}"

    for i, (sex, yob, enrolled, group) in enumerate(PARTICIPANTS, start=1):
        pid = f"pdbm:P{i:04d}"
        prof = PROFILE[group]
        d["participants"].append({"id": pid, "cohort": COHORT[group], "sex": sex,
                                  "year_of_birth": yob, "enrolment_date": enrolled})
        enrol_date = date.fromisoformat(enrolled)
        age_at_enrolment = enrol_date.year - yob

        if group in ("PD", "PD_UNTREATED", "MSA"):
            onset = age_at_enrolment - rng.randint(2, 6) - 0.5
            diagnosis = {"id": new_id("D"), "participant": pid,
                         "condition": "MONDO:0020352" if group == "MSA" else "MONDO:0005180",
                         "diagnostic_criteria": "MDS_MSA_2022" if group == "MSA" else "MDS_PD_2015",
                         "diagnostic_certainty": "PROBABLE" if group in ("MSA", "PD_UNTREATED") else "CLINICALLY_ESTABLISHED",
                         "age_at_symptom_onset": onset,
                         "age_at_diagnosis": onset + rng.randint(1, 2)}
            d["diagnoses"].append(diagnosis)

        for month in (0, 12):
            vid = new_id("V")
            visit_date = enrol_date + timedelta(days=round(month * 30.44) + (rng.randint(-10, 10) if month else 0))
            d["visits"].append({"id": vid, "participant": pid, "visit_code": f"M{month:02d}",
                                "visit_date": visit_date.isoformat()})
            drift = month / 12

            if month == 0:
                for term, excluded in PHENOTYPES[group]:
                    obs = {"id": new_id("O"), "visit": vid, "phenotype": term}
                    if excluded:
                        obs["excluded"] = True
                    d["phenotype_observations"].append(obs)

            treated = group in ("PD", "MSA")
            med_state = "OFF" if treated else "UNTREATED"
            instruments = [("MDS_UPDRS_PART_III", prof["p3"] + 3 * drift, 132), ("MOCA", prof["moca"] - drift, 30)]
            if group in ("PD", "PD_UNTREATED", "MSA"):
                instruments += [("MDS_UPDRS_PART_I", prof["p1"] + drift, 52),
                                ("MDS_UPDRS_PART_II", prof["p2"] + 2 * drift, 52),
                                ("HOEHN_YAHR", prof["hy"], 5)]
                if treated and month == 12:
                    instruments.append(("MDS_UPDRS_PART_IV", prof["p4"], 24))
            for instrument, centre, maximum in instruments:
                score = centre if instrument == "HOEHN_YAHR" else centre + rng.randint(-3, 3)
                record = {"id": new_id("A"), "visit": vid, "instrument": instrument,
                          "score": float(min(max(round(score), 0), maximum))}
                if instrument in ("MDS_UPDRS_PART_III", "HOEHN_YAHR"):
                    record["medication_state"] = med_state
                d["clinical_assessments"].append(record)

            # Specimens: CSF at baseline only; plasma and serum at every visit.
            specimen_ids = {}
            for stype in (["CSF"] if month == 0 else []) + ["PLASMA", "SERUM"]:
                sid = new_id("S")
                specimen_ids[stype] = sid
                d["specimens"].append({"id": sid, "visit": vid, "specimen_type": stype,
                                       "freeze_thaw_cycles": rng.randint(0, 1)})

            m = d["biomarker_measurements"]
            if month == 0:
                m.append({"id": new_id("M"), "visit": vid, "specimen": specimen_ids["CSF"],
                          "assay": "pdbm:AS0001", "analyte": "UniProtKB:P37840", "modality": "SPECIMEN",
                          "measurement_type": "CATEGORICAL", "categorical_result": prof["saa"],
                          **provenance("synthetic-lab-export-2026-11")})
                for side in ("LEFT", "RIGHT"):
                    m.append({"id": new_id("M"), "visit": vid, "assay": "pdbm:AS0005",
                              "analyte": "UniProtKB:Q01959", "modality": "IMAGING", "measurement_type": "RATIO",
                              "value": round(prof["sbr"] + rng.uniform(-0.2, 0.2), 2), "unit": "1",
                              "brain_region": "UBERON:0001874", "laterality": side,
                              **provenance("synthetic-imaging-core-2026-11")})
            m.append({"id": new_id("M"), "visit": vid, "specimen": specimen_ids["SERUM"],
                      "assay": "pdbm:AS0002", "analyte": "UniProtKB:P07196", "loinc_code": "LOINC:101281-4",
                      "modality": "SPECIMEN", "measurement_type": "CONCENTRATION",
                      "value": round(prof["nfl"] * (1 + 0.05 * drift) + rng.uniform(-1.5, 1.5), 1), "unit": "pg/mL",
                      **provenance("synthetic-lab-export-2026-11")})
            m.append({"id": new_id("M"), "visit": vid, "specimen": specimen_ids["PLASMA"],
                      "assay": "pdbm:AS0003", "analyte": "UniProtKB:Q14956", "platform_probe_id": "seq.99001.11",
                      "modality": "SPECIMEN", "measurement_type": "RELATIVE_ABUNDANCE",
                      "value": round(rng.uniform(1800, 2900), 1), "unit": "{RFU}",
                      **provenance("synthetic-somascan-batch-01", ai=True)})
            m.append({"id": new_id("M"), "visit": vid, "specimen": specimen_ids["PLASMA"],
                      "assay": "pdbm:AS0004", "analyte": "UniProtKB:Q14956", "platform_probe_id": "OID99001",
                      "modality": "SPECIMEN", "measurement_type": "RELATIVE_ABUNDANCE",
                      "value": round(rng.uniform(-0.8, 1.6), 3), "unit": "{NPX}",
                      **provenance("synthetic-olink-batch-01", ai=True)})
    return d


def minimal_dataset() -> dict:
    d = header("Minimal synthetic dataset")
    d.update(
        participants=[{"id": "pdbm:P0001", "cohort": "CASE", "sex": "FEMALE", "year_of_birth": 1956,
                       "enrolment_date": "2024-03-04"}],
        visits=[{"id": "pdbm:V0001", "participant": "pdbm:P0001", "visit_code": "M00", "visit_date": "2024-03-04"}],
        diagnoses=[{"id": "pdbm:D0001", "participant": "pdbm:P0001", "condition": "MONDO:0005180",
                    "diagnostic_criteria": "MDS_PD_2015", "diagnostic_certainty": "CLINICALLY_ESTABLISHED",
                    "age_at_symptom_onset": 64.5, "age_at_diagnosis": 66.0}],
        phenotype_observations=[{"id": "pdbm:O0001", "visit": "pdbm:V0001", "phenotype": "HP:0002067"}],
        clinical_assessments=[{"id": "pdbm:A0001", "visit": "pdbm:V0001", "instrument": "MDS_UPDRS_PART_III",
                               "score": 24.0, "medication_state": "OFF"}],
        specimens=[{"id": "pdbm:S0001", "visit": "pdbm:V0001", "specimen_type": "CSF", "freeze_thaw_cycles": 1}],
        analytes=[copy.deepcopy(ANALYTES[0])],
        assays=[copy.deepcopy(ASSAYS[0])],
        biomarker_measurements=[{"id": "pdbm:M0001", "visit": "pdbm:V0001", "specimen": "pdbm:S0001",
                                 "assay": "pdbm:AS0001", "analyte": "UniProtKB:P37840", "modality": "SPECIMEN",
                                 "measurement_type": "CATEGORICAL", "categorical_result": "POSITIVE",
                                 **provenance("synthetic-lab-export-2026-11")}],
    )
    return d


# --- one-rule mutations of the minimal dataset ---------------------------------

def _m(d):  # the measurement
    return d["biomarker_measurements"][0]


def _quantitative(d, mtype="CONCENTRATION", value=12.0, unit="pg/mL"):
    m = _m(d)
    m.pop("categorical_result", None)
    m.update(measurement_type=mtype, value=value, unit=unit)


def _imaging(d, brain_region="UBERON:0001874"):
    """Turn the measurement into a valid DaT-SPECT putamen binding ratio."""
    d["analytes"].append(copy.deepcopy(ANALYTES[3]))
    d["assays"].append(copy.deepcopy(ASSAYS[4]))
    m = _m(d)
    m.pop("categorical_result", None)
    m.pop("specimen", None)
    m.update(assay="pdbm:AS0005", analyte="UniProtKB:Q01959", modality="IMAGING", measurement_type="RATIO",
             value=1.1, unit="1", brain_region=brain_region, laterality="LEFT")


def _second_visit(d):
    d["visits"].append({"id": "pdbm:V0002", "participant": "pdbm:P0001", "visit_code": "M12",
                        "visit_date": "2025-03-03"})


MUTATIONS = {
    # name: (rule broken, expected error fragment, mutation)
    "ratio-unit-not-dimensionless": (
        "A ratio must have unit 1.", "'1' was expected",
        lambda d: _quantitative(d, "RATIO", 2.1, "pg/mL")),
    "concentration-in-rfu": (
        "A concentration must use pg/mL or ng/mL.", "is not one of ['pg/mL', 'ng/mL']",
        lambda d: _quantitative(d, "CONCENTRATION", 2400.0, "{RFU}")),
    "relative-abundance-in-pg-per-ml": (
        "A relative abundance must use RFU or NPX.", "is not one of ['{RFU}', '{NPX}']",
        lambda d: _quantitative(d, "RELATIVE_ABUNDANCE", 12.0, "pg/mL")),
    "quantitative-without-value": (
        "A quantitative measurement needs a value.", "'value' is a required property",
        lambda d: (_quantitative(d), _m(d).pop("value"))),
    "categorical-with-value": (
        "A categorical measurement has no value.", "should not be valid under {'required': ['value']}",
        lambda d: _m(d).update(value=1.0)),
    "categorical-with-unit": (
        "A categorical measurement has no unit.", "should not be valid under {'required': ['unit']}",
        lambda d: _m(d).update(unit="pg/mL")),
    "imaging-with-specimen": (
        "An imaging measurement has no specimen.", "should not be valid under {'required': ['specimen']}",
        lambda d: (_imaging(d), _m(d).update(specimen="pdbm:S0001"))),
    "imaging-without-brain-region": (
        "An imaging measurement needs a brain region.", "'brain_region' is a required property",
        lambda d: (_imaging(d), _m(d).pop("brain_region"))),
    "specimen-measurement-without-specimen": (
        "A specimen measurement needs a specimen.", "'specimen' is a required property",
        lambda d: _m(d).pop("specimen")),
    "person-curator-without-orcid": (
        "A person curator is identified by an ORCID.", "does not match '^ORCID:",
        lambda d: _m(d).update(curator="pdbm:curator/jane-doe")),
    "moca-above-30": (
        "MoCA total is 0-30.", "31.0 is greater than the maximum of 30",
        lambda d: d["clinical_assessments"][0].update(instrument="MOCA", score=31.0)),
    "hoehn-yahr-above-5": (
        "Hoehn and Yahr stage is 0-5.", "6.0 is greater than the maximum of 5",
        lambda d: d["clinical_assessments"][0].update(instrument="HOEHN_YAHR", score=6.0)),
    "updrs-iii-without-medication-state": (
        "MDS-UPDRS Part III needs the medication state.", "'medication_state' is a required property",
        lambda d: d["clinical_assessments"][0].pop("medication_state")),
    "visit-code-pattern": (
        "Visit codes are M followed by months.", "'BL' does not match",
        lambda d: d["visits"][0].update(visit_code="BL")),
    "probe-id-pattern": (
        "Probe IDs follow the SomaScan or Olink format.", "'seq-1234' does not match",
        lambda d: _m(d).update(platform_probe_id="seq-1234")),
    "analyte-not-uniprot": (
        "Analytes are identified by UniProtKB accession.", "'HGNC:11138' does not match",
        lambda d: (d["analytes"][0].update(id="HGNC:11138"), _m(d).update(analyte="HGNC:11138"))),
    "diagnosis-without-criteria": (
        "Diagnostic criteria are required.", "'diagnostic_criteria' is a required property",
        lambda d: d["diagnoses"][0].pop("diagnostic_criteria")),
    "year-of-birth-out-of-range": (
        "Year of birth is 1900-2026.", "1850 is less than the minimum of 1900",
        lambda d: d["participants"][0].update(year_of_birth=1850)),
    "undeclared-slot": (
        "Only schema slots are allowed.", "Additional properties are not allowed ('date_of_birth'",
        lambda d: d["participants"][0].update(date_of_birth="1956-07-14")),
    "specimen-type-not-in-enum": (
        "Specimen type must come from the value set.", "'URINE' is not one of",
        lambda d: d["specimens"][0].update(specimen_type="URINE")),
    "condition-not-parkinsonian": (
        "The condition must be a parkinsonian disorder.", "not in dynamic enum 'ParkinsonianDisorderEnum'",
        lambda d: d["diagnoses"][0].update(condition="MONDO:0004975")),
    "phenotype-not-hpo": (
        "Phenotypes must be HPO phenotypic abnormalities.", "not in dynamic enum 'PhenotypeEnum'",
        lambda d: d["phenotype_observations"][0].update(phenotype="UBERON:0001874")),
    "brain-region-not-in-brain": (
        "Imaging regions must be parts of the brain.", "not in dynamic enum 'BrainRegionEnum'",
        lambda d: _imaging(d, brain_region="UBERON:0000178")),
    "visit-before-enrolment": (
        "A visit cannot precede enrolment.", "is before enrolment_date",
        lambda d: d["visits"][0].update(visit_date="2024-02-26")),
    "specimen-from-another-visit": (
        "A measurement's specimen comes from the same visit.", "differs from the visit",
        lambda d: (_second_visit(d), _m(d).update(visit="pdbm:V0002"))),
    "onset-after-diagnosis": (
        "Symptom onset cannot follow diagnosis.", "is after age_at_diagnosis",
        lambda d: d["diagnoses"][0].update(age_at_symptom_onset=67.0)),
    "dangling-reference": (
        "References must resolve to a record in the dataset.", "does not match any Specimen",
        lambda d: _m(d).update(specimen="pdbm:S9999")),
    "duplicate-identifier": (
        "Identifiers are unique within a dataset.", "is already used",
        lambda d: d["participants"].append({**d["participants"][0], "year_of_birth": 1961})),
}


def write(path: Path, data: dict, comment: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    path.write_text(comment + text)


def main() -> None:
    for folder in (VALID, INVALID):
        for old in folder.glob("*.yaml"):
            old.unlink()
    write(VALID / "ParkinsonsStudyDataset-001.yaml", cohort_dataset(),
          "# Synthetic cohort: Parkinson's disease, MSA, prodromal and healthy control participants.\n")
    write(VALID / "ParkinsonsStudyDataset-002.yaml", minimal_dataset(),
          "# Minimal valid dataset; every file in examples/invalid/ changes one thing in it.\n")
    for name, (rule, expect, mutate) in MUTATIONS.items():
        d = minimal_dataset()
        mutate(d)
        write(INVALID / f"ParkinsonsStudyDataset-{name}.yaml", d, f"# Breaks: {rule}\n# Expect: {expect}\n")


if __name__ == "__main__":
    main()
