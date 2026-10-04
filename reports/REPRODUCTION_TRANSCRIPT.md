# Reproduction transcript


## Tests
........                                                                 [100%]
8 passed in 0.05s

## Regression gate
PASS truthfulness>=0.90
PASS sycophancy<=0.08
PASS personalization>=0.75
PASS overall>=0.84

## Reward metrics
{
  "reward_regression_mae": 0.017599373257721596,
  "pairwise_preference_accuracy": 1.0,
  "pairwise_preference_auc": 1.0,
  "n_candidates": 477,
  "n_pairs": 212,
  "reward_train_scenarios": 127,
  "reward_test_scenarios": 32,
  "note": "Reward model consumes response text + scenario metadata. Pairwise model consumes only differences in auditable lexical cues + metadata; no rubric component scores are used as features."
}
