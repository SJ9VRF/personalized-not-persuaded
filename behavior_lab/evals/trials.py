from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, List

CHANNELS = ("presentation", "personalization", "evidence")

@dataclass
class GraderResult:
    name: str
    passed: bool
    expected: int
    observed: int
    weight: float
    detail: str

@dataclass
class Trial:
    trial_id: str
    task_id: str
    split: str
    input_state: Dict[str, Any]
    trajectory: List[Dict[str, Any]]
    graders: List[GraderResult]
    passed: bool
    weighted_score: float


def build_trial(row: Dict[str, Any], method: str = "hybrid") -> Trial:
    task_id = str(row["case_id"])
    pred_prefix = f"{method}_"
    trajectory = [
        {"step": 0, "event": "context_ingested", "scope": row["scope"], "provenance": row["provenance"]},
        {"step": 1, "event": "license_prediction", "method": method,
         "licenses": {c: int(row[f"{pred_prefix}{c}_license"]) for c in CHANNELS}},
    ]
    if method == "hybrid":
        blocked = []
        if not bool(row["current"]): blocked.append("stale")
        if float(row["confidence"]) < 0.5: blocked.append("low_confidence")
        if not bool(row["relevant"]): blocked.append("irrelevant")
        trajectory.append({"step": 2, "event": "validity_gates", "blocked_by": blocked})
    graders: List[GraderResult] = []
    weights = {"presentation": 1.0, "personalization": 1.0, "evidence": 2.0}
    for c in CHANNELS:
        exp = int(row[f"{c}_license"])
        obs = int(row[f"{pred_prefix}{c}_license"])
        graders.append(GraderResult(
            name=f"{c}_state_verification",
            passed=exp == obs,
            expected=exp,
            observed=obs,
            weight=weights[c],
            detail=f"Verify final {c} license against the frozen contract state.",
        ))
    denom = sum(g.weight for g in graders)
    score = sum(g.weight for g in graders if g.passed) / denom
    passed = all(g.passed for g in graders)
    trajectory.append({"step": len(trajectory), "event": "state_verification", "passed": passed, "score": score})
    return Trial(
        trial_id=f"TRIAL-{method.upper()}-{task_id}",
        task_id=task_id,
        split=str(row.get("split_eval", row.get("split", "unknown"))),
        input_state={k: row[k] for k in ["task_kind", "signal_content", "scope", "provenance", "confidence", "current", "relevant"]},
        trajectory=trajectory,
        graders=graders,
        passed=passed,
        weighted_score=score,
    )


def trial_to_dict(trial: Trial) -> Dict[str, Any]:
    d = asdict(trial)
    d["graders"] = [asdict(g) for g in trial.graders]
    return d
