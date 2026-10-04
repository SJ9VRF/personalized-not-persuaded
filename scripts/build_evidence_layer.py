from __future__ import annotations

import json
import shutil
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "evidence"

for name in ["experiment_logs", "eval_runs", "failure_examples", "plots", "configs", "qualitative_cases", "ablations"]:
    (OUT / name).mkdir(parents=True, exist_ok=True)

# Canonical evidence copies. These are snapshots for review; results/ remains source of truth.
copy_map = {
    "results/provenancebench_method_summary.csv": "eval_runs/provenancebench_method_summary.csv",
    "results/provenancebench_strict_stats.csv": "eval_runs/provenancebench_strict_stats.csv",
    "results/provenancebench_multiseed.csv": "eval_runs/provenancebench_multiseed.csv",
    "results/provenancebench_calibration.csv": "eval_runs/provenancebench_calibration.csv",
    "results/trial_eval_summary.json": "eval_runs/trial_eval_summary.json",
    "results/launch_gate.json": "eval_runs/launch_gate.json",
    "results/failure_curriculum_summary.json": "eval_runs/failure_curriculum_summary.json",
    "results/training_mixture_manifest.json": "eval_runs/training_mixture_manifest.json",
    "results/provenancebench_errors.csv": "failure_examples/provenancebench_errors.csv",
    "results/homepage_trial_examples.json": "qualitative_cases/recorded_trial_examples.json",
    "results/trial_trajectories.jsonl": "qualitative_cases/trial_trajectories.jsonl",
}
for src, dst in copy_map.items():
    s, d = ROOT / src, OUT / dst
    if s.exists():
        shutil.copy2(s, d)

method = pd.read_csv(ROOT / "results/provenancebench_method_summary.csv")
strict = pd.read_csv(ROOT / "results/provenancebench_strict_stats.csv")
errors = pd.read_csv(ROOT / "results/provenancebench_errors.csv")
multiseed = pd.read_csv(ROOT / "results/provenancebench_multiseed.csv")

# Focused ablation table.
ab = method[method["method"].isin(["provenance_only", "learned_plp", "hybrid_plp", "learned_no_provenance"])].copy()
ab.to_csv(OUT / "ablations" / "standing_ablation_table.csv", index=False)

# Representative failures: deterministic selection, first 5 from each available split/domain combination.
rep = errors.sort_values(["split", "domain", "case_id"]).groupby(["split", "domain"], dropna=False).head(5)
rep.to_csv(OUT / "failure_examples" / "representative_hybrid_failures.csv", index=False)

# Frozen config summary for review.
config = {
    "canonical_source_of_truth": "results/provenancebench_method_summary.csv",
    "bootstrap": {"repetitions": 5000, "seed": 11},
    "learned_router_seeds": list(range(10)),
    "splits": {row.split: int(row.n) for row in method[method.method == "hybrid_plp"].itertuples()},
    "post_training_mixture_seed": 17,
    "claim_boundary": "controlled routing benchmark; no completed external-model generation or independent human-label claim",
}
(OUT / "configs" / "canonical_eval_config.json").write_text(json.dumps(config, indent=2) + "\n")

# Experiment registry, with only claims backed by canonical files/docs.
experiments = [
    {
        "experiment_id": "EXP-001", "name": "Naive personalization baseline", "status": "rejected",
        "hypothesis": "Using all personally relevant context should improve personalization without badly damaging epistemic behavior.",
        "setup": "Evaluate the naive policy on the frozen ProvenanceBench splits.",
        "result": "Domain-OOD exact=0.368, evidence uptake=1.000, unsupported leakage=0.857 (N=912).",
        "interpretation": "Personal relevance was being treated too much like evidentiary authority.",
        "next_decision": "Keep as a lower-bound baseline; separate relevance from evidence standing."
    },
    {
        "experiment_id": "EXP-002", "name": "Fixed firewall", "status": "rejected",
        "hypothesis": "Blocking personal context from the evidence channel should prevent contamination while remaining useful.",
        "setup": "Evaluate a fixed firewall on the same frozen splits.",
        "result": "Domain-OOD exact=0.526, leakage=0.000, evidence uptake=0.000 (N=912).",
        "interpretation": "Leakage was replaced by evidence starvation.",
        "next_decision": "Retain only as a diagnostic baseline; allow task-conditioned legitimate evidence."
    },
    {
        "experiment_id": "EXP-003", "name": "Provenance-only rule", "status": "partial",
        "hypothesis": "Source provenance alone may be sufficient to decide evidentiary standing.",
        "setup": "Apply a narrow explicit provenance rule across frozen splits.",
        "result": "Domain-OOD exact=0.684, uptake=0.800, leakage=0.071; compositional exact=0.600.",
        "interpretation": "Provenance matters but does not encode task relevance, freshness, or confidence by itself.",
        "next_decision": "Learn task-conditioned standing rather than rely on source type alone."
    },
    {
        "experiment_id": "EXP-004", "name": "Learned three-head PLP router", "status": "revised",
        "hypothesis": "A learned router can infer three standing channels and generalize beyond the training distribution.",
        "setup": "Train three license heads with validation-only thresholds; evaluate ID/OOD/compositional/provenance splits.",
        "result": "ID exact=1.000, domain-OOD=0.842, compositional=0.400, OOD leakage=0.143.",
        "interpretation": "The learned decision surface fit ordinary held-out data but was brittle under structured shift.",
        "next_decision": "Add small auditable validity constraints instead of hiding the failure with more capacity."
    },
    {
        "experiment_id": "EXP-005", "name": "Hybrid validity gates", "status": "current",
        "hypothesis": "Narrow stale/low-confidence/irrelevance gates can reduce leakage without collapsing into a firewall.",
        "setup": "Apply three validity gates after the learned heads and rerun frozen splits.",
        "result": "Domain-OOD exact=0.947 [0.933,0.962], compositional=0.800 [0.771,0.828], OOD leakage=0.000, uptake=0.800.",
        "interpretation": "The repair improves structured-shift behavior but remains conservative.",
        "next_decision": "Treat evidence starvation as the dominant remaining failure."
    },
    {
        "experiment_id": "EXP-006", "name": "Matched provenance intervention", "status": "diagnostic",
        "hypothesis": "Changing only provenance should change the correct standing decision when provenance is causally relevant.",
        "setup": "Evaluate 400 matched pairs / 800 examples with all non-provenance fields and surface text fixed.",
        "result": "No-provenance exact=0.500; Learned/Hybrid=0.750; provenance-only=1.000.",
        "interpretation": "Provenance is causally necessary on the isolated test, but learned transfer is incomplete.",
        "next_decision": "Require this intervention in the canonical paper pipeline."
    },
    {
        "experiment_id": "EXP-007", "name": "Calibration under shift", "status": "diagnostic",
        "hypothesis": "If the evidence head generalizes, confidence should remain calibrated under shift.",
        "setup": "Measure evidence-head ECE on ID, domain-OOD, compositional, and provenance-intervention splits.",
        "result": "ECE: 0.011 ID, 0.157 domain-OOD, 0.486 compositional, 0.253 provenance intervention.",
        "interpretation": "Confidence degrades sharply under the same shifts that hurt standing decisions.",
        "next_decision": "Report calibration beside exact match."
    },
    {
        "experiment_id": "EXP-008", "name": "Multi-seed stability", "status": "diagnostic",
        "hypothesis": "The compositional failure may mainly reflect optimizer/initialization variance.",
        "setup": "Retrain/evaluate Learned and Hybrid PLP across seeds 0-9.",
        "result": "The same split-specific metrics repeated across all 10 seeds in the current linear-router setup.",
        "interpretation": "The dominant failure is structural in the representation/split, not a cherry-pickable seed.",
        "next_decision": "Improve interventions/data rather than search for a favorable seed."
    },
    {
        "experiment_id": "EXP-009", "name": "Conflicting-source authority subtest", "status": "separate",
        "hypothesis": "Authority selection among conflicting sources should be measured separately from standing classification.",
        "setup": "Evaluate an explicit source-authority ranking on controlled conflict groups.",
        "result": "The explicit ranking rule reaches 1.000 on the controlled in-domain and held-out conflict groups.",
        "interpretation": "This is a distinct specification-level subproblem and should not inflate the learned-router claim.",
        "next_decision": "Keep conflict ranking separate in the paper and code."
    },
    {
        "experiment_id": "EXP-010", "name": "Trial-level failure mining", "status": "diagnostic",
        "hypothesis": "Remaining Hybrid PLP failures will include both unsupported leakage and starvation.",
        "setup": "Run the frozen task/trial/grader evaluation over 2,600 trials and mine failed state verification.",
        "result": "392 licensing failures; all 392 are classified as evidence starvation in the current run.",
        "interpretation": "The hybrid method has become conservative rather than permissive.",
        "next_decision": "Target missed valid evidence in the next data intervention."
    },
    {
        "experiment_id": "EXP-011", "name": "Failure-driven correction mixture", "status": "prepared",
        "hypothesis": "Failure corrections should be balanced with already-correct anchors to reduce regression risk.",
        "setup": "Convert 392 starvation failures into corrections and sample 392 stability anchors.",
        "result": "784-example post-training seed: 392 corrections + 392 anchors.",
        "interpretation": "The eval-to-data loop is executable, but this is not evidence that post-training improved a model.",
        "next_decision": "Use the mixture in a future real-model intervention and rerun the frozen eval."
    },
    {
        "experiment_id": "EXP-012", "name": "Research-candidate gate", "status": "passed",
        "hypothesis": "The controlled router is mature enough for the next research stage without implying production readiness.",
        "setup": "Apply fixed thresholds to ID/OOD/compositional exact, leakage, uptake, and trial-weighted state score.",
        "result": "All controlled research-candidate checks pass; trial-weighted state score=0.9246.",
        "interpretation": "The controlled system is reproducible enough for external-model/human validation next.",
        "next_decision": "Freeze the controlled protocol; move the next scientific risk to real-model generation and human judgment."
    },
]
registry = pd.DataFrame(experiments)
registry.to_csv(OUT / "experiment_logs" / "experiment_registry.csv", index=False)

# Individual machine-readable experiment records link to the human journal.
for row in experiments:
    payload = dict(row)
    payload["human_log"] = "evidence/EXPERIMENT_JOURNAL.md"
    (OUT / "experiment_logs" / f"{row['experiment_id']}.json").write_text(json.dumps(payload, indent=2) + "\n")

# Plots: default Matplotlib colors/styles only.
ood = method[method.split == "ood_test"].copy()
order = ["naive", "firewall", "provenance_only", "learned_plp", "hybrid_plp", "oracle"]
ood["method"] = pd.Categorical(ood["method"], categories=order, ordered=True)
ood = ood.sort_values("method")
plt.figure(figsize=(8, 4.5))
plt.bar(ood["method"].astype(str), ood["exact_license_match"])
plt.ylabel("Domain-OOD exact license match")
plt.xlabel("Method")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(OUT / "plots" / "domain_ood_exact_by_method.png", dpi=160)
plt.close()

plt.figure(figsize=(7, 4.5))
plt.bar(strict["split"], strict["evidence_head_ece"])
plt.ylabel("Evidence-head ECE")
plt.xlabel("Split")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUT / "plots" / "calibration_ece_by_split.png", dpi=160)
plt.close()

hy = method[method.method == "hybrid_plp"].copy()
plt.figure(figsize=(7, 4.5))
plt.bar(hy["split"], hy["exact_license_match"])
plt.ylabel("Hybrid PLP exact license match")
plt.xlabel("Split")
plt.xticks(rotation=25, ha="right")
plt.tight_layout()
plt.savefig(OUT / "plots" / "hybrid_exact_across_splits.png", dpi=160)
plt.close()

# Minimal provenance manifest so evidence copies are traceable.
manifest = {
    "generated_by": "scripts/build_evidence_layer.py",
    "source_files": sorted(copy_map.keys()),
    "experiment_count": int(len(registry)),
    "rejected_or_revised_logged_experiments": int(registry.status.isin(["rejected", "revised"]).sum()),
    "failed_or_revised_research_ideas_documented": 6,
    "material_decisions_documented": 8,
    "unexpected_findings_documented": 5,
    "multiseed_rows": int(len(multiseed)),
    "representative_failure_rows": int(len(rep)),
}
(OUT / "EVIDENCE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
print(json.dumps(manifest, indent=2))


# Evidence provenance fields and immutable-source hash ledger.
provenance_meta = {
    "EXP-001": ("canonical benchmark result", "results/provenancebench_method_summary.csv", "python scripts/provenancebench_learned.py"),
    "EXP-002": ("canonical benchmark result", "results/provenancebench_method_summary.csv", "python scripts/provenancebench_learned.py"),
    "EXP-003": ("canonical benchmark result", "results/provenancebench_method_summary.csv", "python scripts/provenancebench_learned.py"),
    "EXP-004": ("canonical benchmark result", "results/provenancebench_method_summary.csv; results/provenancebench_predictions.csv", "python scripts/provenancebench_learned.py"),
    "EXP-005": ("canonical benchmark + bootstrap result", "results/provenancebench_method_summary.csv; results/provenancebench_strict_stats.csv", "python scripts/provenancebench_learned.py && python scripts/provenancebench_strict_stats.py"),
    "EXP-006": ("matched causal diagnostic", "datasets/provenance/provenance_intervention_test.csv; results/provenancebench_method_summary.csv", "python scripts/provenancebench_learned.py"),
    "EXP-007": ("calibration diagnostic", "results/provenancebench_calibration.csv; results/provenancebench_strict_stats.csv", "python scripts/provenancebench_strict_stats.py"),
    "EXP-008": ("multi-seed stability diagnostic", "results/provenancebench_multiseed.csv", "python scripts/provenancebench_multiseed.py"),
    "EXP-009": ("controlled conflict subtest", "results/provenancebench_method_summary.csv", "python scripts/provenancebench_learned.py"),
    "EXP-010": ("trial/state-verification run", "results/trial_eval_summary.json; results/trial_trajectories.jsonl; results/provenancebench_errors.csv", "python scripts/run_trial_eval.py"),
    "EXP-011": ("derived post-training data artifact", "datasets/post_training/failure_curriculum.jsonl; datasets/post_training/training_mixture.jsonl; results/training_mixture_manifest.json", "python scripts/build_failure_curriculum.py && python scripts/build_training_mixture.py"),
    "EXP-012": ("research-candidate gate", "results/launch_gate.json", "python scripts/launch_gate.py"),
}
registry = pd.read_csv(OUT / "experiment_logs" / "experiment_registry.csv")
registry["evidence_type"] = registry.experiment_id.map(lambda x: provenance_meta[x][0])
registry["source_artifacts"] = registry.experiment_id.map(lambda x: provenance_meta[x][1])
registry["reproduction_command"] = registry.experiment_id.map(lambda x: provenance_meta[x][2])
registry["journal_provenance"] = "retrospective reconstruction from frozen outputs"
registry.to_csv(OUT / "experiment_logs" / "experiment_registry.csv", index=False)
for row in registry.to_dict(orient="records"):
    rec = OUT / "experiment_logs" / f"{row['experiment_id']}.json"
    payload = json.loads(rec.read_text())
    for key in ["evidence_type","source_artifacts","reproduction_command","journal_provenance"]:
        payload[key] = row[key]
    rec.write_text(json.dumps(payload, indent=2) + "\n")

import hashlib
hash_rows=[]
for item in sorted(set(sum(([x.strip() for x in v.split(';')] for v in registry.source_artifacts), []))):
    src=ROOT/item
    if src.exists(): hash_rows.append({"path":item,"sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"bytes":src.stat().st_size})
pd.DataFrame(hash_rows).to_csv(OUT / "EVIDENCE_HASH_LEDGER.csv", index=False)

# One real failure lineage: frozen benchmark -> trajectory -> mined correction -> training mixture.
case_id="PI-0000-1"
bench=pd.read_csv(ROOT / "datasets/provenance/provenance_intervention_test.csv")
benchmark_row=bench[bench.case_id==case_id].iloc[0].to_dict()
trial=None
for line in (ROOT / "results/trial_trajectories.jsonl").read_text().splitlines():
    x=json.loads(line)
    if x.get("task_id")==case_id: trial=x; break
correction=None
for line in (ROOT / "datasets/post_training/failure_curriculum.jsonl").read_text().splitlines():
    x=json.loads(line)
    if x.get("source_case_id")==case_id: correction=x; break
mix_line=None; mix_rec=None
for i,line in enumerate((ROOT / "datasets/post_training/training_mixture.jsonl").read_text().splitlines(),1):
    x=json.loads(line)
    if x.get("source_case_id")==case_id and x.get("mixture_role")=="failure_correction": mix_line=i; mix_rec=x; break
trace={"case_id":case_id,"benchmark_row":benchmark_row,"trial":trial,"failure_curriculum_record":correction,"training_mixture_line":mix_line,"training_mixture_record":mix_rec,"claim_boundary":"This trace shows routing failure -> mined correction data. It does not claim a completed model-training improvement."}
(OUT / "qualitative_cases" / f"{case_id}_failure_trace.json").write_text(json.dumps(trace, indent=2, default=str)+"\n")
