# Reproducibility

## One-command pipeline

```bash
python scripts/run_all.py
```

The pipeline regenerates BehaviorBench, validates all scenarios, runs held-out baseline evaluation, executes long-horizon drift simulation, trains reward/preference models, builds the dashboard, and writes a research report.

## Scientific boundary
The default policies and evaluator are local proxies. They are designed to test infrastructure and hypotheses without external APIs. Do not present their scores as evidence about proprietary or frontier models. Replace the policy adapter and calibrate graders against human labels before making model-performance claims.

## Data leakage control
Train/validation/test assignment is based on semantic template clusters rather than random row-level splitting. Language variants of the same content share a split because the split key excludes language.
