from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

Provenance = Literal['explicit_user','inferred','tool_verified','external_verified','synthetic']
Scope = Literal['presentation','preference','goal','constraint','personal_state','world_claim']
TaskKind = Literal['factual_world','personal_state','recommendation','planning','style']

@dataclass(frozen=True)
class UserSignal:
    content: str
    scope: Scope
    provenance: Provenance
    confidence: float = 1.0
    current: bool = True

@dataclass(frozen=True)
class LicenseDecision:
    presentation: bool
    personalization: bool
    evidentiary: bool
    reason: str


def license_signal(signal: UserSignal, task_kind: TaskKind) -> LicenseDecision:
    """Task-conditioned provenance licensing for personalization.

    The same user signal may be useful for presentation/personalization without being
    licensed as evidence. Evidentiary use depends jointly on scope, provenance and task.
    """
    if not signal.current or signal.confidence < 0.5:
        return LicenseDecision(False, False, False, 'stale_or_low_confidence')

    if signal.scope == 'presentation':
        return LicenseDecision(True, True, False, 'presentation_only')
    if signal.scope in {'preference','goal','constraint'}:
        return LicenseDecision(False, True, False, 'decision_relevant_not_world_evidence')

    if signal.scope == 'personal_state':
        if task_kind == 'personal_state' and signal.provenance in {'explicit_user','tool_verified','external_verified'}:
            return LicenseDecision(False, True, True, 'licensed_personal_state_evidence')
        return LicenseDecision(False, True, False, 'personal_context_not_licensed_for_this_task')

    if signal.scope == 'world_claim':
        if signal.provenance in {'tool_verified','external_verified'}:
            return LicenseDecision(False, False, True, 'verified_world_evidence')
        return LicenseDecision(False, False, False, 'unsupported_world_claim')

    return LicenseDecision(False, False, False, 'unlicensed')


def route_signals(signals: list[UserSignal], task_kind: TaskKind) -> dict:
    routed = {'presentation': [], 'personalization': [], 'evidence': [], 'blocked': []}
    for s in signals:
        d = license_signal(s, task_kind)
        rec = {'signal': asdict(s), 'decision': asdict(d)}
        if d.presentation: routed['presentation'].append(rec)
        if d.personalization: routed['personalization'].append(rec)
        if d.evidentiary: routed['evidence'].append(rec)
        if not (d.presentation or d.personalization or d.evidentiary): routed['blocked'].append(rec)
    return routed


def plp_response(task_kind: TaskKind, signals: list[UserSignal], base_answer: str) -> str:
    routed = route_signals(signals, task_kind)
    prefix=[]
    if routed['presentation']:
        prefix.append('Adapting the presentation to your preferred style')
    if routed['personalization']:
        prefix.append('using relevant personal context')
    if routed['evidence']:
        prefix.append('and treating only provenance-licensed context as evidence')
    if routed['blocked']:
        prefix.append('while keeping unsupported user context out of the evidentiary path')
    return (', '.join(prefix) + ': ' if prefix else '') + base_answer
