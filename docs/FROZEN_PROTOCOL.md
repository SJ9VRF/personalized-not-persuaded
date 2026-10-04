# Frozen Evaluation Protocol

**Protocol version:** `1.3.1`

This file makes post-hoc changes auditable. The bundled proxy results are tied to the following SHA-256 hashes.

| Artifact | SHA-256 |
|---|---|
| `datasets/behaviorbench/behaviorbench_v1.jsonl` | `476db755ccbb82e390b2e8c06479cfec048536c4dbd490e88dafbcfa2ede5c48` |
| `datasets/contracts/counterfactual_personalization_contracts_v1.jsonl` | `1b551091c96dd55b3ea249ee548b25840d1dda7042f283d6e789515579668188` |
| `behavior_lab/eval/scorer.py` | `ff56aca6217438a905c3e5681febff52b4e0733168fe5cd3b5141c7db16741f3` |
| `behavior_lab/methods/cgsp.py` | `e50ae15dc217da20262b73fb91754f5596e6d2508771a6233e5759f6e90edf08` |
| `scripts/build_contract_benchmark.py` | `a77e5f51ca62038d78484c50608e015d80a37a74d4578b402e62a5fdbad4451e` |
| `scripts/contract_eval.py` | `287e194bfefb4ca83dfb522805e6a8ee6001c638b1ebc1fd9ab17efc146c292b` |

## Change policy

- Changes to any frozen artifact require a protocol version bump.
- Results from different protocol versions must not be pooled without re-running the full pipeline.
- New human/model adapters may be added without changing the frozen scenarios or split.
- Automatic-grader revisions should be reported as a new grader version and calibrated independently.
