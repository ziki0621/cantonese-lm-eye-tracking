# Third-Party Resources and Reuse

## MCFIX

The eye-tracking observations, stimulus text, and original annotations derive from **MCFIX**, released by the authors of Li et al. (2023), *Comparing and Predicting Eye-tracking Data of Mandarin and Cantonese*.

- Official repository: https://github.com/CN-Eyetk/MCFIX
- Paper: https://aclanthology.org/2023.vardial-1.12/

Prepared tables here contain aggregate outcomes and derived annotations. They do not transfer ownership of the source corpus or stimulus text. No explicit blanket license was visible in the upstream repository root at release preparation. This repository does not assign a new license to MCFIX-derived material; consult the original authors for permissions beyond the applicable source terms.

## Cifu

**Regine Lai and Gregoire Winterstein (2020), Cifu: a Frequency Lexicon of Hong Kong Cantonese.**

- Official repository: https://github.com/gwinterstein/Cifu
- Paper: https://aclanthology.org/2020.lrec-1.375/
- Original license: GNU GPL version 3, preserved in `LICENSES/Cifu-GPL-3.0.txt`.

`data/inputs/Cifu-v1_with_pycantonese_pos.csv` is a modified Cifu lexicon: it adds cleaned lookup forms, PyCantonese POS annotations, error/validity metadata used in candidate construction. It is not an unmodified upstream release. Original Cifu content and this Cifu-derived file remain subject to the upstream license. Cifu-derived fields in the modeling tables retain their provenance; they are not newly collected lexical norms.

## Model Checkpoints and Software

Model weights/tokenizers are not included. They are obtained separately from:

- https://huggingface.co/ckiplab/gpt2-tiny-chinese
- https://huggingface.co/jed351/gpt2_tiny_zh-hk-wiki
- https://huggingface.co/Qwen/Qwen2.5-7B
- https://huggingface.co/hon9kon9ize/CantoneseLLMChat-v1.0-7B
- https://huggingface.co/bert-base-chinese

Their respective publishers' terms apply. The project also uses PyTorch, Transformers, minicons, PyCantonese, CatBoost, NumPy, pandas, SciPy, scikit-learn, Matplotlib and related packages under their own licenses. The normalized-text workflow follows the released MCFIX/Li-style preparation and is acknowledged as such.

## Original Research Code

The authors' original research code has no separately selected blanket license in this release. Public access allows inspection but should not be read as an explicit grant of unrestricted reuse. No license here overrides third-party terms. Contact the research authors for clarification or additional permissions.
