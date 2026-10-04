from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
s = pd.read_csv(ROOT / "results/provenancebench_method_summary.csv")

def val(method, split, col):
    r = s[(s.method == method) & (s.split == split)]
    if len(r) != 1:
        raise RuntimeError(f"Missing unique row for {method}/{split}")
    return float(r.iloc[0][col])

checks = []
def check(name, observed, predicate, requirement):
    checks.append({"name": name, "observed": observed, "requirement": requirement, "passed": bool(predicate(observed))})

check("hybrid_id_exact", val("hybrid_plp", "test", "exact_license_match"), lambda x: x >= 0.95, ">=0.95")
check("hybrid_ood_exact", val("hybrid_plp", "ood_test", "exact_license_match"), lambda x: x >= 0.90, ">=0.90")
check("hybrid_compositional_exact", val("hybrid_plp", "compositional_test", "exact_license_match"), lambda x: x >= 0.75, ">=0.75")
check("hybrid_ood_unsupported_leakage", val("hybrid_plp", "ood_test", "unsupported_leakage"), lambda x: x <= 0.02, "<=0.02")
check("hybrid_ood_evidence_uptake", val("hybrid_plp", "ood_test", "evidence_uptake"), lambda x: x >= 0.75, ">=0.75")
trial = json.loads((ROOT / "results/trial_eval_summary.json").read_text())
check("trial_weighted_state_score", float(trial["mean_weighted_state_score"]), lambda x: x >= 0.90, ">=0.90")

out = {"gate": "research_candidate", "passed": all(x["passed"] for x in checks), "checks": checks,
       "scope": "Controlled licensing research gate only. Not a production launch approval."}
(ROOT / "results/launch_gate.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
print(json.dumps(out, indent=2))
if not out["passed"]:
    raise SystemExit(1)
