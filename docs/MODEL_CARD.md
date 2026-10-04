# Method and Evaluation Components

This repository contains two different kinds of executable components, and they should not be conflated.

## Learned routing method

The paper's current method is implemented in `behavior_lab/methods/learned_plp.py`.

- **Learned PLP** predicts three task-conditioned licenses for each personal-context signal: presentation, personalization, and evidence.
- **Hybrid PLP** applies narrow validity gates after the learned prediction to block stale, low-confidence, or task-irrelevant context.
- Thresholds are selected on validation data; the reported ID, domain-OOD, compositional, calibration, and paired-provenance results come from this learned/hybrid pipeline.

These are the components associated with the main paper claim.

## Offline fixtures and diagnostic baselines

The repository also keeps small deterministic policies used for regression tests and for earlier controlled behavior experiments:

- `generic`
- `naive_personalized`
- `behavior_trained_proxy`

They are **not language models** and their scores are not evidence about production assistants. They remain in the repository because they make legacy regression tests, failure-analysis utilities, and comparison tooling executable without an external model provider.

## Generation boundary

Routing quality is evaluated separately from generation quality. The provider-neutral generation interface in `behavior_lab/generation/` and `scripts/evaluate_generation_adapter.py` is the boundary for a real checkpoint or API-backed generator.

The current release reports controlled routing results. It does not report frontier-model generation or independent human judgments.
