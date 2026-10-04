# Research Claims: What This Release Can and Cannot Support

## Supported by the bundled executable evidence
- The counterfactual-contract benchmark is exactly matched over task, language, and pressure while profile state changes.
- The local CGSP implementation structurally excludes protected beliefs and non-evidentiary memories from its response-construction path.
- In the deterministic proxy fixture, removing protected gating causes measurable epistemic drift, while removing allowed adaptation eliminates useful personalization.
- The complete benchmark/evaluation/reward-modeling pipeline is reproducible locally and tied to frozen protocol hashes.

## Hypotheses, not yet empirical frontier-model claims
- A learned CGSP-style regularizer will improve personalization/epistemic tradeoffs in frontier or open-weight language models.
- Counterfactual contract metrics will correlate strongly with blinded human judgments.
- The same factorization will transfer robustly across languages, domains, tool use, and long-horizon stateful interaction.

## Claims this release must not make
- “State of the art on GPT/Claude/Gemini.”
- “Human users prefer CGSP.”
- “CGSP eliminates sycophancy.”
- “The benchmark proves multilingual consistency.”
- “The reward model predicts real human preferences.”

The intended scientific upgrade is to keep the frozen benchmark fixed, evaluate real models, collect blinded human labels, and then test a learned contract regularizer against strong prompting and personalization baselines.
