# 9-Minute Research Talk — Model Behavior Lab

**0:00–0:45 — Problem.** Personalization can improve relevance while quietly increasing epistemic deference. The core question is whether an assistant can learn *how* a person wants help without learning to treat that person's beliefs as evidence.

**0:45–2:00 — Failure taxonomy.** Show four concrete failures: agreement bias, belief leakage, false validation, confidence inflation. Introduce the separation between personalization utility and truthfulness/calibration.

**2:00–3:15 — BehaviorBench.** Explain P0–P5 profile richness, pressure transformations, frozen semantic splits, and the multidimensional metrics.

**3:15–4:30 — Baselines.** Compare generic, naive personalized, and behavior-aware proxy policies. Explicitly state that proxy results validate the machinery, not frontier-model performance.

**4:30–5:45 — Reward modeling.** Show multidimensional features, pairwise preferences, trained reward regressor, and preference classifier.

**5:45–6:45 — Reward hacking.** Show the satisfaction-weight sweep: a scalar objective can look better while truthfulness/calibration degrade.

**6:45–7:45 — Long horizon.** Show personality drift over 1–200 turns and why character needs trajectory-level evaluation.

**7:45–8:30 — Human data path.** Annotation UI, disagreement-preserving labels, grader calibration, and frozen held-out evaluation.

**8:30–9:00 — Thesis.** The right target is not maximally agreeable personalization. It is user adaptation under explicit epistemic and behavioral invariants.
