from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import DateTime, Float, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def JsonColumn():
    return JSONB().with_variant(SQLiteJSON(), "sqlite")


class Base(DeclarativeBase):
    pass


class EventRecord(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    actor: Mapped[str] = mapped_column(String(32), index=True)
    kind: Mapped[str] = mapped_column(String(32), index=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    content: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    privacy_scope: Mapped[str] = mapped_column(String(64), default="pair_private")
    metadata: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    embedding: Mapped[list[float]] = mapped_column(JsonColumn(), default=list)


class MemoryChunk(Base):
    __tablename__ = "memory_chunks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    namespace: Mapped[str] = mapped_column(String(128), index=True)
    title: Mapped[str] = mapped_column(String(256), default="")
    content: Mapped[str] = mapped_column(Text)
    privacy_scope: Mapped[str] = mapped_column(String(64), default="pair_private")
    evidence_level: Mapped[str] = mapped_column(String(32), default="inferred")
    embedding: Mapped[list[float]] = mapped_column(JsonColumn(), default=list)
    metadata: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class RelationshipState(Base):
    __tablename__ = "relationship_state"

    pair_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    scales: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    value_function: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class PersonProfile(Base):
    __tablename__ = "person_profiles"
    __table_args__ = (UniqueConstraint("pair_id", "role", name="uq_profile_pair_role"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    role: Mapped[str] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(128))
    summary: Mapped[str] = mapped_column(Text, default="")
    traits: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    boundaries: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    values: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    consent: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    actor: Mapped[str] = mapped_column(String(32), index=True)
    media_kind: Mapped[str] = mapped_column(String(32), index=True)
    storage_path: Mapped[str] = mapped_column(Text)
    sha256: Mapped[str] = mapped_column(String(128), index=True)
    caption: Mapped[str] = mapped_column(Text, default="")
    vlm_description: Mapped[str] = mapped_column(Text, default="")
    privacy_scope: Mapped[str] = mapped_column(String(64), default="pair_private")
    metadata: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    actor: Mapped[str] = mapped_column(String(32), index=True)
    source: Mapped[str] = mapped_column(String(64), index=True)
    metrics: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    raw_mood: Mapped[str] = mapped_column(String(128), default="")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )


class ConsentRecord(Base):
    __tablename__ = "consents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    actor: Mapped[str] = mapped_column(String(32), index=True)
    consent_type: Mapped[str] = mapped_column(String(128), index=True)
    granted: Mapped[bool] = mapped_column(default=False)
    scope: Mapped[str] = mapped_column(String(128), default="pair_private")
    details: Mapped[dict[str, Any]] = mapped_column(JsonColumn(), default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class BeliefRecord(Base):
    __tablename__ = "beliefs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    key: Mapped[str] = mapped_column(String(256), index=True)
    claim: Mapped[str] = mapped_column(Text)
    evidence_level: Mapped[str] = mapped_column(String(32), default="inferred")
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    evidence_count: Mapped[int] = mapped_column(Integer, default=0)
    counterevidence_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )


class TelegramIdentity(Base):
    __tablename__ = "telegram_identities"
    __table_args__ = (UniqueConstraint("pair_id", "telegram_id", name="uq_telegram_identity_pair_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    pair_id: Mapped[str] = mapped_column(String(128), index=True)
    telegram_id: Mapped[int] = mapped_column(Integer, index=True)
    role: Mapped[str] = mapped_column(String(32), default="unknown", index=True)
    display_name: Mapped[str] = mapped_column(String(128), default="")
    consent_scope: Mapped[str] = mapped_column(String(64), default="pair_private")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
