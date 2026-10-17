# Data Guide

## Inputs

| File in `data/inputs/` | Purpose |
|---|---|
| `trad_NR_first_column_aligned_original_content.xlsx` | Original 5,072-row NR source; worksheet `Original_Data`. |
| `MCFIX_NR_TSR_NEW_JED351_complete_cases.csv` | Prepared 10,089-row NR/TSR base, before shared-sample exclusions. |
| `Cifu-v1_with_pycantonese_pos.csv` | Cifu lexicon with PyCantonese POS annotations. |

## Analysis Tables

`data/modeling/` contains `JED351.csv`, `CKIP_GPT2_tiny.csv`, `Qwen25_7B.csv`, and `CantoneseLLM7B.csv`. Each has 10,011 rows: NR 5,007 and TSR 5,004.

Join rows using **`canonical_row_id` + `TASK`**. `pure_token` is the lexical target; `IA_LABEL` is its annotated surface. `SENTENCE` and zero-based `n_in_sent` locate the word.

Primary LLM columns use the model prefix followed by `lexical_surprisal`, `pos_surprisal`, `entropy_before`, or `entropy_reduction`. Additional legacy/audit columns are retained. The paper uses `entropy_before`, not the older `entropy` field.

The baseline uses original lexical, POS, dependency, position, and previous-word controls. Additional `cifu_*` fields retain Cifu frequency and neighbourhood information. Outcomes are `IA_FIRST_FIXATION_DURATION`, `IA_SECOND_FIXATION_DURATION`, and `TOTAL_DURATION`, in milliseconds.

## Results and Inventory

Each `results/<model>/` directory contains fold assignments, feature specifications, per-fold/per-seed scores, robustness summaries, ablations, and run manifests. `all_oof_metrics.csv` contains evaluation scores rather than individual predictions.

See [DATA_COLUMNS.csv](DATA_COLUMNS.csv) for every data column and its nonmissing count, and [SOURCE_MANIFEST.csv](SOURCE_MANIFEST.csv) for source files and hashes.
