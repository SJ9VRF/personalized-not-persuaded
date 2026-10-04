# Reward / Metric Ablations

These are deterministic re-weighting ablations over the frozen proxy-evaluation outputs. They test whether the headline comparison depends on a single metric. They are **not** retraining ablations.

| ablation                       |   behavior_trained_proxy |   cgsp |   generic |   naive_personalized |
|:-------------------------------|-------------------------:|-------:|----------:|---------------------:|
| drop_calibration               |                   0.8762 | 0.8754 |    0.7636 |               0.7959 |
| drop_emotional_appropriateness |                   0.8943 | 0.8934 |    0.7817 |               0.8079 |
| drop_non_sycophancy            |                   0.8623 | 0.8613 |    0.7428 |               0.8081 |
| drop_personality_consistency   |                   0.8818 | 0.881  |    0.773  |               0.797  |
| drop_personalization           |                   0.8953 | 0.8953 |    0.8953 |               0.8043 |
| drop_truthfulness              |                   0.8682 | 0.8672 |    0.7393 |               0.8092 |
| full                           |                   0.8799 | 0.8791 |    0.7819 |               0.8035 |
