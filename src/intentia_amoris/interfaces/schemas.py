from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from intentia_amoris.domain import ActorRole, EventKind, PrivacyScope
from intentia_amoris.security.validation import validate_event_content, validate_metadata


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class EventIn(StrictModel):
    actor: ActorRole = ActorRole.UNKNOWN
    kind: EventKind = EventKind.TEXT
    content: str = Field(min_length=1)
    source: str = Field(default="api", min_length=1, max_length=64)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    privacy_scope: PrivacyScope = PrivacyScope.PAIR_PRIVATE
    metadata: dict[str, Any] = Field(default_factory=dict)

    @field_validator("content")
    @classmethod
    def content_policy(cls, value: str) -> str:
        return validate_event_content(value)

    @field_validator("metadata")
    @classmethod
    def metadata_policy(cls, value: dict[str, Any]) -> dict[str, Any]:
        return validate_metadata(value)


class TelemetryIn(StrictModel):
    actor: ActorRole
    source: str = Field(default="mobile", min_length=1, max_length=64)
    metrics: dict[str, float] = Field(default_factory=dict)
    raw_mood: str | None = Field(default=None, max_length=256)

    @field_validator("metrics")
    @classmethod
    def metric_limits(cls, value: dict[str, float]) -> dict[str, float]:
        if len(value) > 64:
            raise ValueError("too many telemetry metrics")
        return {str(k)[:64]: float(v) for k, v in value.items()}


class ProfileIn(StrictModel):
    role: ActorRole
    name: str = Field(min_length=1, max_length=128)
    summary: str = Field(default="", max_length=12000)
    traits: dict[str, Any] = Field(default_factory=dict)
    boundaries: dict[str, Any] = Field(default_factory=dict)
    values: dict[str, Any] = Field(default_factory=dict)
    consent: dict[str, Any] = Field(default_factory=dict)


class ConsentIn(StrictModel):
    actor: ActorRole
    consent_type: str = Field(min_length=1, max_length=128)
    granted: bool
    scope: PrivacyScope = PrivacyScope.PAIR_PRIVATE
    details: dict[str, Any] = Field(default_factory=dict)
