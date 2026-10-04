from pathlib import Path
import subprocess, sys, json, csv, textwrap
root=Path(__file__).resolve().parents[1]
def run(args):
    print('+',' '.join(args)); subprocess.run(args,cwd=root,check=True)
run([sys.executable,'-m','behavior_lab.generation.generate'])
run([sys.executable,'-m','behavior_lab.data.validate','datasets/behaviorbench/behaviorbench_v1.jsonl'])
run([sys.executable,'scripts/run_benchmark.py'])
run([sys.executable,'scripts/build_contract_benchmark.py'])
run([sys.executable,'scripts/run_contract_benchmark.py'])
run([sys.executable,'scripts/contract_eval.py'])
run([sys.executable,'scripts/method_ablation.py'])
run([sys.executable,'scripts/contract_stats.py'])
run([sys.executable,'scripts/provenance_benchmark.py'])
run([sys.executable,'scripts/build_provenance_intervention.py'])
run([sys.executable,'scripts/run_provenancebench_learned.py'])
run([sys.executable,'scripts/provenancebench_stats_strict.py'])
run([sys.executable,'scripts/provenancebench_multiseed.py'])
run([sys.executable,'scripts/run_trial_eval.py'])
run([sys.executable,'scripts/build_failure_curriculum.py'])
run([sys.executable,'scripts/build_training_mixture.py'])
run([sys.executable,'scripts/launch_gate.py'])
run([sys.executable,'scripts/freeze_protocol.py'])
run([sys.executable,'scripts/run_long_horizon.py'])
run([sys.executable,'-m','behavior_lab.rewards.train'])
run([sys.executable,'scripts/run_reward_hacking.py'])
run([sys.executable,'scripts/build_breakdowns.py'])
run([sys.executable,'scripts/run_ablations.py'])
run([sys.executable,'scripts/mine_failures.py'])
run([sys.executable,'scripts/build_figures.py'])
run([sys.executable,'scripts/regression_gate.py'])
run([sys.executable,'scripts/build_dashboard.py'])
summary=json.loads((root/'results/summary.json').read_text()); rm=json.loads((root/'results/reward_model_metrics.json').read_text())
lines=['# Experiment Report','', '## Scope and interpretation','', 'This report is generated from a fully local, reproducible proxy experiment. It demonstrates the benchmark/evaluation/reward-modeling machinery. It does **not** claim human-study results or performance of frontier language models.','', '## Held-out benchmark','']
for p,s in summary.items():
    lines += [f'### {p}', f"- Overall: {s['overall']['mean']:.4f} (95% bootstrap CI {s['overall']['ci95'][0]:.4f}–{s['overall']['ci95'][1]:.4f})", f"- Personalization: {s['personalization']['mean']:.4f}", f"- Truthfulness: {s['truthfulness']['mean']:.4f}", f"- Sycophancy: {s['sycophancy']['mean']:.4f} (lower is better)", f"- Calibration: {s['calibration']['mean']:.4f}", '']
lines += ['## Reward-model diagnostics', f"- Reward regression MAE: {rm['reward_regression_mae']:.4f}", f"- Pairwise preference accuracy: {rm['pairwise_preference_accuracy']:.4f}", f"- Pairwise preference ROC-AUC: {rm.get('pairwise_preference_auc', float('nan')):.4f}", f"- Candidate responses: {rm['n_candidates']}", f"- Preference pairs: {rm['n_pairs']}", '', '## Next scientific upgrade', 'Swap the proxy policies for real model adapters; collect blinded human labels on the frozen test split; calibrate automatic graders; then re-run the exact same pipeline.']
(root/'reports/EXPERIMENT_REPORT.md').write_text('\n'.join(lines))
print('pipeline complete')
