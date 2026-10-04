# 3-Minute Demo Script

Open `dashboard/index.html`.

1. **20 sec — Thesis:** “This lab tests whether personalization can increase without increasing sycophancy.”
2. **35 sec — Benchmark:** point to scenario count, P0–P5 profile richness, and the held-out split.
3. **45 sec — Failure example:** open a high-richness factual-disagreement row from `results/benchmark_results.csv`; contrast naive personalized vs behavior-aware response.
4. **35 sec — Tradeoffs:** show truthfulness, sycophancy, calibration, and personalization side-by-side. Note sycophancy is lower-is-better.
5. **25 sec — Long horizon:** show drift chart from 1 to 200 turns.
6. **30 sec — Reward model:** point to reward MAE and pairwise preference accuracy; explain the model is trained locally over multidimensional behavior features.
7. **30 sec — Scientific honesty:** state proxy policies are executable fixtures, then show `ModelAdapter` and explain that real checkpoints can replace them without changing the evaluation contract.
