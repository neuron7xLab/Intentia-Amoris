from __future__ import annotations

from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status

from intentia_amoris.config import get_settings
from intentia_amoris.domain import ActorRole, Event, EventKind, PrivacyScope, Scales, Telemetry
from intentia_amoris.import_seed import import_seed
from intentia_amoris.interfaces.schemas import ConsentIn, EventIn, ProfileIn, TelemetryIn
from intentia_amoris.kernel.embeddings import get_embedding_provider
from intentia_amoris.kernel.engine import IntentiaAmorisEngine
from intentia_amoris.memory.db import SessionLocal, init_db
from intentia_amoris.memory.repository import (
    get_state,
    record_consent,
    record_event,
    record_media,
    record_telemetry,
    search_memory,
    set_state,
    upsert_profile,
)
from intentia_amoris.multimodal.media import build_media_description_stub, store_media_bytes
from intentia_amoris.policies.consent import ConsentGate
from intentia_amoris.security.auth import Principal, require_api_key, require_scope
from intentia_amoris.security.audit import AuditEvent, AuditLedger
from intentia_amoris.security.middleware import security_headers_middleware
from intentia_amoris.security.rate_limit import rate_limit_dependency
from intentia_amoris.security.validation import ValidationError, validate_media_upload

app = FastAPI(title="Intentia Amoris", version="1.0.0")
app.middleware("http")(security_headers_middleware)

embedder = get_embedding_provider()
engine = IntentiaAmorisEngine(embedder)


@app.on_event("startup")
async def startup() -> None:
    get_settings().assert_runtime_safe()
    await init_db()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "system": "intentia-amoris", "version": "1.0.0"}


@app.get("/ready")
async def ready() -> dict[str, str]:
    get_settings().assert_runtime_safe()
    return {"status": "ready"}


Protected = Depends(require_api_key)
RateLimited = Depends(rate_limit_dependency)


@app.get("/state", dependencies=[RateLimited])
async def state(principal: Principal = Protected) -> dict:
    require_scope(principal, "read")
    async with SessionLocal() as session:
        row = await get_state(session)
        return {"scales": row.scales, "value_function": row.value_function, "updated_at": row.updated_at}




@app.get("/value", dependencies=[RateLimited])
async def value(principal: Principal = Protected) -> dict:
    """Current canonical Intentia value vector."""
    require_scope(principal, "read")
    from intentia_amoris.kernel.value_core import compute_intentia_value, decision_from_value
    async with SessionLocal() as session:
        row = await get_state(session)
        scales = Scales.from_dict(row.scales)
        intentia = compute_intentia_value(
            scales,
            {
                "retrieval_quality": 0.74,
                "archive_integrity": 0.88,
                "consent_freshness": 0.62,
                "privacy_quality": 0.82,
                "reproducibility": 0.84,
                "auditability": 0.90,
            },
        )
        return {"intentia_value": intentia.as_dict(), "policy": decision_from_value(intentia)}


@app.post("/events", dependencies=[RateLimited])
async def events(payload: EventIn, principal: Principal = Protected) -> dict:
    require_scope(principal, "write")
    event = Event(
        actor=payload.actor,
        kind=payload.kind,
        content=payload.content,
        source=payload.source,
        confidence=payload.confidence,
        privacy_scope=payload.privacy_scope,
        metadata=payload.metadata,
    )
    event_embedding = await embedder.embed(event.content)

    async with SessionLocal() as session:
        state_row = await get_state(session)
        current = Scales.from_dict(state_row.scales)
        retrieved_rows = await search_memory(session, event_embedding, limit=5)
        retrieved = [r.content for r in retrieved_rows]

        result = await engine.process_event(current, event, retrieved)
        if not result.get("blocked"):
            await record_event(session, event, event_embedding)
            await set_state(session, Scales.from_dict(result["scales"]), result["value_function"])
        await session.commit()

    AuditLedger().append(
        AuditEvent(
            event_type="domain.event",
            actor=event.actor.value,
            action=event.kind.value,
            target=event.source,
            allowed=not result.get("blocked", False),
            reason="; ".join(result.get("reasons", [])),
            metadata={"privacy_scope": event.privacy_scope.value, "principal": principal.subject},
        )
    )
    return result


@app.post("/telemetry", dependencies=[RateLimited])
async def telemetry(payload: TelemetryIn, principal: Principal = Protected) -> dict:
    require_scope(principal, "write")
    telemetry_obj = Telemetry(
        actor=payload.actor,
        source=payload.source,
        metrics=payload.metrics,
        raw_mood=payload.raw_mood,
    )
    event = await engine.telemetry_to_event(telemetry_obj)
    embedding = await embedder.embed(event.content)

    async with SessionLocal() as session:
        await record_telemetry(session, telemetry_obj)
        state_row = await get_state(session)
        current = Scales.from_dict(state_row.scales)
        retrieved_rows = await search_memory(session, embedding, limit=5)
        result = await engine.process_event(current, event, [r.content for r in retrieved_rows])
        if not result.get("blocked"):
            await record_event(session, event, embedding)
            await set_state(session, Scales.from_dict(result["scales"]), result["value_function"])
        await session.commit()
        return result


@app.post("/media", dependencies=[RateLimited])
async def media(
    actor: str = Form(...),
    kind: str = Form("image"),
    caption: str = Form(""),
    privacy_scope: str = Form("pair_private"),
    consent_confirmed: bool = Form(False),
    file: UploadFile = File(...),
    principal: Principal = Protected,
) -> dict:
    require_scope(principal, "write")
    if kind not in {"image", "audio", "video"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="kind must be image/audio/video")

    actor_role = ActorRole(actor) if actor in {r.value for r in ActorRole} else ActorRole.UNKNOWN
    scope = PrivacyScope(privacy_scope) if privacy_scope in {s.value for s in PrivacyScope} else PrivacyScope.PAIR_PRIVATE
    event_kind = {"image": EventKind.IMAGE, "audio": EventKind.AUDIO, "video": EventKind.VIDEO}[kind]

    pre_event = Event(
        actor=actor_role,
        kind=event_kind,
        content=caption or f"{kind} upload",
        source="media",
        privacy_scope=scope,
        metadata={"consent_confirmed": consent_confirmed, "filename": file.filename or "upload.bin"},
    )
    gate = ConsentGate().evaluate_event(pre_event)
    if not gate.allowed:
        return {
            "blocked": True,
            "reasons": gate.reasons,
            "required_action": gate.required_action,
            "scales": Scales().as_dict(),
        }

    data = await file.read()
    try:
        validate_media_upload(data, file.filename or "upload.bin")
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=str(exc)) from exc

    storage_path, sha = await store_media_bytes(data, file.filename or "upload.bin", actor, kind)
    description = build_media_description_stub(kind, caption, {"sha256": sha})
    content = f"{caption}\n{description}".strip()
    event = Event(
        actor=actor_role,
        kind=event_kind,
        content=content,
        source="media",
        privacy_scope=scope,
        metadata={"sha256": sha, "storage_path": storage_path, "consent_confirmed": consent_confirmed},
    )

    embedding = await embedder.embed(content)
    async with SessionLocal() as session:
        state_row = await get_state(session)
        current = Scales.from_dict(state_row.scales)
        retrieved = [r.content for r in await search_memory(session, embedding, limit=5)]
        result = await engine.process_event(current, event, retrieved)
        if not result.get("blocked"):
            await record_media(
                session,
                actor=actor,
                media_kind=kind,
                storage_path=storage_path,
                sha256=sha,
                caption=caption,
                vlm_description=description,
                privacy_scope=privacy_scope,
            )
            await record_event(session, event, embedding)
            await set_state(session, Scales.from_dict(result["scales"]), result["value_function"])
        await session.commit()
        return result


@app.post("/profiles", dependencies=[RateLimited])
async def profiles(payload: ProfileIn, principal: Principal = Protected) -> dict:
    require_scope(principal, "write")
    async with SessionLocal() as session:
        row = await upsert_profile(
            session,
            role=payload.role.value,
            name=payload.name,
            summary=payload.summary,
            traits=payload.traits,
            boundaries=payload.boundaries,
            values=payload.values,
            consent=payload.consent,
        )
        await session.commit()
        return {"id": row.id, "role": row.role, "name": row.name}


@app.post("/consent", dependencies=[RateLimited])
async def consent(payload: ConsentIn, principal: Principal = Protected) -> dict:
    require_scope(principal, "write")
    async with SessionLocal() as session:
        row = await record_consent(
            session,
            actor=payload.actor.value,
            consent_type=payload.consent_type,
            granted=payload.granted,
            scope=payload.scope.value,
            details=payload.details,
        )
        await session.commit()
        return {"id": row.id, "granted": row.granted}


@app.post("/import/seed", dependencies=[RateLimited])
async def import_seed_endpoint(principal: Principal = Protected) -> dict:
    require_scope(principal, "admin")
    count = await import_seed(Path("seeds"))
    return {"imported_chunks": count}


@app.get("/memory/search", dependencies=[RateLimited])
async def memory_search(q: str, limit: int = 5, principal: Principal = Protected) -> dict:
    require_scope(principal, "read")
    safe_limit = min(max(int(limit), 1), 20)
    embedding = await embedder.embed(q[: get_settings().max_content_chars])
    async with SessionLocal() as session:
        rows = await search_memory(session, embedding, limit=safe_limit)
        return {
            "results": [
                {"title": r.title, "namespace": r.namespace, "content": r.content, "metadata": r.metadata}
                for r in rows
            ]
        }


def run() -> None:
    uvicorn.run("intentia_amoris.api:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
