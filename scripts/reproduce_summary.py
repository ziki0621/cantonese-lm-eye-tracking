"""Rebuild manuscript summary tables and figures from archived per-seed results."""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MODELS = ('JED351', 'CKIP_GPT2_tiny', 'Qwen25_7B', 'CantoneseLLM7B')
LABELS = ('JED351', 'CKIP', 'Qwen2.5-7B', 'CantoneseLLM-7B')
METRICS = ('lexical_surprisal', 'pos_surprisal', 'entropy_before', 'entropy_reduction', 'all_four')
NAMES = ('Lexical surprisal', 'POS surprisal', 'Entropy before', 'Entropy reduction', 'All four')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'results/reproduced')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    records = []
    ablations = []
    for model in MODELS:
        df = pd.read_csv(ROOT / f'results/{model}/metric_additions_by_seed.csv')
        if df.duplicated(['split_seed', 'evaluation_scope', 'target', 'specification']).any():
            raise ValueError(f'Duplicate per-seed results for {model}')
        df['percent_delta_mae'] = 100 * df.delta_mae / df.baseline_mae
        summary = df.groupby(['evaluation_scope', 'target', 'specification'], as_index=False).agg(
            mean_delta_mae=('delta_mae', 'mean'), sd_delta_mae=('delta_mae', 'std'),
            mean_percent_delta_mae=('percent_delta_mae', 'mean'),
            sd_percent_delta_mae=('percent_delta_mae', 'std'),
            positive_seed_count=('delta_mae', lambda x: int((x > 0).sum())),
            n_seeds=('split_seed', 'nunique'))
        if not summary.n_seeds.eq(5).all():
            raise ValueError(f'Incomplete seeds for {model}')
        summary.insert(0, 'model', model)
        records.append(summary)
        abl = pd.read_csv(ROOT / f'results/{model}/leave_one_out_ablation_robustness.csv')
        abl.insert(0, 'model', model)
        ablations.append(abl)
    summary = pd.concat(records, ignore_index=True)
    summary.to_csv(args.output / 'metric_additions_recomputed.csv', index=False)
    pd.concat(ablations, ignore_index=True).to_csv(args.output / 'ablation_summary_combined.csv', index=False)
    pooled = summary.loc[summary.evaluation_scope.eq('POOLED')]
    table = pooled.pivot(index=['specification', 'target'], columns='model', values='mean_delta_mae')[list(MODELS)]
    table.to_csv(args.output / 'table2_mean_delta_mae.csv')
    lines = ['| Metric | Outcome | ' + ' | '.join(LABELS) + ' |', '|---|---|' + '---:|' * 4]
    for metric, name in zip(METRICS, NAMES):
        spec = metric if metric == 'all_four' else 'add_' + metric
        for outcome in ('FFD', 'SFD', 'TFD'):
            values = table.loc[(spec, outcome)]
            lines.append(f'| {name} | {outcome} | ' + ' | '.join(f'{x:+.3f}' for x in values) + ' |')
    (args.output / 'table2.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False})
    fig, axes = plt.subplots(5, 3, figsize=(12, 14), layout='constrained')
    colors = ('#2878a5', '#666666', '#bd7c20', '#b64a5b')
    for row, (metric, name) in enumerate(zip(METRICS, NAMES)):
        spec = metric if metric == 'all_four' else 'add_' + metric
        for col, outcome in enumerate(('FFD', 'SFD', 'TFD')):
            ax = axes[row, col]
            sub = pooled.loc[pooled.specification.eq(spec) & pooled.target.eq(outcome)].set_index('model').loc[list(MODELS)]
            ax.bar(np.arange(4), sub.mean_delta_mae, yerr=sub.sd_delta_mae,
                   color=colors, capsize=3, width=.65)
            ax.axhline(0, color='black', linewidth=.7)
            ax.set_xticks(np.arange(4), LABELS, rotation=25, ha='right', fontsize=8)
            ax.set_title(f'{name}: {outcome}', fontsize=11)
            ax.set_ylabel('Delta MAE (ms)')
    fig.savefig(args.output / 'metric_additions_mean_sd.png', dpi=200)
    plt.close(fig)
    print(f'Rebuilt summaries and figure: {args.output}')


if __name__ == '__main__':
    main()
