# Reviewer Guide

**Personalized, Not Persuaded — Aura Yavary**

## 60 seconds
Read `RESULTS_CARD.md` and the abstract of `paper/PAPER_DRAFT.md`.

The paper asks one question: **when is user context merely useful for personalization, and when is it licensed to count as evidence?**

## 5 minutes
1. `reports/PROVENANCEBENCH_EXECUTABLE.md` — regenerated learned/hybrid results.
2. `reports/PROVENANCEBENCH_STRICT_STATS.md` — bootstrap intervals, paired tests, calibration.
3. `docs/BENCHMARK_CARD.md` — intended use and leakage risks.
4. `docs/DESIGN_DECISIONS.md` — why the method changed after earlier failures.
5. `docs/THREATS_TO_VALIDITY.md` — external-validity boundaries.


## One-command reproduction

Run:

```bash
make paper
```

For a full local verification matching CI:

```bash
make verify
```

This is the canonical evidence path for the current paper. `make reproduce` runs the broader historical/proxy experiment suite and is intentionally not the recommended first review path.

## 15 minutes
Inspect:

- `behavior_lab/methods/learned_plp.py`
- `scripts/run_provenancebench_learned.py`
- `datasets/provenance/provenancebench.csv`
- `datasets/provenance/provenance_intervention_test.csv`
- `datasets/human_eval/blinded_license_packet.csv`
- `scripts/evaluate_generation_adapter.py`

## What the evidence says

- Learned PLP reaches 1.000 exact match on the ordinary held-out split but degrades under domain and compositional shift.
- Hybrid PLP improves robustness to 0.947 domain-OOD and 0.800 compositional exact match while eliminating measured OOD leakage; it still starves some licensed evidence.
- A paired provenance intervention holds all non-source variables fixed. Removing provenance cues gives 0.500 exact match; Learned/Hybrid PLP reach 0.750.
- The evidence-head calibration error rises sharply under shift.

## Current evidence boundary

- The reported numbers are routing results on controlled data, not end-to-end language-model generation results.
- Human agreement has not yet been collected.
- The oracle and provenance-only baselines isolate specific failure modes; they are not general solutions.
- The conflict-source ranker is a controlled reference for source ordering, not open-ended source reasoning.

## Best next experiment

Run one or more real generators with full context, predicted licenses, and oracle licenses, then score unsupported influence, evidence starvation, factuality, personalization utility, and confidence with blinded human raters. That experiment separates routing quality from generation compliance.

## If you are evaluating research-engineering depth

After the paper, inspect:

1. `results/trial_eval_summary.json` — task/trial/grader/state-verification view.
2. `datasets/post_training/failure_curriculum.jsonl` — failures converted into training targets.
3. `datasets/post_training/training_mixture.jsonl` — balanced correction + stability-anchor mixture.
4. `results/launch_gate.json` — executable research-candidate gate.
5. `docs/RESEARCH_AGENDA.md` — next experiments and kill criteria.

These are deliberately separate from the main paper claim. They show how the evaluation can drive a model-improvement loop without pretending that the external post-training run has already happened.

## If you want to see whether the project was actually iterated

Open `evidence/index.html`. It links the experiment journal, failed ideas, decision log, unexpected findings, canonical eval tables, raw trajectories/failures, and the real Git history that starts from the verified snapshot import. The Evidence Layer is deliberately separated from the polished 60-second homepage.
