# Ontology mapping

An AI agent maps the source dictionary to ontology terms, a curator reviews
every proposal, and the agent is scored against a gold standard the curator
froze beforehand. All mapping sets are SSSOM/TSV, and the rules for agent and
curator alike are in [docs/curation-guidelines.md](../docs/curation-guidelines.md).

## Files

- `source_dictionary.tsv`: 68 synthetic variables in the style of a study
  export (invented names, short free-text descriptions, units).
- `gold_standard_review.tsv`: the gold-standard draft, one row per variable,
  with the rationale for each choice and the curator's decision (`ACCEPT`,
  `CHANGE` or `REJECT`). Rows marked `needs_attention` are judgement calls.
- `gold_standard.sssom.tsv`: the frozen gold standard built from those
  decisions.
- `agent/prompt_<version>.md`: the agent's prompt for each version.
- `runs/<version>/`: one folder per agent run:
  - `proposals.tsv`: the agent's output, and `proposals.sssom.tsv`, the
    same proposals as SSSOM with provenance;
  - `review.tsv` (the curator's decisions) and `reviewed.sssom.tsv`;
  - `score.json` and `errors.tsv`, one row per disagreement with the gold
    standard;
  - `tool_calls.tsv`, every search the agent ran, and `blindness_check.txt`.

## Workflow

Commands run from the repository root with `uv run python`.

1. **Freeze the gold standard** once every row has a decision:
   `scripts/mapping_workflow.py freeze-gold --orcid <ORCID iD> --name "<name>"`
2. **Prepare a workspace** outside the repository, holding only the
   dictionary, the guidelines and the search tool:
   `scripts/prepare_agent_workspace.py v1 ~/mapping-agent/v1`
3. **Run the agent**: start a Claude Code agent with the text of
   `<workspace>/prompt.md`. It searches the ontologies with
   `search_terms.py` and writes `<workspace>/proposals.tsv`; copy that file
   to `runs/v1/`.
4. **Audit the run** from the agent's transcript (in
   `~/.claude/projects/<project>/<session>/subagents/`):
   `scripts/check_agent_transcript.py <transcript> <workspace> mapping/runs/v1`.
   It fails if the agent read, listed or searched anything outside its
   workspace.
5. **Import the proposals** as SSSOM:
   `scripts/mapping_workflow.py import-proposals v1 --tool-version <Claude Code version> --model <model>`
6. **Review**: `scripts/mapping_workflow.py review-sheet v1` writes
   `runs/v1/review.tsv`, with proposals identical to the gold standard
   already accepted. Fill in `decision` for the rest, then run
   `scripts/mapping_workflow.py apply-review v1 --orcid <ORCID iD> --name "<name>"`.
7. **Score**: `scripts/mapping_workflow.py score v1`.

## Scoring

- **Precision**: share of the agent's proposed terms that are the gold term.
- **Recall**: share of gold terms the agent proposed.
- **Predicate agreement**: among correct terms, share with the gold
  predicate.
- **No-term agreement**: among variables with no gold term, share where the
  agent also proposed none.

Each disagreement gets an error type: *missed* (no term proposed),
*spurious* (a term where none applies), *wrong predicate*, *wrong ontology*,
*too broad* or *too narrow* (checked against the ontology hierarchy), or
*wrong term*. The error analysis refines the last into causes such as
synonym confusion or a unit mix-up.
