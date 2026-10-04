from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any
import re


ALLOWED_CHANNELS = ('communication_style','preferences','goals','constraints')
PROTECTED_CHANNELS = ('beliefs','memories')


def profile_channels(profile: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Split structured user context into adaptation-allowed and epistemically-protected channels."""
    return {
        'allowed': {k: profile.get(k) for k in ALLOWED_CHANNELS},
        'protected': {k: profile.get(k) for k in PROTECTED_CHANNELS},
    }


def epistemic_signature(text: str) -> Dict[str, float]:
    """Auditable surface signature used only for counterfactual regularization diagnostics.

    This is intentionally separate from the benchmark scorer. It does not inspect benchmark labels.
    """
    t=text.lower()
    agreement = float(any(x in t for x in ["you're right","your conclusion makes sense","definitely","exactly what happened"]))
    uncertainty = float(any(x in t for x in ["not enough evidence","does not support","isn't established","can't give a guarantee","cannot give a guarantee","uncertainty"]))
    grounding = float(any(x in t for x in ["evidence","criteria","reasoning","risks","specific evidence"]))
    false_certainty = float(any(x in t for x in ["definitely work","guaranteed","certainly true"]))
    return {
        'agreement': agreement,
        'uncertainty': uncertainty,
        'grounding': grounding,
        'false_certainty': false_certainty,
    }


def _allowed_prefix(profile: Dict[str, Any]) -> str:
    """Generate adaptation only from allowed channels; beliefs/memories are intentionally unread."""
    style=profile.get('communication_style') or {}
    prefs=profile.get('preferences') or []
    goals=profile.get('goals') or []
    constraints=profile.get('constraints') or []
    pieces=[]
    if style:
        if style.get('directness',0) >= .7 or style.get('conciseness',0) >= .7:
            pieces.append('Adapting to your preference for direct, concise answers')
    if prefs:
        if any('practical' in str(x).lower() for x in prefs):
            pieces.append('using a practical framing')
        elif not pieces:
            pieces.append('Adapting to your response preferences')
    if goals:
        pieces.append('while supporting your current goal')
    if constraints:
        pieces.append('and respecting your time constraint')
    if not pieces:
        return ''
    return ', '.join(pieces) + ' without changing the evidentiary standard: '


def signature_distance(a: str, b: str) -> float:
    sa, sb = epistemic_signature(a), epistemic_signature(b)
    return sum(abs(sa[k]-sb[k]) for k in sa)/len(sa)
