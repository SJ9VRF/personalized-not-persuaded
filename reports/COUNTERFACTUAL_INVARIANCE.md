# Counterfactual Epistemic Invariance

This report evaluates rich-profile conditions (P4/P5) against matched P0 scenarios with the same template cluster, pressure condition, language, and policy.

The new metrics are designed to reward **useful adaptation without epistemic drift**.

## Proxy diagnostic result

| Policy | Personalization gain | Epistemic drift ↓ | CEI ↑ | Selective adaptation ↑ |
|---|---:|---:|---:|---:|
| Generic | -0.1314 | 0.0000 | 1.0000 | -0.1314 |
| Naive personalized | +0.2229 | 0.2619 | 0.7381 | -0.0390 |
| Behavior-aware proxy | +0.2229 | 0.0000 | 1.0000 | +0.2229 |

These are controlled proxy diagnostics, not frontier-model claims. They demonstrate that the metric distinguishes three qualitatively different behaviors: refusing to personalize, personalizing by epistemically drifting, and personalizing selectively.
