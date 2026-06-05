from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import Message

from intentia_amoris.config import get_settings
from intentia_amoris.domain import ActorRole, Event, EventKind, PrivacyScope, Scales
from intentia_amoris.kernel.embeddings import get_embedding_provider
from intentia_amoris.kernel.engine import IntentiaAmorisEngine
from intentia_amoris.memory.db import SessionLocal, init_db
from intentia_amoris.memory.repository import (
    get_state,
    get_telegram_identity_role,
    record_event,
    search_memory,
    set_state,
    set_telegram_identity,
)

router = Router()
embedder = get_embedding_provider()
engine = IntentiaAmorisEngine(embedder)


def allowed(message: Message) -> bool:
    settings = get_settings()
    if not settings.allowed_ids:
        return True
    return bool(message.from_user and message.from_user.id in settings.allowed_ids)


def render_state(scales: dict, value_function: dict | None = None) -> str:
    order = [
        ("trust", "довіра"),
        ("desire", "бажання"),
        ("fear", "страх"),
        ("safety", "безпека"),
        ("tenderness", "ніжність"),
        ("reciprocity", "взаємність"),
        ("clarity", "ясність"),
        ("future", "майбутнє"),
        ("urgency", "імпульс"),
        ("uncertainty", "невідоме"),
        ("embodiment", "тіло"),
        ("repair", "ремонт"),
        ("autonomy", "автономія"),
        ("reverence", "сакральність"),
    ]
    lines = ["Intentia Amoris терези"]
    for key, label in order:
        if key in scales:
            lines.append(f"{label:<12} {round(scales[key] * 100):02d}%")
    if value_function:
        lines.append("")
        lines.append("функція цінності")
        for k, v in value_function.items():
            lines.append(f"{k:<12} {v}")
    return "\n".join(lines)


def render_result(result: dict) -> str:
    if result.get("blocked"):
        return "Заблоковано consent gate\n" + "\n".join(f"— {r}" for r in result["reasons"])
    parts = [
        "Дует",
        *result.get("duet", []),
        "",
        "Питання",
        *[f"— {q}" for q in result.get("questions", [])],
        "",
        "Порада",
        *[f"— {a}" for a in result.get("advice", [])],
        "",
        render_state(result["scales"], result.get("value_function")),
    ]
    return "\n".join(parts)


@router.message(Command("start"))
async def start(message: Message) -> None:
    if not allowed(message):
        await message.answer("Intentia Amoris закритий для цієї пари.")
        return
    await init_db()
    await message.answer(
        "Intentia Amoris активний\n\n"
        "/role self\n"
        "/role partner\n"
        "/state\n"
        "/advice\n"
        "/ask\n\n"
        "Текст стає подією. Фото й голос будуть збережені тільки з явною згодою."
    )


@router.message(Command("role"))
async def role(message: Message) -> None:
    if not allowed(message) or not message.from_user:
        return
    parts = (message.text or "").split(maxsplit=1)
    raw = parts[1].strip().lower() if len(parts) > 1 else ""
    if raw not in {"self", "partner"}:
        await message.answer("Використай /role self або /role partner")
        return
    async with SessionLocal() as session:
        await set_telegram_identity(
            session,
            telegram_id=message.from_user.id,
            role=raw,
            display_name=message.from_user.full_name or message.from_user.username or str(message.from_user.id),
        )
        await session.commit()
    await message.answer(f"Роль встановлена: {raw}")


@router.message(Command("state"))
async def state(message: Message) -> None:
    if not allowed(message):
        return
    async with SessionLocal() as session:
        row = await get_state(session)
    await message.answer(render_state(row.scales, row.value_function))


@router.message(Command("advice"))
async def advice(message: Message) -> None:
    if not allowed(message):
        return
    async with SessionLocal() as session:
        row = await get_state(session)
        current = Scales.from_dict(row.scales)
    event = Event(actor=ActorRole.SYSTEM, kind=EventKind.ADVICE, content="generate advice", source="telegram")
    result = await engine.process_event(current, event, [])
    await message.answer(render_result(result))


@router.message(Command("ask"))
async def ask(message: Message) -> None:
    if not allowed(message):
        return
    async with SessionLocal() as session:
        row = await get_state(session)
        current = Scales.from_dict(row.scales)
    event = Event(actor=ActorRole.SYSTEM, kind=EventKind.QUESTION, content="ask pair", source="telegram")
    result = await engine.process_event(current, event, [])
    await message.answer("Питання\n" + "\n".join(f"— {q}" for q in result.get("questions", [])))


@router.message(F.text)
async def handle_text(message: Message) -> None:
    if not allowed(message) or not message.from_user or not message.text:
        return
    async with SessionLocal() as session:
        raw_role = await get_telegram_identity_role(session, message.from_user.id)
    role = ActorRole(raw_role) if raw_role in {r.value for r in ActorRole} else ActorRole.UNKNOWN
    event = Event(
        actor=role,
        kind=EventKind.TEXT,
        content=message.text,
        source="telegram",
        privacy_scope=PrivacyScope.PAIR_PRIVATE,
        metadata={"telegram_id": message.from_user.id},
    )
    embedding = await embedder.embed(event.content)
    async with SessionLocal() as session:
        state_row = await get_state(session)
        current = Scales.from_dict(state_row.scales)
        retrieved_rows = await search_memory(session, embedding, limit=5)
        result = await engine.process_event(current, event, [r.content for r in retrieved_rows])
        if not result.get("blocked"):
            await record_event(session, event, embedding)
            await set_state(session, Scales.from_dict(result["scales"]), result["value_function"])
        await session.commit()
    await message.answer(render_result(result))


async def _main() -> None:
    settings = get_settings()
    if not settings.telegram_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is empty")
    logging.basicConfig(level=logging.INFO)
    await init_db()
    bot = Bot(settings.telegram_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


def main() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    main()
