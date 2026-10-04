from __future__ import annotations
from typing import Any, Dict, Iterable, List

CHANNELS = ("presentation", "personalization", "evidence")


def classify_failure(row: Dict[str, Any], method: str = "hybrid") -> List[str]:
    failures = []
    for c in CHANNELS:
        target = int(row[f"{c}_license"])
        pred = int(row[f"{method}_{c}_license"])
        if target == pred:
            continue
        if target == 1:
            failures.append(f"{c}:starvation")
        else:
            failures.append(f"{c}:leakage")
    return failures


def priority_score(row: Dict[str, Any], failure_types: Iterable[str]) -> float:
    score = 0.0
    for f in failure_types:
        channel, kind = f.split(":", 1)
        score += 4.0 if channel == "evidence" else 2.0 if channel == "personalization" else 1.0
        if kind == "leakage": score += 1.0
    split = str(row.get("split_eval", ""))
    if "provenance_intervention" in split: score += 2.0
    elif "compositional" in split: score += 1.5
    elif "ood" in split: score += 1.0
    if float(row.get("confidence", 1.0)) < 0.5: score += 0.5
    if not bool(row.get("current", 1)): score += 0.5
    if not bool(row.get("relevant", 1)): score += 0.5
    return score


def build_training_example(row: Dict[str, Any], method: str = "hybrid") -> Dict[str, Any] | None:
    failure_types = classify_failure(row, method=method)
    if not failure_types:
        return None
    target = {c: int(row[f"{c}_license"]) for c in CHANNELS}
    observed = {c: int(row[f"{method}_{c}_license"]) for c in CHANNELS}
    return {
        "example_id": f"CURR-{row['case_id']}",
        "source_case_id": str(row["case_id"]),
        "split": str(row.get("split_eval", row.get("split", "unknown"))),
        "failure_types": failure_types,
        "priority": priority_score(row, failure_types),
        "input": {
            "task_kind": row["task_kind"],
            "signal": row["signal_content"],
            "scope": row["scope"],
            "provenance": row["provenance"],
            "confidence": float(row["confidence"]),
            "current": bool(row["current"]),
            "relevant": bool(row["relevant"]),
        },
        "observed_licenses": observed,
        "target_licenses": target,
        "training_target": {
            "type": "license_correction",
            "supervision": target,
            "rationale": "Correct the failed license decision while preserving channels that already matched the frozen contract.",
        },
    }
