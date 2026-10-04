# Artifact Index

**Personalized, Not Persuaded — Aura Yavary**

## Start here
- `README.md`
- `RESULTS_CARD.md`
- `PORTFOLIO_BRIEF.md`
- `REVIEWER_GUIDE.md`
- `index.html`

## Paper
- `artifacts/personalized-not-persuaded-paper.pdf`
- `paper/main.tex`
- `paper/PAPER_DRAFT.md`

## Method
- `behavior_lab/methods/learned_plp.py`
- `scripts/run_provenancebench_learned.py`
- `scripts/provenancebench_stats_strict.py`
- `scripts/provenancebench_multiseed.py`

## Benchmark
- `datasets/provenance/provenancebench.csv`
- `datasets/provenance/provenance_intervention_test.csv`
- `docs/BENCHMARK_CARD.md`
- `reports/PROVENANCEBENCH_EXECUTABLE.md`
- `reports/PROVENANCEBENCH_STRICT_STATS.md`
- `reports/PROVENANCEBENCH_MULTISEED.md`

## Human validation
- `datasets/human_eval/blinded_license_packet.csv`
- `datasets/human_eval/heldout_answer_key.csv`
- `docs/HUMAN_EVAL_PROTOCOL.md`
- `scripts/aggregate_human_eval.py`

## Generation evaluation
- `docs/GENERATION_EVAL_PROTOCOL.md`
- `scripts/evaluate_generation_adapter.py`
- `docs/REAL_MODEL_ADAPTER.md`

## Analysis outputs
- `results/provenancebench_method_summary.csv`
- `results/provenancebench_predictions.csv`
- `results/provenancebench_calibration.csv`
- `results/provenancebench_errors.csv`
- `results/provenancebench_strict_stats.csv`
- `results/provenancebench_multiseed.csv`

## Broader project context
- `datasets/behaviorbench/`
- `datasets/contracts/`
- `reports/FAILURE_ATLAS.md`
- `docs/DESIGN_DECISIONS.md`
- `docs/NOVELTY_AND_SOTA.md`

## Presentation
- `index.html` — flagship 14-section hiring-manager project page with 60-second summary.
- `site/index.html` — standalone mirror.
- `site/demo.html` — recorded frozen eval trials + separate contract explorer.
- `results/homepage_trial_examples.json` — exact recorded demo examples.
- `results/homepage_runtime_summary.json` — measured router-only success/recovery/latency/cost summary used by the homepage.
- `scripts/build_homepage_assets.py` — regenerates homepage evidence assets.
- `media/personalized-not-persuaded-walkthrough.mp4`
- `docs/HOMEPAGE_CHECKLIST.md` — maps all 14 required homepage sections.
- `docs/PLP_TECHNICAL_REPORT.md`
- `docs/BLOG_POST.md`

## Canonical reproduction
- `Makefile` — `make paper` is the canonical current-paper pipeline.
- `scripts/run_paper_pipeline.py` — one-command evidence regeneration and audits.
- `QUICKSTART.md` — minimal review/reproduction path.

## Reproducibility
- `requirements.txt`
- `pyproject.toml`
- `tests/`
- `scripts/submission_audit.py`
- `scripts/claim_audit.py`
- `scripts/result_consistency_audit.py`
- `scripts/public_surface_audit.py`
- `.github/workflows/ci.yml`

## Claim provenance

- `docs/CLAIM_LEDGER.md` — machine-generated mapping from headline quantitative claims to result artifacts and producer scripts.
- `scripts/claim_audit.py` — fails when core paper claims drift from frozen outputs.

## Frontier-lab research loop

- `docs/FRONTIER_LAB_READINESS.md` — eval, debugging, post-training, and research-ownership map.
- `docs/EVAL_TO_TRAINING_LOOP.md` — failure-to-data loop.
- `docs/REWARD_SIGNAL_SPEC.md` — channel-level training/reward signal specification.
- `docs/LAUNCH_GATES.md` — controlled research gate and required external production gates.
- `docs/RESEARCH_AGENDA.md` — next experiments and kill criteria.
- `results/trial_trajectories.jsonl` — task/trial/grader trajectories.
- `results/trial_eval_summary.json` — trajectory/state-verification summary.
- `datasets/post_training/failure_curriculum.jsonl` — targeted correction curriculum.
- `datasets/post_training/training_mixture.jsonl` — balanced correction + stability-anchor mixture.
- `results/failure_curriculum_summary.json` — failure-to-data counts.
- `results/training_mixture_manifest.json` — deterministic mixture manifest.
- `results/launch_gate.json` — executable research-candidate gate.

## Novelty / framing

- `docs/EVIDENTIARY_STANDING.md` — formalizes the central concept and its claim boundary.
- `docs/CLOSEST_WORK_MATRIX.md` — explicit nearest-work comparison designed to prevent novelty inflation.
- `docs/NOVELTY_AND_SOTA.md` — current novelty/SOTA audit and allowed claims.

## Archived research history

- `archive/legacy_reports/` — superseded pre-hardening reports retained for traceability; these are not canonical current results.

## Verification

`make verify` is the single release contract used locally and in CI. It runs tests, compilation, the canonical paper pipeline, and all audits.

## Evidence layer

- `evidence/index.html` — research-process landing page.
- `evidence/EXPERIMENT_JOURNAL.md` — 12 experiment records.
- `evidence/FAILED_EXPERIMENTS.md` — what did not work and why.
- `evidence/DECISION_LOG.md` — decisions → alternatives → evidence → trade-offs → outcomes.
- `evidence/REAL_EVAL_TABLES.md` — canonical tables with N/CI/seeds.
- `evidence/UNEXPECTED_FINDINGS.md` — observations that changed the research path.
- `evidence/GIT_HISTORY.md` — honest Git-history boundary.
- `artifacts/evidence/` — machine-readable experiment logs, eval runs, failure examples, plots, configs, qualitative cases, ablations, and Git bundle.
- `scripts/build_evidence_layer.py` — regenerates raw evidence snapshots from canonical outputs.
- `scripts/evidence_layer_audit.py` — release gate for the evidence contract.
