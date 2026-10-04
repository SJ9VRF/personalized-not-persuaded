> **Supporting predecessor artifact.** The current paper result is the learned ProvenanceBench study in `reports/PROVENANCEBENCH_EXECUTABLE.md`; this file documents an earlier controlled reference design.

# Contract-Guided Selective Personalization (CGSP)

## Motivation
Personalization context contains heterogeneous information. Communication style, response preferences, goals, and constraints can legitimately alter presentation or action selection. A user's beliefs, confidence, status cues, or remembered requests for certainty are different: absent new task evidence, they should not change factual stance or uncertainty.

CGSP makes that distinction explicit as an **adaptation contract**.

## Factorization
Let user context be `u = (u_A, u_P)` where:

- `u_A` — adaptation-allowed channels: style, explicit response preferences, goals, constraints.
- `u_P` — protected channels: user beliefs and memories that are not themselves external-world evidence.

For a response model `f`, the target is:

`maximize Utility(f(x, u_A), u_A)`

subject to a protected counterfactual constraint:

`E(f(x, u_A, u_P)) ≈ E(f(x, u_A, u'_P))`

for matched protected interventions `u_P → u'_P`, where `E(.)` extracts epistemic behavior (stance, calibration, grounding, unsupported agreement).

A training-time relaxation is:

`L = L_task + α L_personalization + λ L_epistemic_invariance`

with

`L_epistemic_invariance = d(E(y_P3), E(y_P4)) + d(E(y_P4), E(y_P5))`.

## Local executable method
The repository's CGSP policy is intentionally simple and auditable. It constructs the response only from `communication_style`, `preferences`, `goals`, and `constraints`; `beliefs` and `memories` are excluded from the generation path. This gives the benchmark a hard non-interference baseline and makes the proposed contract testable without a proprietary model.

This local implementation is **not** claimed as a learned frontier-model algorithm. The intended next experiment is to train or steer a real model with the same contract loss and evaluate it on the frozen paired benchmark.

## Why it differs from nearby 2026 work
- Continual-personalization methods such as SPRInG selectively decide *when to update* under preference drift; CGSP asks *which user-context channels are permitted to affect which response dimensions*.
- Vision-language selective adaptation decides whether a test sample should adapt; CGSP concerns personalization-specific causal non-interference between user context and epistemic behavior.
- Sycophancy-control work controls agreement under pressure; CGSP couples that concern to useful personalization so a system cannot “solve” sycophancy by simply becoming generic.

## Primary metrics
- **APG — Allowed Personalization Gain**
- **PED — Protected Epistemic Drift**
- **PEI — Protected Epistemic Invariance = 1 − PED**
- **CCI — Cross-Channel Interference**
- **Contract Score = APG − PED**
- **Contract Pass Rate**

## Falsification criteria
CGSP fails if any of the following occur on matched contracts:
1. Allowed channels do not produce meaningful personalization.
2. Belief-only or memory-only interventions change epistemic behavior without new evidence.
3. Improvements appear only under the automatic rubric and disappear under blinded human judgments.
4. The method degrades task capability or factual accuracy on non-personalized controls.
