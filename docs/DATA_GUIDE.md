# Data Guide

## Input Files

| File under `data/inputs/` | Role |
|---|---|
| `trad_NR_first_column_aligned_original_content.xlsx` | The 5,072-row traditional-character NR source, worksheet `Original_Data`. Its original order is used for canonical IDs, text alignment, and previous-word controls. |
| `MCFIX_NR_TSR_NEW_JED351_complete_cases.csv` | The prepared 10,089-row base containing NR/TSR alignment, outcomes, linguistic/Cifu variables and legacy metrics. Removing 39 CKIP-unscorable canonical positions from both tasks leaves 10,011 rows. This is not the initial 10,097-row lexical-eligibility set described in the paper. |
| `Cifu-v1_with_pycantonese_pos.csv` | Cifu lexicon augmented with PyCantonese POS labels and candidate validity fields, for Cifu candidate construction. Original Cifu fields retain upstream meanings. |

## Model Tables

`data/modeling/JED351.csv`, `CKIP_GPT2_tiny.csv`, `Qwen25_7B.csv`, and `CantoneseLLM7B.csv` preserve the archived table contents; no merging or replacement of metric values was applied during packaging. Each contains 5,007 NR and 5,004 TSR rows. The exact source archive and member path for every file are in `SOURCE_MANIFEST.csv`.

The unique row key is **`canonical_row_id` + `TASK`**. `canonical_row_id` alone represents a canonical text position shared by the two tasks. `pure_token` is the lexical target; `IA_LABEL` is the annotated surface, which can carry attached punctuation; `SENTENCE` and `n_in_sent` locate the target. `n_in_sent` is zero based. `sentence_position_1based` is a separate one-based field. Repeated word forms at different positions are distinct observations.

## Column Families

| Family | Columns and interpretation |
|---|---|
| Identity and alignment | `canonical_row_id`, `TASK`, `task_alignment_status`, `WORD`, `SENTENCE`, `IA_LABEL`, `pure_token`, `analysis_token`, `analysis_pos`. |
| Position and length | `n_in_sent`, `sentence_position_1based`, `sentence_length_tokens`, `relative_sentence_position`, `is_sentence_initial`, `is_sentence_final`, `analysis_char_length`. |
| POS and dependency | `pos`, `upos`, `jpos`, `upos*`, `xpos`, `LD2ROOT`, `LD2HEAD`, `DEPTH2ROOT`. Regression uses POS dummies based on `upos*` with the documented label normalization. |
| Original lexical controls | `Freq`, `N_SYL`, `Neighbors_Num`. The baseline uses these original variables; `Neighbors_Num` should not be relabeled as one particular Cifu ND column without tracing its source. |
| Previous-word controls | In unified tables, `source_prev_freq`, `source_prev_n_syl`, `Li_Prev_Freq`, `Li_Prev_N_SYL`. They are derived on the full source sequence before exclusions. Missing sentence-initial previous frequency maps to 0; otherwise the released transformation is `ln(previous_freq + 2)`. Current frequency uses `ln(Freq + 1)`. |
| Cifu matching | `cifu_lookup_word`, `cifu_Word`, `cifu_JyutPing`, `cifu_match`. A match flag is separate from the validity of each individual resource field. |
| Cifu frequency | `cifu_AdultToChild`, `cifu_SpokenAdult`, `cifu_Written`, `cifu_SpokenChildren`, their `_per_million_tokens` forms, and `log1p_cifu_*_per_million_tokens` transforms. `log1p` means natural log of value plus one. |
| Cifu phonological ND | `cifu_ND_w_ins_del_avg_freq`, `cifu_ND_w_ins_del_spok_freq`, `cifu_ND_w_ins_del_writ_freq`, `cifu_ND_no_ins_del_avg_freq`, `cifu_ND_no_ins_del_spok_freq`, `cifu_ND_no_ins_del_writ_freq`, plus retained `log1p_` forms. These are the upstream frequency-weighted variants; unweighted ND from earlier LPPHK explorations is not a predictor in this paper's frozen model. |
| Eye-tracking outcomes | `TOTAL_DURATION`, `IA_FIRST_FIXATION_DURATION`, `IA_SECOND_FIXATION_DURATION` (milliseconds), their `STD_` fields, fixation-presence flags and retained positive-duration log transforms. The reported regressions use the untransformed duration outcomes. |
| Primary LLM measures | The model prefix plus `lexical_surprisal`, `pos_surprisal`, `entropy_before`, `entropy_reduction`; units and adapter differences are in README and implementation notes. |
| Audit and legacy fields | Token IDs/counts, boundary-change flags, normalized text/context/alignment fields, `entropy`, `entropy_after`, other model prefixes in historical tables, and completeness flags. Presence does not imply inclusion in the paper's predictor set. |

For **the complete, file-specific list of every column**, see `DATA_COLUMNS.csv`. Historical and unified tables have different schemas; the schema inventory is more precise than assuming identical columns across all four files.

## Results Files

Each `results/<model>/` directory contains:

- `run_config.json` and `extraction_manifest.json`: original software versions, model IDs, units, sample design, hashes and provenance.
- `fold_assignments.csv`: pooled fold number for every row and each split seed; CKIP also retains historical task-fold metadata, which is not the pooled experiment's split.
- `feature_specifications.csv`: the actual features in each experiment specification.
- `completed_jobs.csv`: completed experiment configurations.
- `all_fold_metrics.csv`, `all_oof_metrics.csv`: fold and concatenated out-of-fold evaluation scores. `all_oof_metrics.csv` contains summary scores, not every token's prediction.
- `metric_additions_by_seed.csv`, `metric_additions_robustness.csv`: improvement over baseline, by seed and summarized across seeds.
- `leave_one_out_ablation_by_seed.csv`, `leave_one_out_ablation_robustness.csv`: conditional contributions of removed blocks.
- `all_performance_metrics_robustness.csv`: across-seed summaries of all retained performance metrics.

Do not treat five split seeds as five independent participant samples, or NR/TSR pooled evaluation subsets as independently trained models.
