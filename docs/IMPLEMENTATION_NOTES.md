# Implementation and Historical Result Provenance

## What the Archive Demonstrates

`scripts/validate_release.py` verifies ordered sample identities, baseline raw controls/outcomes, pooled folds, finite primary measures, cross-task metric identity, notebook Python syntax, and source-file hashes. All 60 rounded mean improvements in manuscript Table 2 match the archived tables. This validates packaging and table correspondence, not the scientific equivalence of different POS definitions or a complete end-to-end rerun.

## POS Surprisal

| Model | Archived procedure | Unit | Provenance |
|---|---|---|---|
| JED351 | Cifu candidate words with PyCantonese POS labels; candidate token-sequence probabilities and longest-match residual subtraction | bits | V2 extraction manifest and notebook |
| CKIP GPT-2 Tiny | Cifu procedure with historical minicons-based extraction/alignment | bits | Historical common-complete-case archive; `extraction_manifest.json` is the original `pipeline_manifest.json` |
| Qwen2.5-7B | Usable single-token model vocabulary tagged by PyCantonese; normalized POS mass with stable log-space aggregation; unpunctuated lexical-prefix context | nats | V2 extraction manifest and original unified Colab notebook |
| CantoneseLLM-7B | Reuses `cantonese7b_pos_surprisal` already present in the prepared base | nats | V1 archived extraction manifest and historical notebook |

The manuscript's statement that all four use a common Cifu candidate inventory is not supported by these archived manifests and code. The supplied Kaggle notebook whose name ends in `cifu_pos` is a different variant; it is not used here to describe the archived Qwen results. Changing an adapter would require new extraction and regression, producing a new analysis rather than reproducing the archived paper results. A bit/nat conversion alone does not harmonize candidate sets or contexts.

## Historical Versus Unified Pipeline

- JED351 and Qwen results were taken from their `MCFIX_STRICT_UNIFIED_10011_V2_*_RESULTS.zip` archives.
- CantoneseLLM results came from the V1 archive; V2 was introduced to stabilize Qwen POS mass calculations and has different checkpoint signatures.
- CKIP results came from `MCFIX_CKIP_common_complete_case_pooled_only_results.zip`, with its original tokenizer/alignment metadata. Its original `reference_sample` description includes stale “10,061” wording, while its actual table, run configuration, task counts, folds, and matched Table 2 values establish the 10,011-row sample.
- The four V2 notebooks are included as the later shared implementation. Historical notebooks are supplied where available, but the original historical CKIP notebook should not be assumed to export the final frozen common sample without its later common-case preparation. The archived CKIP CSV and folds are authoritative for the reported regressions.
- Some legacy columns in CKIP/input tables belong to other models or earlier definitions. Only the model's own four designated columns should be used for the corresponding reported four-metric model.

## Limits of Reproduction

Model revision IDs were recorded for the archived extractions, but tokenizer revision IDs were not consistently recorded, and the notebooks fetch model resources without a universal revision pin. Package pins and manifests are retained; no claim of bitwise GPU determinism is made. The original prepared input table and source workbook are included, avoiding a need to reconstruct them from undocumented intermediate files.

Row-level pooled KFold permits the same canonical text position to occur in different training/test tasks. The released results reproduce that design; grouped sentence/position evaluation would answer a different generalization question and should be reported separately.
