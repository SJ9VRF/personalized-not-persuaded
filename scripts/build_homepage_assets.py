from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0, str(ROOT))

from behavior_lab.methods.learned_plp import PLPRouter, LICENSE_COLS, baseline_predictions


def bench_us_per_item(fn, n_items: int, warmup: int = 5, reps: int = 100) -> dict[str, float]:
    for _ in range(warmup):
        fn()
    values = []
    for _ in range(reps):
        t0 = time.perf_counter_ns()
        fn()
        values.append((time.perf_counter_ns() - t0) / n_items / 1000.0)
    return {
        "median_us_per_item": float(np.median(values)),
        "p95_us_per_item": float(np.percentile(values, 95)),
    }


def main() -> None:
    df = pd.read_csv(ROOT / "datasets/provenance/provenancebench.csv")
    train = df[df.split == "train"].copy()
    val = df[df.split == "val"].copy()
    ood = df[df.split == "ood_test"].copy()
    router = PLPRouter(include_provenance=True, random_state=7).fit(train, val)

    gold = ood[LICENSE_COLS].astype(int).to_numpy()
    naive = baseline_predictions(ood, "naive")
    naive_ok = (naive.to_numpy() == gold).all(axis=1)
    naive_fail = ~naive_ok

    fns = {
        "naive": lambda: baseline_predictions(ood, "naive"),
        "firewall": lambda: baseline_predictions(ood, "firewall"),
        "provenance_only": lambda: baseline_predictions(ood, "provenance_only"),
        "learned_plp": lambda: router.predict(ood, hybrid=False),
        "hybrid_plp": lambda: router.predict(ood, hybrid=True),
    }

    methods = {}
    for name, fn in fns.items():
        pred = fn()
        ok = (pred.to_numpy() == gold).all(axis=1)
        methods[name] = {
            "success_rate": float(ok.mean()),
            "recovery_on_naive_failures": float(ok[naive_fail].mean()) if naive_fail.any() else None,
            **bench_us_per_item(fn, len(ood)),
            "external_api_cost_usd": 0.0,
        }

    runtime = {
        "scope": "router-only batch evaluation; excludes language-model generation, tools, networking, and serving overhead",
        "split": "ood_test",
        "n_items": int(len(ood)),
        "methods": methods,
    }
    (ROOT / "results/homepage_runtime_summary.json").write_text(json.dumps(runtime, indent=2) + "\n")

    # Select one verified success and one real failure from the frozen trial log.
    trials = []
    for line in (ROOT / "results/trial_trajectories.jsonl").read_text().splitlines():
        if line.strip():
            trials.append(json.loads(line))
    success = next(
        t for t in trials
        if t.get("passed")
        and t.get("input_state", {}).get("provenance") == "tool_verified"
        and any(g.get("name") == "evidence_state_verification" and g.get("expected") == 1 for g in t.get("graders", []))
    )
    failure = next(t for t in trials if not t.get("passed", True))
    out = {
        "source": "results/trial_trajectories.jsonl",
        "note": "Recorded benchmark trials from the frozen Hybrid PLP evaluation; not browser-simulated outcomes.",
        "examples": [success, failure],
    }
    (ROOT / "results/homepage_trial_examples.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(runtime, indent=2))
    print("wrote results/homepage_trial_examples.json")


if __name__ == "__main__":
    main()
