from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from intentia_amoris.config import get_settings
from intentia_amoris.domain import Event, Scales, Telemetry
from intentia_amoris.kernel.embeddings import cosine
from intentia_amoris.memory.models import (
    ConsentRecord,
    EventRecord,
    MediaAsset,
    MemoryChunk,
    PersonProfile,
    RelationshipState,
    TelemetryRecord,
    TelegramIdentity,
)


async def get_state(session: AsyncSession, pair_id: str | None = None) -> RelationshipState:
    settings = get_settings()
    pid = pair_id or settings.pair_id
    row = await session.get(RelationshipState, pid)
    if row is None:
        row = RelationshipState(pair_id=pid, scales=Scales().as_dict(), value_function={})
        session.add(row)
        await session.flush()
    return row


async def set_state(
    session: AsyncSession,
    scales: Scales,
    value_function: dict[str, float],
    pair_id: str | None = None,
) -> RelationshipState:
    row = await get_state(session, pair_id)
    row.scales = scales.as_dict()
    row.value_function = value_function
    row.updated_at = datetime.now(timezone.utc)
    await session.flush()
    return row


async def record_event(
    session: AsyncSession,
    event: Event,
    embedding: list[float],
    pair_id: str | None = None,
) -> EventRecord:
    settings = get_settings()
    row = EventRecord(
        pair_id=pair_id or settings.pair_id,
        actor=event.actor.value,
        kind=event.kind.value,
        source=event.source,
        content=event.content,
        confidence=event.confidence,
        privacy_scope=event.privacy_scope.value,
        metadata=event.metadata,
        embedding=embedding,
    )
    session.add(row)
    await session.flush()
    return row


async def add_memory_chunk(
    session: AsyncSession,
    namespace: str,
    title: str,
    content: str,
    embedding: list[float],
    pair_id: str | None = None,
    privacy_scope: str = "pair_private",
    evidence_level: str = "inferred",
    metadata: dict | None = None,
) -> MemoryChunk:
    settings = get_settings()
    row = MemoryChunk(
        pair_id=pair_id or settings.pair_id,
        namespace=namespace,
        title=title,
        content=content,
        embedding=embedding,
        privacy_scope=privacy_scope,
        evidence_level=evidence_level,
        metadata=metadata or {},
    )
    session.add(row)
    await session.flush()
    return row


async def search_memory(
    session: AsyncSession,
    query_embedding: list[float],
    pair_id: str | None = None,
    limit: int = 5,
) -> list[MemoryChunk]:
    settings = get_settings()
    pid = pair_id or settings.pair_id
    result = await session.execute(select(MemoryChunk).where(MemoryChunk.pair_id == pid))
    chunks = list(result.scalars().all())
    chunks.sort(key=lambda c: cosine(c.embedding or [], query_embedding), reverse=True)
    return chunks[:limit]


async def upsert_profile(
    session: AsyncSession,
    role: str,
    name: str,
    summary: str,
    traits: dict,
    boundaries: dict,
    values: dict,
    consent: dict,
    pair_id: str | None = None,
) -> PersonProfile:
    settings = get_settings()
    pid = pair_id or settings.pair_id
    result = await session.execute(
        select(PersonProfile).where(PersonProfile.pair_id == pid, PersonProfile.role == role)
    )
    row = result.scalar_one_or_none()
    if row is None:
        row = PersonProfile(pair_id=pid, role=role, name=name)
        session.add(row)
    row.name = name
    row.summary = summary
    row.traits = traits
    row.boundaries = boundaries
    row.values = values
    row.consent = consent
    row.updated_at = datetime.now(timezone.utc)
    await session.flush()
    return row


async def record_telemetry(
    session: AsyncSession,
    telemetry: Telemetry,
    pair_id: str | None = None,
) -> TelemetryRecord:
    settings = get_settings()
    row = TelemetryRecord(
        pair_id=pair_id or settings.pair_id,
        actor=telemetry.actor.value,
        source=telemetry.source,
        metrics=telemetry.metrics,
        raw_mood=telemetry.raw_mood or "",
    )
    session.add(row)
    await session.flush()
    return row


async def record_consent(
    session: AsyncSession,
    actor: str,
    consent_type: str,
    granted: bool,
    scope: str,
    details: dict | None = None,
    pair_id: str | None = None,
) -> ConsentRecord:
    settings = get_settings()
    row = ConsentRecord(
        pair_id=pair_id or settings.pair_id,
        actor=actor,
        consent_type=consent_type,
        granted=granted,
        scope=scope,
        details=details or {},
    )
    session.add(row)
    await session.flush()
    return row


async def record_media(
    session: AsyncSession,
    actor: str,
    media_kind: str,
    storage_path: str,
    sha256: str,
    caption: str,
    vlm_description: str,
    privacy_scope: str,
    metadata: dict | None = None,
    pair_id: str | None = None,
) -> MediaAsset:
    settings = get_settings()
    row = MediaAsset(
        pair_id=pair_id or settings.pair_id,
        actor=actor,
        media_kind=media_kind,
        storage_path=storage_path,
        sha256=sha256,
        caption=caption,
        vlm_description=vlm_description,
        privacy_scope=privacy_scope,
        metadata=metadata or {},
    )
    session.add(row)
    await session.flush()
    return row



async def set_telegram_identity(
    session: AsyncSession,
    telegram_id: int,
    role: str,
    display_name: str,
    consent_scope: str = "pair_private",
    pair_id: str | None = None,
) -> TelegramIdentity:
    settings = get_settings()
    pid = pair_id or settings.pair_id
    result = await session.execute(
        select(TelegramIdentity).where(
            TelegramIdentity.pair_id == pid,
            TelegramIdentity.telegram_id == telegram_id,
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        row = TelegramIdentity(pair_id=pid, telegram_id=telegram_id)
        session.add(row)
    row.role = role
    row.display_name = display_name
    row.consent_scope = consent_scope
    row.updated_at = datetime.now(timezone.utc)
    await session.flush()
    return row


async def get_telegram_identity_role(
    session: AsyncSession,
    telegram_id: int,
    pair_id: str | None = None,
) -> str:
    settings = get_settings()
    pid = pair_id or settings.pair_id
    result = await session.execute(
        select(TelegramIdentity).where(
            TelegramIdentity.pair_id == pid,
            TelegramIdentity.telegram_id == telegram_id,
        )
    )
    row = result.scalar_one_or_none()
    return row.role if row else "unknown"
