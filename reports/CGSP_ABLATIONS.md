# CGSP Component Ablations

These ablations test whether the contract result depends on both sides of the factorization: useful adaptation and protected-channel non-interference.

| Variant | Contracts | APG ↑ | PED ↓ | PEI ↑ | Contract score ↑ | Pass rate ↑ |
|---|---:|---:|---:|---:|---:|---:|
| Ablate-allowed | 820 | -0.2076 | 0.0000 | 1.0000 | -0.2076 | 0.0% |
| Ablate-protection | 820 | 0.3520 | 0.1641 | 0.8359 | 0.1878 | 29.3% |
| CGSP-full | 820 | 0.3627 | 0.0000 | 1.0000 | 0.3627 | 100.0% |
| Style-only | 820 | 0.3520 | 0.0000 | 1.0000 | 0.3520 | 90.2% |

## Interpretation

- **Ablate-allowed** removes personalization and tests whether invariance alone can satisfy the contract.
- **Ablate-protection** deliberately permits beliefs/memories to affect epistemic stance and tests whether the protected gate is necessary.
- **Style-only** keeps only communication-style adaptation and tests whether richer allowed channels contribute additional personalization.
- **CGSP-full** uses the full allowed set while excluding protected channels from response construction.

All values are controlled proxy diagnostics, not frontier-model claims.
