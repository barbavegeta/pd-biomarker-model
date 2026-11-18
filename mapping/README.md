# Ontology mapping

- `source_dictionary.tsv`: 68 synthetic variables in the style of a study
  export (invented names, short free-text descriptions, units).
- `gold_standard_review.tsv`: the draft gold-standard mapping, one row per
  variable, with the rationale for each choice and columns for the
  reviewer's decision. Rows marked `needs_attention` are judgement calls.

The mapping rules are in [docs/curation-guidelines.md](../docs/curation-guidelines.md).
