# Eval-to-Training Loop

The project treats an evaluation as useful only if it can produce a concrete next intervention.

## Loop

1. **Run frozen trials.** Each signal-level task produces a trajectory and explicit state-verification grader results.
2. **Mine failures.** The licensing output is compared with the frozen contract on presentation, personalization, and evidence channels.
3. **Classify the failure.** Errors are labeled as leakage or starvation per channel; evidence failures receive higher priority.
4. **Build targeted data.** Failed cases become correction examples. Correct nearby cases become stability anchors so a new model is not trained only on errors.
5. **Train outside the benchmark test split.** The bundled mixture is a seed artifact; a real model run must preserve the frozen evaluation and exclude held-out test labels from optimization.
6. **Re-evaluate.** The same task/trial/grader stack is rerun and regression gates decide whether the intervention is a research candidate.

## Current executable artifact

`datasets/post_training/failure_curriculum.jsonl` is generated from Hybrid PLP errors. `datasets/post_training/training_mixture.jsonl` balances those corrections with stability anchors. The current controlled run contains **392 correction examples** and **392 anchors**.

All 392 current Hybrid PLP licensing failures are evidence-starvation failures. This matters: the method is conservative under the tested shifts. The next training intervention should therefore target **licensed evidence uptake without reintroducing unsupported influence leakage**.

## What this does not claim

The repository does not claim that frontier-model post-training, RL, DPO, or SFT has been run. It provides the failure-to-data machinery and a frozen evaluation surface required to run that experiment cleanly.
