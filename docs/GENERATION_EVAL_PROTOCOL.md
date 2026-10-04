# Generation Evaluation Protocol

The licensing benchmark and the generation experiment answer different questions and are kept separate.

1. **Routing:** infer presentation, personalization, and evidence licenses from the user-context signal.
2. **Generation compliance:** given a frozen license vector, produce an answer that uses only the permitted influence.
3. **Scoring:** blind human raters judge unsupported influence, evidence starvation, personalization utility, factuality, and confidence calibration.

`python scripts/evaluate_generation_adapter.py path/to/adapter.py` writes model outputs without provider-specific code or credentials in the repository.

## Required model experiment

Use at least one open-weight model and, when access is available, multiple frontier APIs. Evaluate the same frozen cases under:

- full context, no licensing;
- prompt-only provenance instruction;
- provenance-only heuristic;
- learned PLP;
- Hybrid PLP;
- oracle licenses.

The oracle condition separates **routing error** from **generation-compliance error**. A model can fail even with a perfect router if it ignores the license during generation.

No generation result should be reported as completed until the corresponding output JSONL and blinded annotations are present.
