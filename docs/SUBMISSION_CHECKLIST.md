# Submission / External-Review Checklist

Before presenting this as an empirical model-behavior paper rather than a research systems artifact:

- [ ] Evaluate at least three real models on the frozen test protocol.
- [ ] Use multiple decoding seeds/configurations where stochasticity matters.
- [ ] Add an independently authored transfer set not used during method development.
- [ ] Collect blinded human labels on a preregistered stratified sample.
- [ ] Report inter-rater agreement and automatic-grader calibration.
- [ ] Compare CGSP-style training/steering against naive personalization, generic prompting, strong system-prompt guardrails, and a relevant personalization baseline.
- [ ] Run learned-method ablations for personalization loss and invariance loss.
- [ ] Report model capability regression on non-personalized controls.
- [ ] Validate translations with native speakers before multilingual claims.
- [ ] Freeze all final prompts, model versions, sampling parameters, and evaluation hashes before the main run.
- [ ] Report cost/latency and failure examples, not only aggregate scores.
- [ ] Keep proxy-testbed results separated from real-model results in every table and abstract.
