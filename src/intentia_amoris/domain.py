from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any


class ActorRole(StrEnum):
    SELF = "self"
    PARTNER = "partner"
    ALETHEIA = "aletheia"
    EUNOIA = "eunoia"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class EventKind(StrEnum):
    TEXT = "text"
    ANSWER = "answer"
    QUESTION = "question"
    ADVICE = "advice"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    TELEMETRY = "telemetry"
    LAB = "lab"
    PROFILE = "profile"
    MEMORY = "memory"
    CONSENT = "consent"
    STATE = "state"


class PrivacyScope(StrEnum):
    SELF_PRIVATE = "self_private"
    PARTNER_PRIVATE = "partner_private"
    PAIR_PRIVATE = "pair_private"
    RESEARCH_ANONYMIZED = "research_anonymized"
    PUBLIC = "public"


class EvidenceLevel(StrEnum):
    MEASURED = "measured"
    INFERRED = "inferred"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class Scales:
    trust: float = 0.50
    desire: float = 0.50
    fear: float = 0.35
    safety: float = 0.50
    tenderness: float = 0.50
    reciprocity: float = 0.50
    clarity: float = 0.50
    future: float = 0.50
    urgency: float = 0.40
    uncertainty: float = 0.55
    embodiment: float = 0.50
    repair: float = 0.50
    autonomy: float = 0.60
    reverence: float = 0.50

    def as_dict(self) -> dict[str, float]:
        return {name: float(getattr(self, name)) for name in self.__dataclass_fields__}

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "Scales":
        if not data:
            return cls()
        allowed = cls.__dataclass_fields__.keys()
        return cls(**{k: float(v) for k, v in data.items() if k in allowed})

    def updated(self, values: dict[str, float]) -> "Scales":
        clean = {k: clamp(v) for k, v in values.items() if k in self.__dataclass_fields__}
        return replace(self, **clean)


@dataclass(slots=True)
class Event:
    actor: ActorRole
    kind: EventKind
    content: str
    source: str = "api"
    confidence: float = 1.0
    privacy_scope: PrivacyScope = PrivacyScope.PAIR_PRIVATE
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class Telemetry:
    actor: ActorRole
    source: str
    metrics: dict[str, float]
    raw_mood: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(slots=True)
class CycleOutput:
    observed_facts: list[str]
    retrieved_memories: list[str]
    inferred_states: dict[str, float]
    uncertainty: list[str]
    updated_scales: Scales
    duet: list[str]
    questions: list[str]
    advice: list[str]
    value_function: dict[str, float]


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))
