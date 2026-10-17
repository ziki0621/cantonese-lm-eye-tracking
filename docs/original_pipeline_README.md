# MCFIX Four-Model Strictly Unified Pipelines

This folder is the frozen `MCFIX_STRICT_UNIFIED_10011_V2` implementation.
The four notebooks were generated from one shared source. Except for the
`MODEL_KEY` selection and the explicitly documented POS-surprisal adapters,
their executable code is identical.

V2 replaces V1 because the V1 Qwen POS adapter summed ordinary float32
probabilities. Very small POS masses could underflow to exact zero, producing
626 missing Qwen POS-surprisal rows. V2 computes every POS mass with
`log_softmax` and `logsumexp`; a dedicated `exp(-1000)` regression test confirms
that the result remains finite. V2 also writes to a new Drive directory and
cannot reuse V1 sentence checkpoints.

## Notebooks

1. `01_MCFIX_JED351_strict_unified_10011_v2_pooled_colab.ipynb`
2. `02_MCFIX_CKIP_GPT2_tiny_strict_unified_10011_v2_pooled_colab.ipynb`
3. `03_MCFIX_Qwen25_7B_strict_unified_10011_v2_pooled_colab.ipynb`
4. `04_MCFIX_CantoneseLLM7B_strict_unified_10011_v2_pooled_colab.ipynb`

Each notebook performs metric extraction, creates its model-specific
10,011-row modeling table, runs pooled NR+TSR CatBoost regression and complete
leave-one-block-out ablations, writes checkpoints to Google Drive, and
downloads one result ZIP.

## Required Inputs

All required files are in `input_files/`:

- `trad_NR_first_column_aligned_original_content.xlsx`
- `MCFIX_NR_TSR_NEW_JED351_complete_cases.csv`
- `Cifu-v1_with_pycantonese_pos.csv`

JED351 and CKIP require all three files. Qwen2.5-7B and CantoneseLLM-7B require
the Excel source and complete-case CSV; the Cifu file is not used by their POS
adapters.

In Colab, either upload the required files into `/content`, or place them in:

```text
MyDrive/MCFIX_strict_unified_inputs/
```

## Frozen Common Steps

The following steps are identical in all four notebooks:

1. Read the same 5,072-row NR source and 10,089-row complete-case base.
2. Apply the same released Li-style text normalization.
3. Align `IA_LABEL` and `pure_token` with the same function.
4. Use preceding Li-normalized `IA_LABEL` text, including punctuation, as the
   lexical and entropy context.
5. Tokenize the context and current `pure_token` independently with
   `add_special_tokens=False`, then concatenate their token IDs after one valid
   model-specific causal start token.
6. Use a uniform maximum sequence length of 1,024 tokens and left-truncate only
   the context when necessary.
7. Compute lexical surprisal in bits as the summed negative log2 probability of
   the complete target token sequence.
8. Compute entropy before in bits from a separate context-only forward pass.
9. Compute entropy after from the context-plus-target sequence, and define
   entropy reduction as `entropy_before - entropy_after`.
10. Extract text metrics once from NR and map them to aligned NR and TSR rows by
    `canonical_row_id`.
11. Exclude the same 39 CKIP-unscorable canonical positions from both tasks,
    producing 10,011 rows: NR 5,007 and TSR 5,004.
12. Compute previous frequency and previous syllable number on the complete
    original 5,072-row sentence sequence before any exclusion, then map those
    fixed controls to every model table.
13. Generate row-wise pooled folds with
    `KFold(n_splits=5, shuffle=True, random_state=seed)` for seeds 42-46.
14. Run pooled NR+TSR CatBoost with `TASK`, 1,000 iterations and CatBoost
    random seed 10.
15. Fit the no-LLM baseline, each single LLM-metric addition, all four metrics,
    leave-one-LLM-metric-out models, and leave-one-linguistic-block-out models.
16. Report MAE, MSE, RMSE, R-squared, Pearson correlation and Spearman
    correlation for pooled OOF predictions and for NR/TSR subsets of those same
    pooled predictions.

## Four Analysis Metrics

Each final model table adds exactly four analysis metrics:

- `MODEL_lexical_surprisal`
- `MODEL_pos_surprisal`
- `MODEL_entropy_before`
- `MODEL_entropy_reduction`

Token counts, target token IDs and boundary-change flags are audit fields, not
additional analysis metrics.

## Authorized POS-Surprisal Differences

POS surprisal is the only intentionally model-specific analysis procedure:

| Model | POS candidate method | Unit |
|---|---|---|
| JED351 | Cifu words, PyCantonese POS, joint token-sequence probability and longest-match subtraction | bits |
| CKIP GPT2-tiny | Same Cifu procedure as JED351 | bits |
| Qwen2.5-7B | PyCantonese-tagged usable single-token model vocabulary; normalized POS mass | nats |
| CantoneseLLM-7B | Existing legacy `cantonese7b_pos_surprisal` from the supplied base table | nats |

The Qwen POS adapter retains its previous unpunctuated lexical-prefix context.
The CantoneseLLM POS values are not recalculated. These are explicit exceptions;
they do not alter lexical surprisal or either entropy metric.

## Common Sample

The supplied complete-case base contains 10,089 rows. The frozen common sample
removes 39 canonical positions for which CKIP lexical surprisal is not reliable,
from both NR and TSR. This removes 78 task rows and leaves 10,011 rows.

All four model regressions must use this exact row identity and order. The
notebooks stop if the row count, task counts, metric completeness, cross-task
mapping, or fold assignments do not satisfy the frozen contract.

## Output Isolation

Each notebook writes to a distinct Google Drive directory:

```text
MyDrive/MCFIX_STRICT_UNIFIED_10011_V2_MODELNAME/
```

Sentence checkpoints are stored under a signature containing the source hashes,
model/tokenizer IDs and revisions, token-boundary definition, POS mode and
pipeline version. Outputs from earlier notebooks are therefore not reused.

## Hardware

- JED351 and CKIP can run on a smaller Colab GPU, although an A100 also works.
- Qwen2.5-7B and CantoneseLLM-7B should use a 40 GB A100 runtime.
- Each notebook loads only one language model and releases it before CatBoost.

## Validation Completed

The delivered notebooks passed:

- JSON and Python-cell compilation;
- normalized cross-notebook executable-code identity;
- frozen-pattern checks for the four metrics and pooled-only regression;
- actual 5,072-row alignment dry run;
- 10,011-row sample and 5,007/5,004 task-count checks;
- exact comparison against the available CKIP 10,011-row pooled fold table for
  all five split seeds;
- a mock causal-model test proving separate context-only entropy and forced
  context/target token boundaries;
- a cached JED351 real-model smoke test of the shared causal scoring sequence.

The full 7B extraction was not run locally because it requires the requested
Colab A100 environment.

