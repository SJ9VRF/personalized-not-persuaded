# Contract Statistical Analysis

Bootstrap confidence intervals use 5,000 resamples over the 820 exact matched contracts. Pairwise comparisons preserve contract identity.

## 95% bootstrap confidence intervals

| Policy | Metric | Mean | 95% CI | N |
|---|---|---:|---:|---:|
| behavior_trained_proxy | allowed_personalization_gain | 0.3520 | [0.3439, 0.3596] | 820 |
| behavior_trained_proxy | protected_epistemic_drift | 0.0000 | [0.0000, 0.0000] | 820 |
| behavior_trained_proxy | contract_score | 0.3520 | [0.3439, 0.3596] | 820 |
| behavior_trained_proxy | contract_pass | 0.9024 | [0.8805, 0.9220] | 820 |
| cgsp | allowed_personalization_gain | 0.3627 | [0.3569, 0.3685] | 820 |
| cgsp | protected_epistemic_drift | 0.0000 | [0.0000, 0.0000] | 820 |
| cgsp | contract_score | 0.3627 | [0.3569, 0.3681] | 820 |
| cgsp | contract_pass | 1.0000 | [1.0000, 1.0000] | 820 |
| generic | allowed_personalization_gain | -0.2076 | [-0.2120, -0.2028] | 820 |
| generic | protected_epistemic_drift | 0.0000 | [0.0000, 0.0000] | 820 |
| generic | contract_score | -0.2076 | [-0.2120, -0.2028] | 820 |
| generic | contract_pass | 0.0000 | [0.0000, 0.0000] | 820 |
| naive_personalized | allowed_personalization_gain | 0.3520 | [0.3439, 0.3596] | 820 |
| naive_personalized | protected_epistemic_drift | 0.0634 | [0.0547, 0.0728] | 820 |
| naive_personalized | contract_score | 0.2885 | [0.2777, 0.2996] | 820 |
| naive_personalized | contract_pass | 0.7073 | [0.6756, 0.7390] | 820 |

## Paired CGSP effects

| Comparison | Metric | Mean Δ | 95% CI | Paired d |
|---|---|---:|---:|---:|
| cgsp - behavior_trained_proxy | allowed_personalization_gain | 0.0107 | [0.0086, 0.0130] | 0.329 |
| cgsp - behavior_trained_proxy | protected_epistemic_drift | 0.0000 | [0.0000, 0.0000] | ∞ |
| cgsp - behavior_trained_proxy | contract_score | 0.0107 | [0.0086, 0.0130] | 0.329 |
| cgsp - behavior_trained_proxy | contract_pass | 0.0976 | [0.0780, 0.1183] | 0.329 |
| cgsp - generic | allowed_personalization_gain | 0.5702 | [0.5597, 0.5808] | 3.766 |
| cgsp - generic | protected_epistemic_drift | 0.0000 | [0.0000, 0.0000] | ∞ |
| cgsp - generic | contract_score | 0.5702 | [0.5597, 0.5802] | 3.766 |
| cgsp - generic | contract_pass | 1.0000 | [1.0000, 1.0000] | ∞ |
| cgsp - naive_personalized | allowed_personalization_gain | 0.0107 | [0.0086, 0.0130] | 0.329 |
| cgsp - naive_personalized | protected_epistemic_drift | -0.0634 | [-0.0723, -0.0544] | -0.484 |
| cgsp - naive_personalized | contract_score | 0.0741 | [0.0654, 0.0835] | 0.570 |
| cgsp - naive_personalized | contract_pass | 0.2927 | [0.2634, 0.3232] | 0.643 |

These intervals characterize the deterministic proxy fixture under contract resampling; they do not substitute for model-seed variance or human-rater uncertainty.
