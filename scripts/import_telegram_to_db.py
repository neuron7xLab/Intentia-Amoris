from __future__ import annotations

import asyncio
import json
from pathlib import Path

import typer
from rich import print

from intentia_amoris.domain import ActorRole, Event, EventKind, PrivacyScope
from intentia_amoris.kernel.embeddings import get_embedding_provider
from intentia_amoris.memory.db import SessionLocal, init_db
from intentia_amoris.memory.repository import record_event, set_state, get_state, record_media
from intentia_amoris.kernel.engine import IntentiaEternityEngine
from intentia_amoris.domain import Scales

app = typer.Typer(help="Load parsed Telegram JSONL into Intentia database.")


def _actor(value: str) -> ActorRole:
    try:
        return ActorRole(value)
    except ValueError:
        return ActorRole.UNKNOWN


def _kind_from_message(row: dict) -> EventKind:
    if row.get("media") and not row.get("text"):
        media_kind = row["media"][0].get("kind")
        if media_kind == "photo":
            return EventKind.IMAGE
        if media_kind == "video":
            return EventKind.VIDEO
        if media_kind == "voice":
            return EventKind.AUDIO
    return EventKind.TEXT


async def import_jsonl(path: Path) -> None:
    await init_db()
    embedder = get_embedding_provider()
    engine = IntentiaEternityEngine(embedder)

    async with SessionLocal() as session:
        state = await get_state(session)
        current = Scales.from_dict(state.scales)

        count = 0
        media_count = 0
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            content_parts = []
            if row.get("text"):
                content_parts.append(row["text"])
            for media in row.get("media", []):
                content_parts.append(f"[{media.get('kind')}:{media.get('href')}]")
            content = "\n".join(content_parts).strip() or "[empty telegram event]"

            event = Event(
                actor=_actor(row.get("actor", "unknown")),
                kind=_kind_from_message(row),
                content=content,
                source="telegram_export",
                confidence=1.0,
                privacy_scope=PrivacyScope.PAIR_PRIVATE,
                metadata={
                    "telegram_message_id": row.get("message_id"),
                    "timestamp_raw": row.get("timestamp_raw"),
                    "sender_raw": row.get("sender_raw"),
                    "day": row.get("day"),
                    "reactions": row.get("reactions", []),
                    "reply_to": row.get("reply_to"),
                    "links": row.get("links", []),
                    "media": row.get("media", []),
                },
            )
            emb = await embedder.embed(event.content)
            result = await engine.process_event(current, event, [])
            await record_event(session, event, emb)
            current = Scales.from_dict(result["scales"]) if not result.get("blocked") else current
            await set_state(session, current, result.get("value_function", {}))

            for media in row.get("media", []):
                if media.get("href", "").startswith("call:"):
                    continue
                await record_media(
                    session=session,
                    actor=row.get("actor", "unknown"),
                    media_kind=media.get("kind", "media"),
                    storage_path=f"telegram_export_zip://{media.get('href')}",
                    sha256=media.get("sha256") or "",
                    caption=row.get("text") or "",
                    vlm_description="pending_vlm_description",
                    privacy_scope=PrivacyScope.PAIR_PRIVATE.value,
                    metadata={
                        "telegram_message_id": row.get("message_id"),
                        "timestamp_raw": row.get("timestamp_raw"),
                        "size": media.get("size"),
                    },
                )
                media_count += 1

            count += 1

        await session.commit()

    print(f"[bold green]Imported {count} telegram events and {media_count} media assets[/bold green]")


@app.command()
def run(
    jsonl_path: Path = typer.Argument(Path("data/derived/telegram/messages.jsonl"), exists=True),
) -> None:
    asyncio.run(import_jsonl(jsonl_path))


def main() -> None:
    app()


if __name__ == "__main__":
    main()
