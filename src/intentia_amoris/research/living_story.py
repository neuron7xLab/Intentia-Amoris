from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
import json


@dataclass(frozen=True, slots=True)
class LivingStorySnapshot:
    name: str
    interval: str
    event_count: int
    actors: dict[str, int]
    media: dict[str, int]
    reactions: dict[str, int]
    observable_axes: dict[str, int]
    canon: list[str]
    operational_vows: list[str]

    def to_json(self) -> dict[str, Any]:
        return asdict(self)


def load_messages(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(x) for x in Path(path).read_text(encoding="utf-8").splitlines() if x.strip()]


def build_living_story(messages: list[dict[str, Any]], signals: dict[str, Any]) -> LivingStorySnapshot:
    actor_counts = Counter(m.get("actor", "unknown") for m in messages)
    media_counts = Counter(media.get("kind", "media") for m in messages for media in m.get("media", []))
    reaction_counts = Counter(r for m in messages for r in m.get("reactions", []))

    first = messages[0].get("timestamp_raw") if messages else "unknown"
    last = messages[-1].get("timestamp_raw") if messages else "unknown"

    canon = [
        "Пара не редукується до сексуального імпульсу: у даних є гра, турбота, бажання, межі, очікування, реакції, фото, голос і повторювана взаємність.",
        "Даша не моделюється як обʼєкт без її власних відповідей: партнерська модель активна тільки через її фактичні події або явну згоду.",
        "Ярослав не перетворює травму на командний центр: система підсилює ясність, паузу, ремонт і відповідальність.",
        "Intentia не стверджує приховані гормони, наміри або майбутнє. Вона тримає карту реальності, оновлювану подіями.",
    ]

    operational_vows = [
        "Кожна порада має містити невідоме.",
        "Кожна ескалація близькості проходить autonomy/consent gate.",
        "Кожен медіафайл має hash, source і privacy_scope.",
        "Кожна інтерпретація може бути оскаржена новою відповіддю Даші або Ярослава.",
        "Система зберігає любов як процес, не як клітку.",
    ]

    return LivingStorySnapshot(
        name="Yaroslav ↔ Dasha living digital story",
        interval=f"{first} → {last}",
        event_count=len(messages),
        actors=dict(actor_counts),
        media=dict(media_counts),
        reactions=dict(reaction_counts),
        observable_axes=signals.get("signal_counts", {}),
        canon=canon,
        operational_vows=operational_vows,
    )


def render_markdown(snapshot: LivingStorySnapshot) -> str:
    lines = [
        "# Yaroslav ↔ Dasha Living Story Snapshot",
        "",
        f"Interval: `{snapshot.interval}`",
        f"Events: `{snapshot.event_count}`",
        "",
        "## Actors",
        *[f"- {k}: {v}" for k, v in snapshot.actors.items()],
        "",
        "## Media",
        *[f"- {k}: {v}" for k, v in snapshot.media.items()],
        "",
        "## Reactions",
        *[f"- {k}: {v}" for k, v in snapshot.reactions.items()],
        "",
        "## Observable axes",
        *[f"- {k}: {v}" for k, v in snapshot.observable_axes.items()],
        "",
        "## Canon",
        *[f"- {x}" for x in snapshot.canon],
        "",
        "## Operational vows",
        *[f"- {x}" for x in snapshot.operational_vows],
    ]
    return "\n".join(lines)
