# Real Model Adapter Contract

The local baselines are intentionally dependency-free. To evaluate a real checkpoint or API, implement `ModelAdapter.generate(scenario) -> PolicyOutput` and return only the model response text. The evaluator never accepts model-supplied behavioral scores.

## Required experimental discipline

1. Freeze `datasets/behaviorbench/test.jsonl` before model evaluation.
2. Keep system prompts/configs versioned in `configs/`.
3. Record model identifier, decoding settings, date, seed, latency, and cost per run.
4. Never tune on the frozen test split.
5. Calibrate automatic graders against blinded human labels before publishing model claims.
6. Report all failed runs and exclusions.

A provider-specific adapter can be added without changing benchmark schema or analysis scripts.
