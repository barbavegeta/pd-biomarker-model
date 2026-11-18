# Examples

All records are synthetic. `scripts/make_examples.py` generates every file
here; run `just gen-examples` after changing it.

- `valid/ParkinsonsStudyDataset-001.yaml`: a small cohort with Parkinson's
  disease, multiple system atrophy, prodromal and healthy control
  participants, two visits each, MDS-UPDRS, MoCA and Hoehn and Yahr scores,
  CSF seed amplification results, serum NfL, plasma GPNMB on SomaScan and
  Olink, and DaT-SPECT putamen binding ratios.
- `valid/ParkinsonsStudyDataset-002.yaml`: a minimal dataset with one record
  of each kind.
- `invalid/`: copies of the minimal dataset that each break one rule. The
  first two lines of each file name the rule (`# Breaks:`) and the error it
  must raise (`# Expect:`).

Validate a file with all checks (schema structure, ontology terms and
cross-record rules):

```bash
uv run linkml-validate --config validation.yaml examples/valid/ParkinsonsStudyDataset-001.yaml
```

`just validate-examples` checks that every valid file passes and every
invalid file fails, and `tests/test_examples.py` also checks that each
invalid file fails for its own rule.
