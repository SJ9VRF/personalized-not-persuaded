# ProvenanceBench — Benchmark Card

## Research question
Can a personalized agent distinguish context that is useful for style or preference adaptation from context that is legitimately evidentiary for the current task?

## Structure
The benchmark contains controlled, domain-OOD, compositional, and conflicting-evidence cases. Each signal is labeled with three independent permissions: presentation, personalization, and evidence.

## Intended use
- controlled identification of provenance-sensitive routing failures;
- ablation of provenance, freshness, relevance, and confidence;
- pre-generation routing evaluation;
- construction of blinded human-evaluation packets.

## Not intended as
- evidence of frontier-model generation quality;
- a substitute for human validation;
- a universal ontology of evidence authority;
- a safety certification.

## Leakage risks
Surface wording can reveal source type. The strict no-provenance ablation removes both structured provenance and source-identifying text before fitting. Results should report this stricter ablation rather than claiming provenance dependence from a metadata-only removal.

## Split discipline
Thresholds are selected on validation only. Test, domain-OOD and compositional splits are not used for threshold selection. Conflict cases are evaluated separately because authority selection is a different subproblem from binary licensing.
