# Provenance-Licensed Personalization

## Why this benchmark exists

Fixed protected-channel gating is safe but over-conservative: it blocks legitimate personal evidence along with unsupported beliefs. Naive personalization has the opposite failure: it can treat user context as evidence merely because it is personal or explicit. PLP makes evidentiary use depend jointly on **scope × provenance × task**.

## Controlled benchmark

The benchmark contains 1,500 semantic cases and 4,500 policy decisions. It varies task kind, signal scope, and provenance while keeping the licensing target deterministic and auditable.

| Policy | License accuracy ↑ | Licensed evidence uptake ↑ | Unsupported influence leakage ↓ | Epistemic selectivity ↑ |
|---|---:|---:|---:|---:|
| naive | 0.8000 | 1.0000 | 0.3333 | 0.8333 |
| cgsp_fixed | 0.6000 | 0.0000 | 0.0000 | 0.5000 |
| plp | 1.0000 | 1.0000 | 0.0000 | 1.0000 |

## Interpretation

- **Naive** accepts useful verified evidence but also leaks unsupported explicit user claims into the evidentiary path.
- **CGSP-fixed** prevents unsupported influence but also rejects legitimate evidence, demonstrating over-blocking.
- **PLP** separates *personal relevance* from *evidentiary license* and can therefore both resist unsupported context and use verified/personal-state evidence when task-relevant.

These are deterministic contract tests of the routing rule, not frontier-model performance. The scientific next step is to learn the license function from data and evaluate it with real models and blinded human judgments.
