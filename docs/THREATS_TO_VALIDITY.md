# Threats to Validity

## Construct validity
The bundled scorer is intentionally interpretable but coarse. It detects surface cues for unsupported agreement, uncertainty, grounding, personalization, emotional fit, and personality stability. These proxies do not fully capture human judgments of epistemic quality. In particular, the personalization score saturates once observable adaptation cues are present and is less sensitive to richer goal/constraint adaptation.

## Internal validity
The local policies and scorer are deterministic. This makes causal counterfactual comparisons auditable, but it also means the bundled confidence intervals reflect resampling over contracts rather than stochastic model-seed variance. Real-model experiments should use multiple decoding seeds where applicable and keep prompt/model configuration fixed across matched counterfactuals.

## External validity
The included results do not establish behavior on frontier models, arbitrary domains, cultures, or languages. The four language variants test pipeline coverage; the local policies are not genuine multilingual models. Real multilingual claims require native-language review and model execution.

## Benchmark overfitting
CGSP is designed against the explicit contract structure. The frozen-protocol hashes and held-out split reduce silent post-hoc benchmark edits, but a real scientific claim requires transfer to independently authored scenarios and human labels.

## Grader dependence
Proxy policy ordering may depend on hand-engineered cues. The repository therefore separates the frozen automatic rubric from the recommended blinded human evaluation. A publishable extension should report automatic/human agreement, false positives, false negatives, and grader instability.

## Human-study validity
No human-study result is bundled. Any future human evaluation should randomize response order, blind model identity, retain disagreement distributions, and document recruitment/exclusion criteria before analysis.
