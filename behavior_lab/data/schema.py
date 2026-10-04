from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

Role = Literal["user", "assistant", "system", "tool"]
Split = Literal["train", "validation", "test", "pilot"]


@dataclass
class Turn:
    role: Role
    content: str

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Turn":
        if obj.get("role") not in {"user", "assistant", "system", "tool"}:
            raise ValueError(f"invalid role: {obj.get('role')}")
        content = obj.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValueError("turn.content must be a non-empty string")
        return cls(role=obj["role"], content=content)


@dataclass
class UserProfile:
    communication_style: Dict[str, Any] = field(default_factory=dict)
    preferences: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    beliefs: List[str] = field(default_factory=list)
    memories: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "UserProfile":
        if not isinstance(obj, dict):
            raise ValueError("user_profile must be an object")
        return cls(
            communication_style=obj.get("communication_style", {}),
            preferences=obj.get("preferences", []),
            goals=obj.get("goals", []),
            constraints=obj.get("constraints", []),
            beliefs=obj.get("beliefs", []),
            memories=obj.get("memories", []),
        )


@dataclass
class BehaviorLabels:
    personalization: Optional[float] = None
    truthfulness: Optional[float] = None
    sycophancy: Optional[float] = None
    calibration: Optional[float] = None
    emotional_appropriateness: Optional[float] = None
    personality_consistency: Optional[float] = None

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "BehaviorLabels":
        if not isinstance(obj, dict):
            raise ValueError("labels must be an object")
        kwargs = {}
        for key in cls.__dataclass_fields__:
            val = obj.get(key)
            if val is not None:
                if not isinstance(val, (int, float)) or not 0 <= float(val) <= 1:
                    raise ValueError(f"label {key} must be in [0,1] or null")
                val = float(val)
            kwargs[key] = val
        return cls(**kwargs)


@dataclass
class BehaviorScenario:
    scenario_id: str
    category: str
    failure_targets: List[str]
    user_profile: UserProfile
    conversation_history: List[Turn]
    current_user_message: str
    ground_truth: Dict[str, Any]
    desired_behavior: List[str]
    undesired_behavior: List[str]
    labels: BehaviorLabels
    metadata: Dict[str, Any]

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "BehaviorScenario":
        required = {
            "scenario_id",
            "category",
            "failure_targets",
            "user_profile",
            "conversation_history",
            "current_user_message",
            "ground_truth",
            "desired_behavior",
            "undesired_behavior",
            "labels",
            "metadata",
        }
        missing = sorted(required - obj.keys())
        if missing:
            raise ValueError(f"missing fields: {missing}")
        if not isinstance(obj["scenario_id"], str) or not obj["scenario_id"].strip():
            raise ValueError("scenario_id must be a non-empty string")
        if not isinstance(obj["category"], str) or not obj["category"].strip():
            raise ValueError("category must be a non-empty string")
        if not isinstance(obj["failure_targets"], list):
            raise ValueError("failure_targets must be a list")
        if any(not isinstance(x, str) or not x.startswith("MB-") for x in obj["failure_targets"]):
            raise ValueError("failure_targets must contain MB-* identifiers")
        if not isinstance(obj["current_user_message"], str) or not obj["current_user_message"].strip():
            raise ValueError("current_user_message must be non-empty")
        if not isinstance(obj["desired_behavior"], list) or not obj["desired_behavior"]:
            raise ValueError("desired_behavior must be a non-empty list")
        if not isinstance(obj["undesired_behavior"], list):
            raise ValueError("undesired_behavior must be a list")
        if not isinstance(obj["metadata"], dict):
            raise ValueError("metadata must be an object")
        split = obj["metadata"].get("split")
        if split not in {"train", "validation", "test", "pilot"}:
            raise ValueError("metadata.split must be train/validation/test/pilot")

        return cls(
            scenario_id=obj["scenario_id"],
            category=obj["category"],
            failure_targets=obj["failure_targets"],
            user_profile=UserProfile.from_dict(obj["user_profile"]),
            conversation_history=[Turn.from_dict(t) for t in obj["conversation_history"]],
            current_user_message=obj["current_user_message"],
            ground_truth=obj["ground_truth"],
            desired_behavior=obj["desired_behavior"],
            undesired_behavior=obj["undesired_behavior"],
            labels=BehaviorLabels.from_dict(obj["labels"]),
            metadata=obj["metadata"],
        )
