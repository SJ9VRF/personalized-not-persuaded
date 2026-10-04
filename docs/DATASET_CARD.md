# BehaviorBench v1 — Dataset Card

## Purpose
BehaviorBench is a controlled evaluation dataset for studying whether personalization changes *delivery* while preserving epistemic independence. It targets excessive agreement, flattery, false validation, confidence inflation, user-belief leakage, preference overfitting, emotional over/under-response, and personality instability.

## Composition
The default build contains 1,200 deterministic scenarios spanning 10 scenario families, six user-profile richness conditions (P0–P5), four language-tag stress conditions, and five pressure modes. The 20 hand-authored canonical seeds remain separate from generated benchmark data.

## Splits
Train/validation/test assignment is deterministic. Related language variants share the same semantic split key to reduce cross-split leakage.

## Provenance
Generated records use authored templates and deterministic transformations. No scraped personal conversations are included.

## Intended use
- behavioral evaluation
- grader development
- preference/reward-model prototyping
- regression testing
- long-horizon research scaffolding

## Not intended for
- claiming representative human behavior
- clinical or psychological assessment
- demographic inference
- claims about frontier-model quality without actually running those models

## Known limitation
The default multilingual condition is a language-tag perturbation rather than a linguistically complete translation corpus. A real multilingual study should replace these variants with human-checked translations and native-speaker labels.
