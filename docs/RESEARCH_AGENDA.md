# Research Agenda

## Thesis

Personalization should not be implemented as a scalar preference for “more user context.” A personal agent needs a learned policy for **which context may influence which behavioral channel**, with provenance and task validity treated as first-class variables.

## What the current work establishes

- a factorized presentation/personalization/evidence interface;
- a controlled benchmark with OOD, compositional, conflict, and matched provenance interventions;
- a learned-router failure under shift;
- a hybrid correction that removes unsupported evidence leakage in the controlled OOD setting while leaving a measurable evidence-starvation problem;
- an eval-to-training data loop that turns the remaining failures into targeted correction data.

## Highest-value next experiments

### 1. End-to-end model compliance
Run the provider-neutral adapter on several real model families under two conditions: predicted licenses and oracle licenses. This separates routing quality from generation obedience.

### 2. Human validity
Collect blinded labels for the frozen packet. Measure agreement, contract-vs-human discrepancies, and grader calibration. Revise the ontology only on a new development split, never retroactively on the frozen test set.

### 3. Post-training intervention
Fine-tune a small open model or license head with the failure curriculum plus stability anchors. Test whether evidence uptake improves without leakage returning.

### 4. Provenance uncertainty
Replace perfect provenance metadata with inferred provenance from tool traces, memory stores, and third-party messages. Evaluate spoofing and uncertainty calibration.

### 5. Long-horizon personal state
Embed licensing inside a memory system with temporally evolving facts and authority ordering. Evaluate when fresh tool evidence should supersede remembered user state and vice versa.

## Kill criteria

The agenda should be revised if: human raters do not support the three-channel license ontology; oracle licenses do not improve downstream generation; the method fails to outperform simpler context-gating baselines on naturalistic data; or provenance cannot be inferred robustly enough for the routing abstraction to be useful.
