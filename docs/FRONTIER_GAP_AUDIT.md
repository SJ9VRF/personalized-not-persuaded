# Frontier Gap Audit

## Bottom line
The project is **not** novel if framed as “personalization without sycophancy,” “causal personalization,” or “selective context use” in isolation. Those directions are already represented by strong adjacent work. The defensible research gap is narrower:

> **Counterfactual Personalization Contracts:** specify which response dimensions are allowed to adapt under a user-context intervention and which epistemic dimensions must remain invariant, then measure cross-channel interference on exactly paired interventions.

This is a *formulation + evaluation target* in the current local release, not a claim of state-of-the-art model performance.

## Closest work and boundary

| Work | What it already covers | What this project must not claim | Remaining gap targeted here |
|---|---|---|---|
| NextQuill (ICLR 2026) | causal preference effects; preference-bearing tokens | “first causal personalization” | explicit adaptation-vs-invariance behavioral contracts, especially protected epistemic channels |
| CAUSM (ICLR 2025) | causally motivated sycophancy mitigation in internal representations | “first causal sycophancy mitigation” | user-context factor contracts and exact paired profile interventions |
| Cautious Context Steering (2026) | token-level gating of whether context should affect generation | “first selective use of personalization context” | normative/evaluation contract specifying *which dimensions* may change and which must not |
| Kelley & Riedl (2026) | personalization vs affective alignment / epistemic independence across frontier models | “first personalization × epistemic independence study” | intervention-level contract metrics and cross-channel interference |
| Jain et al., CHI 2026 | real interaction context and memory can increase sycophancy | “first memory/context sycophancy study” | controlled factorized user-state interventions with protected-dimension invariance |
| Personalized RewardBench (2026) | personalized reward-model evaluation | “first personalized RM benchmark” | reward/eval targets that distinguish legitimate preference adaptation from epistemically protected behavior |
| SPRInG (2026) | selective continual adaptation under preference drift | “first selective personalization/adaptation” | selective **behavioral dimensions**, not just selective examples/updates |

## New unit of analysis: a personalization contract
A contract declares two sets for a user-context intervention `z`:

- `A(z)`: response dimensions that **should adapt** (style, format, explicit preferences, goals, constraints).
- `I(z)`: dimensions that **should remain invariant** unless new task evidence changes (factual stance, calibration, resistance to unsupported pressure).

A system violates the contract in two ways:

1. **Under-adaptation:** insufficient change on `A(z)`.
2. **Cross-channel interference:** change on `I(z)` caused only by user context.

This makes “personalization quality” a structured counterfactual property rather than a single preference score.

## Exact paired benchmark design
`datasets/contracts/counterfactual_personalization_contracts_v1.jsonl` fixes task, prompt, language, and pressure while changing only profile state across P0–P5. It contains 820 matched contracts × 6 profile interventions = 4,920 scenarios.

Profile ladder:
- P0: no user context
- P1: communication style
- P2: explicit response preferences
- P3: goals / constraints
- P4: user belief
- P5: memory of prior confidence request

P0→P3 are adaptation-permitted. P3→P4 and P4→P5 are protected epistemic interventions in the current benchmark.

## Metrics
- **APG — Allowed Personalization Gain**
- **PED — Protected Epistemic Drift**
- **PEI — Protected Epistemic Invariance = 1 − PED**
- **CCI — Cross-Channel Interference = PED / |APG|** (stabilized denominator)
- **Contract Score = APG − PED**
- **Contract Pass Rate** under explicit thresholds

## Novelty claim that is safe
A defensible statement is:

> We formulate personalized model behavior as a counterfactual contract over adaptation-sensitive and protected response dimensions, and provide an exactly paired testbed that separately measures useful adaptation and cross-channel epistemic interference.

Avoid “first” unless a future systematic review establishes it. Avoid “SOTA” until real models are run against comparable baselines with human-calibrated labels.

## Sources reviewed
- Zhao et al., **NextQuill: Causal Preference Modeling for Enhancing LLM Personalization**, ICLR 2026. https://openreview.net/forum?id=xYpVlKMFqv
- Li et al., **Causally Motivated Sycophancy Mitigation for Large Language Models**, ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/a52b0d191b619477cc798d544f4f0e4b-Abstract-Conference.html
- Kim et al., **Cautious Context Steering for Language Model Personalization**, arXiv:2608.05813.
- Kelley & Riedl, **Personalization Increases Affective Alignment but Has Role-Dependent Effects on Epistemic Independence in LLMs**, 2026.
- Jain et al., **Interaction Context Often Increases Sycophancy in LLMs**, CHI 2026. DOI:10.1145/3772318.3791915
- Ma et al., **Personalized RewardBench**, arXiv:2604.07343.
- Kim & Kim, **SPRInG: Continual LLM Personalization via Selective Parametric Adaptation and Retrieval-Interpolated Generation**, arXiv:2601.09974.
- Ibrahim et al., **Training language models to be warm can reduce accuracy and increase sycophancy**, Nature 2026.
