# Cantonese Language Models and Eye-Tracking Prediction

Code and data for **Do Cantonese-Adapted Language Models Better Predict Cantonese Reading? A Cross-Model Eye-Tracking Evaluation**, by Ziqi Zhang, Emmanuele Chersoni, and Mohammad Momenian. arXiv preprint, 2026.

[arXiv](https://arxiv.org/abs/2609.02163) | [MCFIX](https://github.com/CN-Eyetk/MCFIX) | [Cifu](https://github.com/gwinterstein/Cifu)

We compare CKIP GPT-2 Tiny, JED351, Qwen2.5-7B, and CantoneseLLM-7B on predicting Cantonese eye-tracking durations using four information-theoretic measures:

- **Lexical surprisal:** unexpectedness of the target word, summed over its tokens.
- **POS surprisal:** unexpectedness of the target's syntactic category.
- **Entropy before:** uncertainty over the next token before the target.
- **Entropy reduction:** entropy before minus entropy after the complete target.

## Files

| Directory | Contents |
|---|---|
| `notebooks/` | Four model pipelines for extraction, regression, and ablation; historical notebooks are in `historical/`. |
| `data/inputs/` | Source workbook, prepared NR/TSR base, and POS-annotated Cifu lexicon. |
| `data/modeling/` | Final analysis CSV for each model. |
| `data/audit/` | Sample-exclusion records. |
| `results/<model>/` | Fold assignments, regression results, feature definitions, and run configurations. |
| `results/reproduced/` | Rebuilt summary tables and figure. |
| `scripts/` | Data validation and summary-generation scripts. |
| `docs/` | Brief data/implementation notes, complete column inventory, and source-file hashes. |

## Data and Analysis

Each model table contains **10,011 observations**: 5,007 natural-reading (NR) and 5,004 task-specific-reading (TSR) rows. The unique key is `(canonical_row_id, TASK)`. Outcomes are first, second, and total fixation durations in milliseconds.

The pooled CatBoost analysis uses 1,000 iterations, model seed 10, and five shuffled row-level folds for split seeds 42-46. It evaluates single-metric additions, all four metrics, and ablations against a linguistic baseline. Positive `delta_mae = baseline_mae - augmented_mae` indicates improvement. NR/TSR scores are subsets of pooled out-of-fold evaluation.

## Run

For validation and summaries, use Python 3.12:

```bash
python -m pip install -r requirements.txt
python scripts/validate_release.py
python scripts/reproduce_summary.py
```

For full extraction and regression, open a model notebook in Google Colab and run its cells in order. Place the files from `data/inputs/` in `/content` or `MyDrive/MCFIX_strict_unified_inputs/`. The 7B notebooks are intended for a 40 GB A100. Dependencies are recorded in `requirements-extraction.txt`; model weights are downloaded separately.

The released results reproduce all 60 rounded entries in manuscript Table 2. The archive includes historical runs and later unified notebooks; consult the associated manifests for exact extraction settings, units, and software versions.

## Citation and Resources

```bibtex
@misc{zhang2026cantonese,
  title = {Do Cantonese-Adapted Language Models Better Predict Cantonese Reading? A Cross-Model Eye-Tracking Evaluation},
  author = {Zhang, Ziqi and Chersoni, Emmanuele and Momenian, Mohammad},
  year = {2026},
  eprint = {2609.02163},
  archivePrefix = {arXiv},
  primaryClass = {cs.CL},
  doi = {10.48550/arXiv.2609.02163},
  url = {https://arxiv.org/abs/2609.02163}
}
```

Please also cite [MCFIX (Li et al., 2023)](https://aclanthology.org/2023.vardial-1.12/) and [Cifu (Lai and Winterstein, 2020)](https://aclanthology.org/2020.lrec-1.375/). Resource attribution and reuse terms are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
