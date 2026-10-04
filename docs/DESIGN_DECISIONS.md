# Design decisions

This note records the choices that changed the project materially. I keep it separate from the paper because several of these were engineering/research decisions made while iterating, not polished retrospective claims.

## 1. I stopped treating all memory as either trusted or untrusted

**Initial idea:** keep beliefs and memories out of the epistemic path entirely.

**Why I rejected it:** that prevents unsupported influence, but it also blocks legitimate user-specific evidence. A verified flight change and an unsupported opinion are both “memory” at the storage layer, but they should not have the same authority.

**Current choice:** attach provenance and scope to a signal, then grant presentation, personalization, and evidence permissions separately for the current task.

## 2. I separated personalization quality from epistemic stability

A single “personalization score” hides the failure I care about. A model can look highly personalized because it mirrors the user’s claims.

I therefore evaluate two things independently:

- did the response adapt where adaptation was useful?
- did protected factual/calibration behavior change when only user context changed?

This became the matched counterfactual contract suite.

## 3. I kept the default router deterministic

A learned router would be more realistic, but it would make early failures harder to diagnose. The deterministic implementation acts as an executable specification: if a case fails, I can inspect the exact rule and provenance field that caused it.

The learned version is a follow-on experiment, not something I want to hide inside the baseline.

## 4. I removed self-reported policy scores from evaluation

An earlier version let the policy expose latent quality traits. That made evaluation circular. The evaluator now receives response text and scenario metadata, not a policy’s own claim that it was truthful or calibrated.

## 5. I grouped reward-model splits by scenario

Random row splits made near-duplicate profile variants leak across train and test. Grouping by scenario makes the local diagnostic harder and more representative of the intended generalization boundary.

## 6. I keep “contract success” separate from model performance

A deterministic router can reach 100% on a benchmark built to encode its contract. That is useful as a software/specification test, but it is not a scientific result about model behavior.

For that reason, the project page calls these numbers **contract diagnostics** and keeps real-model evaluation as a separate adapter path.

## 7. I kept public claims tied to locally verifiable evidence

The repo includes the source bundle, human-evaluation protocol, and external-model adapter, but not results that were never collected. I would rather leave a boundary explicit than make the portfolio look more complete by inventing evidence.

## What I would do next

The next experiment I would run is deliberately narrow: freeze the provenance suite, evaluate several real model adapters, collect blinded labels on disagreement cases, and learn the license router from those labels while keeping the deterministic router as an oracle/specification baseline.
