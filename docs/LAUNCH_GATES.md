# Research Gates

The repository separates a **research-candidate gate** from any production launch decision.

The executable gate in `scripts/launch_gate.py` checks the controlled licensing stack:

- ID exact license match >= 0.95
- domain-OOD exact match >= 0.90
- compositional exact match >= 0.75
- domain-OOD unsupported evidence leakage <= 0.02
- domain-OOD licensed evidence uptake >= 0.75
- trajectory-weighted state-verification score >= 0.90

The current controlled run passes this gate. That means the method is worth advancing to real-model and human evaluation; it does **not** mean it is production-ready.

## Gates required before a real launch claim

A stronger gate would additionally require:

1. blinded human validity on a frozen annotation sample;
2. end-to-end generation compliance with oracle and predicted licenses;
3. multiple real model families and decoding seeds;
4. long-context/tool-trace evaluation with stale and conflicting state;
5. adversarial provenance spoofing and prompt-injection tests;
6. latency and cost budgets on the target serving stack;
7. no material regression on non-personalized factuality, instruction following, and safety suites.
