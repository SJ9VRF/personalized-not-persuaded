# Experiment Report

## Scope and interpretation

This report is generated from a fully local, reproducible proxy experiment. It demonstrates the benchmark/evaluation/reward-modeling machinery. It does **not** claim human-study results or performance of frontier language models.

## Held-out benchmark

### generic
- Overall: 0.7819 (95% bootstrap CI 0.7749–0.7893)
- Personalization: 0.3796
- Truthfulness: 0.9168
- Sycophancy: 0.0400 (lower is better)
- Calibration: 0.9041

### naive_personalized
- Overall: 0.8035 (95% bootstrap CI 0.7822–0.8238)
- Personalization: 0.8008
- Truthfulness: 0.7855
- Sycophancy: 0.2171 (lower is better)
- Calibration: 0.8543

### behavior_trained_proxy
- Overall: 0.8799 (95% bootstrap CI 0.8753–0.8844)
- Personalization: 0.8250
- Truthfulness: 0.9168
- Sycophancy: 0.0400 (lower is better)
- Calibration: 0.9041

### cgsp
- Overall: 0.8791 (95% bootstrap CI 0.8744–0.8837)
- Personalization: 0.8215
- Truthfulness: 0.9168
- Sycophancy: 0.0400 (lower is better)
- Calibration: 0.9041

## Reward-model diagnostics
- Reward regression MAE: 0.0156
- Pairwise preference accuracy: 1.0000
- Pairwise preference ROC-AUC: 1.0000
- Candidate responses: 636
- Preference pairs: 184

## Next scientific upgrade
Swap the proxy policies for real model adapters; collect blinded human labels on the frozen test split; calibrate automatic graders; then re-run the exact same pipeline.