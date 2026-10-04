# Personalized, Not Persuaded

**Aura Yavary**

### Learning When Personal Context Counts as Evidence

## Thesis
A personal AI should adapt to the user without silently promoting every remembered belief, preference, or inferred state into evidence.

## Research gap
Personalization systems usually ask whether context is relevant or helpful. That is not enough. The same signal can be useful for tone, relevant for a personal decision, and still illegitimate as evidence for a factual claim.

## Method
**Provenance-Licensed Personalization (PLP)** predicts three permissions per signal:

- presentation;
- personalization;
- evidence.

A learned router predicts the permissions from signal text and structured context. **Hybrid PLP** adds narrow validity gates for stale, low-confidence, or task-irrelevant context.

## What the experiments show

The learned router fits ordinary held-out data but degrades under shift. Hybrid PLP improves domain-OOD exact match to **0.947** and compositional exact match to **0.800**, while eliminating measured OOD unsupported leakage. It does not fully recover licensed evidence, which is an explicit remaining failure rather than a hidden one.

A separate **400-pair provenance intervention** fixes task, scope, confidence, currentness, relevance, and wording. Only provenance changes. Removing provenance cues falls to **0.500** exact match; Learned/Hybrid PLP reach **0.750**. This demonstrates genuine source sensitivity while exposing incomplete transfer.

## Why this is useful
The project separates three questions that are often conflated:

1. Is context personally relevant?
2. Is it valid for the current task?
3. Is it actually evidence?

That distinction is directly relevant to persistent-memory agents and tool-using assistants, where retrieved context may be useful without being authoritative.

## What is implemented

- 4,800-example ProvenanceBench
- 800-example paired provenance intervention
- learned three-head router + Hybrid PLP
- naive / firewall / provenance-only / oracle baselines
- OOD + compositional evaluation
- calibration + item-bootstrap statistics + paired tests
- ten-seed stability check
- conflict-source subtest
- 552-item blinded human-eval packet and answer key
- generation adapter with oracle-license decomposition
- paper PDF/LaTeX, demo, technical report, benchmark card, tests and audit

## Scientific boundary
The current result is a controlled routing/benchmark result. Real-model generation and independent human validation are specified as follow-up experiments.


## Research-engineering loop
The benchmark is wired into an executable improvement loop: trial trajectories and state-verification graders identify failures; failures become targeted correction examples; correct cases become stability anchors; and a controlled research gate decides whether a future intervention is worth advancing. The current snapshot produces 392 evidence-starvation corrections and 392 stability anchors. No frontier-model post-training run is claimed.
