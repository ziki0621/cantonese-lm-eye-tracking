# Cantonese Language Models and Eye-Tracking Prediction

Code, derived data, and archived experiment results accompanying:

**Do Cantonese-Adapted Language Models Better Predict Cantonese Reading? A Cross-Model Eye-Tracking Evaluation**  
Ziqi Zhang, Emmanuele Chersoni, and Mohammad Momenian. Accepted at PACLIC 2026.

[Preprint](https://arxiv.org/abs/2609.02163) · [MCFIX source corpus](https://github.com/CN-Eyetk/MCFIX) · [Cifu lexicon](https://github.com/gwinterstein/Cifu)

The study tests whether language-model information measures improve prediction of Cantonese eye-tracking durations beyond a linguistic baseline. It compares two adaptation contrasts: CKIP GPT-2 Tiny versus JED351, and Qwen2.5-7B versus CantoneseLLM-7B.

## Release Status and Provenance

This release preserves the available experiment artifacts rather than retrospectively changing their calculations. The archived result tables reproduce all **60 entries in Table 2** of the supplied accepted manuscript to its three-decimal precision. The four model datasets contain the same ordered 10,011 observations and the same pooled cross-validation folds.

There is a substantive discrepancy between the manuscript's description of POS surprisal and the archived implementation: **the reported runs did not use one shared Cifu POS candidate inventory across all four models.** JED351 and CKIP use Cifu candidates; Qwen uses a tagged model vocabulary; CantoneseLLM reuses a precomputed legacy POS column. Their POS units also differ. See [implementation notes](docs/IMPLEMENTATION_NOTES.md). This release documents that discrepancy; it does not establish that the POS methods are equivalent or silently replace the reported POS results.

The archived CKIP run predates the unified V2 notebooks, and the archived CantoneseLLM run is V1. The V2 notebooks provide the later common pipeline and explicitly retain these POS adapters. Do not assume that rerunning V2 necessarily reproduces every historical metric bit for bit. Original manifests, historical notebooks, and source hashes are included to make the distinction inspectable.

## Repository Contents

| Path | Contents and purpose |
|---|---|
| `notebooks/01_MCFIX_JED351_strict_unified_10011_v2_pooled_colab.ipynb` | JED351 metric extraction, sample alignment, pooled CatBoost regression, and ablations. |
| `notebooks/02_MCFIX_CKIP_GPT2_tiny_strict_unified_10011_v2_pooled_colab.ipynb` | CKIP implementation in the unified V2 pipeline. |
| `notebooks/03_MCFIX_Qwen25_7B_strict_unified_10011_v2_pooled_colab.ipynb` | Qwen2.5-7B V2 extraction and regression, with the original model-vocabulary POS adapter. |
| `notebooks/04_MCFIX_CantoneseLLM7B_strict_unified_10011_v2_pooled_colab.ipynb` | CantoneseLLM V2 pipeline, reusing the legacy POS column from the base input. |
| `notebooks/historical/` | Available historical CKIP extraction and CantoneseLLM V1 notebooks for tracing the reported runs. Notebook outputs are cleared. |
| `data/inputs/` | Three required source/prepared input files, described below. |
| `data/modeling/` | Four original archived model-specific CSVs, each containing 10,011 observations. |
| `data/audit/` | CKIP exclusions underlying the shared sample. |
| `results/<model>/` | Original per-fold, per-seed and across-seed regression tables, feature specifications, folds, and execution manifests. |
| `scripts/validate_release.py` | CPU-only checks of samples, baseline variables, folds, primary metrics, source hashes, notebook syntax, and Table 2 values. |
| `scripts/reproduce_summary.py` | Recompute summary tables and a Matplotlib figure from archived per-seed results, without retraining models. |
| `results/reproduced/` | Generated Table 2, combined summaries, and mean/SD plot. |
| `results/release_validation/` | Machine-readable validation results and the 60 manuscript-value comparisons. |
| `docs/SOURCE_MANIFEST.csv` | One row per packaged source artifact, including its source filename/archive member, purpose, size, and SHA-256. |
| `docs/DATA_COLUMNS.csv` | Every CSV data column, its inferred dtype, row count, and nonmissing count. |
| `docs/DATA_GUIDE.md` | Data files, row identity, main column groups, and controls. |
| `docs/original_pipeline_README.md` | Preserved original unified-pipeline documentation. |
| `THIRD_PARTY_NOTICES.md`, `LICENSES/` | Resource attribution and applicable third-party license text. |
| `publish_to_github.ps1` | Publish the prepared, committed local repository after GitHub CLI authentication. |

## Models and Measures

| Model | Hugging Face checkpoint | Metric prefix |
|---|---|---|
| JED351 | `jed351/gpt2_tiny_zh-hk-wiki` | `jed351_` |
| CKIP GPT-2 Tiny | `ckiplab/gpt2-tiny-chinese` | `ckip_gpt2_tiny_` |
| Qwen2.5-7B | `Qwen/Qwen2.5-7B` | `qwen25_7b_` |
| CantoneseLLM-7B | `hon9kon9ize/CantoneseLLMChat-v1.0-7B` | `cantonese7b_` |

The CKIP pipeline uses the `bert-base-chinese` tokenizer. Resolved model revisions and original software versions are recorded in the individual manifests; tokenizer revisions were not consistently pinned in the original runs.

Each model supplies four analysis predictors:

1. **Lexical surprisal:** negative log2 joint probability of the target's token sequence, computed by summing conditional token surprisals; unit: bits.
2. **POS surprisal:** negative log category probability, using the model-specific candidate and aggregation procedures documented below. JED351/CKIP: bits; Qwen/CantoneseLLM: nats.
3. **Entropy before:** Shannon entropy of the next-token distribution before the target; unit: bits.
4. **Entropy reduction:** entropy before minus next-token entropy after the complete target; unit: bits. Negative values indicate increased uncertainty.

The unified pipeline uses preceding within-sentence, Li-normalized text with punctuation for lexical and entropy measures. It tokenizes context and target separately, concatenates their token IDs, uses one valid causal start token, and limits the sequence to 1,024 tokens by truncating context as necessary. Entropy before is obtained from a separate context-only forward pass. The documented Qwen POS adapter uses a different, unpunctuated lexical-prefix context.

Older input/CKIP tables contain additional `entropy`, `entropy_after`, or legacy metric columns. Those columns are retained for provenance. The paper's four-metric analysis uses **`entropy_before`**, not the older summed-within-word `entropy` measure. Always select columns by the correct model prefix and the four names above.

## Data and Experimental Design

The frozen analysis contains **10,011 task-level observations**: 5,007 natural-reading (NR) rows and 5,004 task-specific-reading (TSR) rows, spanning 5,007 canonical text positions. The same position can occur once in each task; `(canonical_row_id, TASK)` is the unique row key. These are aggregate eye-tracking measures, not individual-participant recordings.

Outcomes are first fixation duration (FFD, `IA_FIRST_FIXATION_DURATION`), second fixation duration (SFD, `IA_SECOND_FIXATION_DURATION`), and total fixation duration (TFD, `TOTAL_DURATION`), in milliseconds.

The pooled linguistic baseline includes reading task, POS dummies, dependency distances/depth, `Neighbors_Num`, current and previous frequency, current and previous syllable count, and relative sentence position. Although prepared tables retain additional Cifu frequency/ND columns, the archived baseline is defined by the original `Freq` and `Neighbors_Num` controls, not by substituting a selected Cifu written-frequency or ND column.

CatBoost uses 1,000 iterations, internal random seed 10, and five shuffled row-level folds for each split seed 42-46. Each model has 315 experiment jobs, corresponding to 1,575 fold fits. The experiments include the baseline, single-metric additions, all four measures jointly, and leave-one-block-out ablations. NR/TSR summaries evaluate subsets of the pooled models' out-of-fold predictions; they are not separately trained task-specific models.

`delta_mae = baseline_mae - augmented_model_mae`; positive values mean improvement. Ablation contribution uses `removed_model_mae - full_model_mae`. Across-seed SD and positive-seed counts describe stability, not independent significance tests. Pooled row-wise splitting can place matched NR and TSR text positions in different folds; it does not test generalization to entirely unseen sentences or participants.

## Quick Start: Validate and Rebuild Summaries

Use Python 3.12. The archived runs also used Python 3.12; exact original package versions are in `results/<model>/run_config.json`.

```bash
python -m venv .venv
# Activate the virtual environment using your operating system's usual command.
python -m pip install -r requirements.txt
python scripts/validate_release.py
python scripts/reproduce_summary.py
```

These commands do not download model weights or train CatBoost. Validation checks the released data and archives; the summary script rebuilds the reported means and SDs from the per-seed CSVs and writes to `results/reproduced/`.

## Full Extraction and Regression

Open the desired notebook in Google Colab. JED351 and CKIP can use smaller GPUs; the 7B pipelines are intended for a 40 GB A100. The notebooks install their dependencies, mount Google Drive, checkpoint extraction, run regression, and export result ZIPs. One full model run performs substantial GPU computation.

Place the following files from `data/inputs/` in `/content` or Google Drive's `MyDrive/MCFIX_strict_unified_inputs/`:

- `trad_NR_first_column_aligned_original_content.xlsx`
- `MCFIX_NR_TSR_NEW_JED351_complete_cases.csv`
- `Cifu-v1_with_pycantonese_pos.csv` (required for JED351 and CKIP POS extraction)

Run the notebook cells in order. Outputs go to a separate model-specific directory under `MyDrive/MCFIX_STRICT_UNIFIED_10011_V2_<model>/`. Historical notebooks have their own configuration and paths. The prepared complete-case base is an upstream input, not a newly generated output of the four notebooks; it already contains the legacy CantoneseLLM POS values needed by that adapter.

`requirements-extraction.txt` records the notebook package pins and additional dependencies. Install a suitable PyTorch build for the selected GPU runtime. The notebooks use Colab-specific mounting/upload APIs; they are not ordinary local Python scripts. GPU reductions and hardware/library differences can affect exact numerical reproduction. A complete GPU extraction/regression rerun was not performed when assembling this release.

## Main Archived Findings

The complete comparison is in [the regenerated main table](results/reproduced/table2.md). For TFD, mean MAE improvements from lexical surprisal are 0.229 ms (JED351), 0.249 ms (CKIP), 0.599 ms (Qwen2.5-7B), and 0.683 ms (CantoneseLLM-7B). Adding all four measures yields 0.409, 0.651, 0.821, and 1.251 ms, respectively. Entropy reduction instead favors CKIP. Model rankings therefore depend on the measure, and the absolute predictive gains are modest. POS comparisons should be interpreted with the implementation differences above.

## Attribution and Reuse

MCFIX data and annotations originate with Li et al. (2023). Cifu originates with Lai and Winterstein (2020); its upstream repository carries GPL-3.0, which is preserved for the included Cifu-derived lexicon. Models and tokenizers are obtained from their respective publishers and are not redistributed here. See [third-party notices](THIRD_PARTY_NOTICES.md).

No blanket license is assigned here to third-party MCFIX material or to the authors' original code. Public availability alone does not establish an unrestricted reuse license. The third-party resources retain their original terms and attribution; this repository does not override them.

## Citation

```bibtex
@inproceedings{zhang2026cantonese,
  title = {Do Cantonese-Adapted Language Models Better Predict Cantonese Reading? A Cross-Model Eye-Tracking Evaluation},
  author = {Zhang, Ziqi and Chersoni, Emmanuele and Momenian, Mohammad},
  booktitle = {Proceedings of PACLIC 2026},
  year = {2026},
  note = {Accepted; proceedings details pending},
  url = {https://arxiv.org/abs/2609.02163}
}
```

Please also cite the [MCFIX paper](https://aclanthology.org/2023.vardial-1.12/), the [Cifu paper](https://aclanthology.org/2020.lrec-1.375/), and the model/software resources relevant to your use. Update the provisional PACLIC bibliographic details when the proceedings are available.
