# Reward / Training Signal Specification

PLP exposes three supervised behavior channels rather than a single scalar “personalization quality” reward.

For a prediction \(\hat L=(\hat L_p,\hat L_u,\hat L_e)\) and frozen target \(L\), the default controlled training signal weights evidence mistakes more heavily than presentation mistakes:

- presentation mismatch: weight 1
- personalization mismatch: weight 1
- evidence mismatch: weight 2
- unsupported evidence leakage receives an additional safety penalty in curriculum priority

This weighting is used for **failure prioritization and state-verification diagnostics**, not claimed as an optimal RL reward. A real post-training experiment should ablate these weights and evaluate Pareto tradeoffs between evidence uptake and unsupported influence.

A key anti-reward-hacking constraint is to preserve raw metrics separately. A scalar combined score must never replace reporting of evidence uptake and leakage because a model can improve one while degrading the other.
