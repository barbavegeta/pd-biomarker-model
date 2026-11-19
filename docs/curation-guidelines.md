# Curation guidelines

These rules govern how a source variable is mapped to an ontology term. The
gold-standard mapping follows them, the mapping agent is instructed with
them, and a reviewer applies them when accepting, rejecting or correcting a
proposal.

## What is mapped

Each source variable is mapped once, to the concept the variable records.
A yes/no variable for "rest tremor" records the phenotype *Resting tremor*;
a variable holding a serum NfL concentration records the laboratory test
for NfL mass concentration in serum or plasma.

Read the name, the description and the unit together. Abbreviations are
resolved from the description and unit, never from the name alone (*SAA*
is a seed amplification assay here, not serum amyloid A; *PD* is Parkinson's
disease, not peritoneal dialysis; *RBD* is REM sleep behaviour disorder, not
a receptor-binding domain).

## Target vocabularies

Use the first vocabulary that applies:

1. **Diagnoses** (a disease present or absent): MONDO.
2. **Signs and symptoms**: HPO, even when a disease of the same name exists
   in MONDO.
3. **Laboratory tests**: LOINC. The code must agree with the variable on
   component, specimen, property and, if the variable states it, method.
   The unit decides the property: a mass unit (pg/mL, ng/L, mg/L) takes a
   *Mass/volume* code, a molar unit (pmol/L, µmol/L) a *Moles/volume* code.
4. **Rating scales**: LOINC when a code exists for the same instrument
   version and score; otherwise NCIT. MDS-UPDRS is not the original UPDRS,
   and the Hoehn and Yahr stage rated in MDS-UPDRS is not the modified Hoehn
   and Yahr scale.
5. **Analyte measurements without a LOINC code**, including SomaScan (RFU)
   and Olink (NPX) values: the protein in NCIT, with `skos:relatedMatch`.
   A relative unit is never mapped to a concentration test.
6. **Study administration and demographics**: NCIT (CDISC concepts).

Only current terms are used; obsolete terms are replaced by their successor.

## Predicates

- `skos:exactMatch`: the term means the same as the variable, including
  specimen, property and instrument version.
- `skos:broadMatch`: the term is more general than the variable (a
  questionnaire for one of its total scores; *Cognitive impairment* for
  PD mild cognitive impairment).
- `skos:narrowMatch`: the term is more specific than the variable.
- `skos:relatedMatch`: associated but neither equivalent nor hierarchical
  (a measurement and its analyte; a carrier status and the genetic disease).

When no term meets these rules, the object is `sssom:NoTermFound`. Proposing
no term is better than proposing a wrong one.

## Provenance

Every mapping records who made it (`author_id`: an ORCID for a person, a
versioned agent identifier for an AI agent), how (`mapping_justification`:
`semapv:ManualMappingCuration` for a person; `semapv:CompositeMatching` for
the agent, which combines lexical search with its own judgement), when
(`mapping_date`) and, for agent proposals, with what (`mapping_tool`,
`mapping_tool_version`, `confidence`). The `curator_type` column records
whether the author was a person or an AI agent.

A review never overwrites a proposal. The reviewer adds `reviewer_id` and
`reviewer_agreement` to it: 1.0 to accept, -1.0 to reject. A correction is a
rejection plus a new mapping authored by the reviewer, so the original
proposal stays in the file.
