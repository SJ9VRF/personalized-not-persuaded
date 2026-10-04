from pathlib import Path
import sys
import json
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from behavior_lab.evals.trials import build_trial, trial_to_dict
IN = ROOT / "results/provenancebench_predictions.csv"
OUT = ROOT / "results/trial_trajectories.jsonl"
SUMMARY = ROOT / "results/trial_eval_summary.json"

df = pd.read_csv(IN)
rows = df.to_dict(orient="records")
trials = [build_trial(r, method="hybrid") for r in rows]
OUT.write_text("\n".join(json.dumps(trial_to_dict(t), sort_keys=True) for t in trials) + "\n")
by_split = {}
for t in trials:
    x = by_split.setdefault(t.split, {"n": 0, "passed": 0, "score_sum": 0.0})
    x["n"] += 1; x["passed"] += int(t.passed); x["score_sum"] += t.weighted_score
summary = {
    "method": "hybrid",
    "n_trials": len(trials),
    "pass_rate": sum(t.passed for t in trials) / len(trials),
    "mean_weighted_state_score": sum(t.weighted_score for t in trials) / len(trials),
    "by_split": {k: {"n": v["n"], "pass_rate": v["passed"]/v["n"], "mean_weighted_state_score": v["score_sum"]/v["n"]} for k,v in by_split.items()},
    "interpretation": "Task/trial/grader/trajectory view of licensing behavior. State verification is against the frozen contract, not a claim of end-to-end generation quality."
}
SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
print(json.dumps(summary, indent=2))
