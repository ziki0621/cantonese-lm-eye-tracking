"""Validate archived samples, folds, paper values and source-file hashes without a GPU."""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODELS = {'JED351': 'jed351_', 'CKIP_GPT2_tiny': 'ckip_gpt2_tiny_',
          'Qwen25_7B': 'qwen25_7b_', 'CantoneseLLM7B': 'cantonese7b_'}
METRICS = ('lexical_surprisal', 'pos_surprisal', 'entropy_before', 'entropy_reduction')
KEY = ['canonical_row_id', 'TASK']
FOLDS = [f'pooled_fold_seed_{seed}' for seed in range(42, 47)]
# Table 2 in the accepted manuscript; model order follows MODELS.
PAPER = {
    'lexical_surprisal': [[.118, .196, .268, .297], [.064, .081, .152, .161], [.229, .249, .599, .683]],
    'pos_surprisal': [[.118, .200, .276, .308], [.002, .018, .015, .050], [.124, .231, .321, .478]],
    'entropy_before': [[.147, .112, .163, .293], [.008, .042, .016, .097], [.133, .101, .175, .478]],
    'entropy_reduction': [[.152, .183, .153, .156], [-.008, .104, -.003, .009], [.159, .362, .163, .162]],
    'all_four': [[.409, .504, .597, .729], [.125, .197, .200, .267], [.409, .651, .821, 1.251]],
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    report = {'status': 'passed', 'checks': [], 'models': {}}
    manifest = pd.read_csv(ROOT / 'docs/SOURCE_MANIFEST.csv')
    for row in manifest.itertuples():
        actual = hashlib.sha256((ROOT / row.path).read_bytes()).hexdigest()
        require(actual == row.sha256, f'Hash mismatch: {row.path}')
    report['checks'].append(f'{len(manifest)} source-file SHA-256 hashes')
    reference = None
    reference_folds = None
    reference_controls = None
    control_cols = ['SENTENCE', 'n_in_sent', 'pure_token', 'Freq', 'N_SYL', 'LD2ROOT',
                    'LD2HEAD', 'DEPTH2ROOT', 'Neighbors_Num', 'TOTAL_DURATION',
                    'IA_FIRST_FIXATION_DURATION', 'IA_SECOND_FIXATION_DURATION']
    paper_rows = []
    for m, (label, prefix) in enumerate(MODELS.items()):
        df = pd.read_csv(ROOT / f'data/modeling/{label}.csv', low_memory=False)
        require(len(df) == 10011, f'{label}: unexpected sample size')
        require(df.TASK.value_counts().to_dict() == {'NR': 5007, 'TSR': 5004}, f'{label}: task counts')
        require(not df.duplicated(KEY).any(), f'{label}: duplicate row IDs')
        require(df.canonical_row_id.nunique() == 5007, f'{label}: canonical positions')
        cols = [prefix + metric for metric in METRICS]
        require(np.isfinite(df[cols].to_numpy(dtype=float)).all(), f'{label}: nonfinite primary metrics')
        require(df.groupby('canonical_row_id')[cols].nunique().le(1).all().all(),
                f'{label}: text metrics differ across tasks')
        if reference is None:
            reference = df[KEY]
            reference_controls = df[control_cols]
        else:
            pd.testing.assert_frame_equal(reference, df[KEY], check_dtype=False)
            pd.testing.assert_frame_equal(reference_controls, df[control_cols], check_dtype=False)
        folds = pd.read_csv(ROOT / f'results/{label}/fold_assignments.csv')
        pd.testing.assert_frame_equal(reference, folds[KEY], check_dtype=False)
        require(folds[FOLDS].isin(range(1, 6)).all().all(), f'{label}: invalid fold IDs')
        if reference_folds is None:
            reference_folds = folds[FOLDS]
        else:
            pd.testing.assert_frame_equal(reference_folds, folds[FOLDS], check_dtype=False)
        summary = pd.read_csv(ROOT / f'results/{label}/metric_additions_robustness.csv')
        for metric, values in PAPER.items():
            spec = 'all_four' if metric == 'all_four' else 'add_' + metric
            for i, target in enumerate(('FFD', 'SFD', 'TFD')):
                sub = summary.loc[(summary.evaluation_scope == 'POOLED') &
                                  (summary.target == target) & (summary.specification == spec)]
                require(len(sub) == 1, f'{label}/{spec}/{target}: ambiguous result')
                actual = float(sub.iloc[0].mean_delta_mae)
                expected = values[i][m]
                require(abs(actual - expected) <= .000500001,
                        f'Paper mismatch: {label}/{spec}/{target}: {actual} vs {expected}')
                paper_rows.append({'model': label, 'metric': metric, 'outcome': target,
                                   'archived_mean_delta_mae': actual, 'paper_rounded': expected})
        report['models'][label] = {'rows': len(df), 'unique_positions': 5007,
                                    'task_counts': df.TASK.value_counts().to_dict()}
    report['checks'] += ['Shared ordered row identities and baseline controls/outcomes',
                         'Shared five-seed pooled fold assignments',
                         'All primary metrics finite and identical across matched NR/TSR positions',
                         'All 60 Table 2 values match archived results at manuscript precision']
    for p in (ROOT / 'notebooks').rglob('*.ipynb'):
        notebook = json.loads(p.read_text(encoding='utf-8'))
        for i, cell in enumerate(notebook['cells']):
            if cell['cell_type'] == 'code':
                source = ''.join(cell.get('source', []))
                # IPython installation and shell lines are valid notebook syntax, not Python AST.
                source = '\n'.join(line for line in source.splitlines()
                                   if not line.lstrip().startswith(('%', '!')))
                ast.parse(source, filename=f'{p.name}:cell{i}')
                require(not cell.get('outputs'), f'{p.name}: uncleared output')
    report['checks'].append('All notebook Python cells parse; execution output cleared')
    regenerated_path = ROOT / 'results/reproduced/metric_additions_recomputed.csv'
    if regenerated_path.exists():
        regenerated = pd.read_csv(regenerated_path)
        count = 0
        for label in MODELS:
            archived = pd.read_csv(ROOT / f'results/{label}/metric_additions_robustness.csv')
            merged = regenerated.loc[regenerated.model.eq(label)].merge(
                archived, on=['evaluation_scope', 'target', 'specification'],
                validate='one_to_one', suffixes=('_new', '_archive'))
            require(len(merged) == 45, f'{label}: incomplete regenerated summary')
            for field in ('mean_delta_mae', 'sd_delta_mae'):
                require(np.allclose(merged[field + '_new'], merged[field + '_archive'],
                                    atol=1e-12, rtol=0), f'{label}: regenerated {field} mismatch')
            count += len(merged)
        report['checks'].append(f'{count} regenerated mean/SD pairs match archived summaries')
    out = ROOT / 'results/release_validation'
    out.mkdir(parents=True, exist_ok=True)
    (out / 'validation.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    pd.DataFrame(paper_rows).to_csv(out / 'table2_value_check.csv', index=False)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
