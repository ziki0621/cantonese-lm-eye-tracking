# Implementation Notes

Lexical surprisal sums conditional token surprisals. Entropy before describes the next-token distribution before the target; entropy reduction subtracts the next-token entropy after the complete word. The unified pipeline scores sentence-local contexts with a maximum sequence length of 1,024 tokens.

POS surprisal is `-log P(target_POS | context)`. For Cifu-based extraction, Cifu candidate words receive PyCantonese POS labels and candidate probabilities are aggregated by category. Exact candidate settings and units are recorded in the notebooks and extraction manifests.

The archive contains historical CKIP/CantoneseLLM runs and later unified V2 notebooks. Use the model's archived CSV, folds, and manifests when tracing reported results. Original pipeline notes remain in `original_pipeline_README.md`.

`validate_release.py` checks row alignment, controls, folds, metric completeness, hashes, notebook syntax, and manuscript Table 2 values. `reproduce_summary.py` rebuilds tables and a figure from archived per-seed results. These checks do not rerun full GPU extraction or training; exact GPU results can depend on hardware and software versions.

The reported pooled cross-validation splits rows rather than grouping sentences or canonical positions. Matched NR/TSR positions may therefore occur in different folds.
