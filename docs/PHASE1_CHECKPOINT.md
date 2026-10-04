# Phase 1 Checkpoint

## Completed

- Central thesis and falsifiable hypotheses
- Experimental factors and success criteria
- 20-class behavior failure taxonomy
- Metric definitions
- Typed benchmark schema
- 20 human-authored canonical seed scenarios
- Dataset validator
- Initial metric utilities
- Unit tests

## Verified

- Seed dataset validation: PASS (20/20 scenarios)
- Unit tests: PASS (5/5)

## Next implementation milestone — Phase 2A

Build the first 1,000-example benchmark without contaminating the final test set.

### Planned composition

- 12 core scenario families × ~60–80 examples
- 200 held-out adversarial transformations
- balanced personalization conditions P0–P5
- explicit semantic-cluster split to prevent near-duplicate leakage

### Next code components

1. Scenario template registry
2. Controlled synthetic generator interface
3. Deduplication / semantic-cluster guard
4. Quality-filter pipeline
5. Train/validation/test split builder
6. Annotation packet exporter
7. Baseline response runner abstraction
8. Grader interface and human-calibration format

### Freeze rule

The final test templates must be frozen before any reward-model or post-training experiment consumes benchmark-derived data.
