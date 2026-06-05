from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MESSAGES = ROOT / "data/derived/telegram/messages.jsonl"


def parse_timestamp(raw: str) -> datetime | None:
    match = re.match(
        r"(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT([+-]\d{2}):(\d{2})",
        raw or "",
    )
    if not match:
        return None
    day, month, year, hour, minute, second, off_h, off_m = match.groups()
    return datetime(
        int(year), int(month), int(day), int(hour), int(minute), int(second)
    )


def load_events(path: Path = DEFAULT_MESSAGES) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _text_features(text: str) -> Counter:
    t = (text or "").lower()
    features = Counter()
    if any(x in t for x in ["люб", "кох", "скуч", "сумую", "нрав", "подоба"]):
        features["affection"] += 1
    if any(x in t for x in ["хочу", "секс", "тіло", "тело", "трог", "член", "лобок"]):
        features["eros"] += 1
    if any(x in t for x in ["не хочу", "не планирую", "згода", "согласна", "не дав", "не буду"]):
        features["boundary"] += 1
    if any(x in t for x in ["дякую", "спасибо", "умничка", "молодец"]):
        features["care_repair"] += 1
    if any(x in t for x in ["страх", "бою", "травм", "голов", "бол", "пизд", "хуй"]):
        features["intensity"] += 1
    if any(x in t for x in ["майбут", "назавжди", "життя", "истор", "нarrative", "норатив"]):
        features["future_story"] += 1
    return features


@dataclass(frozen=True, slots=True)
class DialogueMetrics:
    total_events: int
    actors: dict[str, int]
    text_events: int
    media_events: int
    reactions: dict[str, int]
    feature_counts: dict[str, int]
    hourly_distribution: dict[str, int]
    mean_text_length: float
    alternation_ratio: float
    first_timestamp: str | None
    last_timestamp: str | None

    def as_dict(self) -> dict:
        return {
            "total_events": self.total_events,
            "actors": self.actors,
            "text_events": self.text_events,
            "media_events": self.media_events,
            "reactions": self.reactions,
            "feature_counts": self.feature_counts,
            "hourly_distribution": self.hourly_distribution,
            "mean_text_length": self.mean_text_length,
            "alternation_ratio": self.alternation_ratio,
            "first_timestamp": self.first_timestamp,
            "last_timestamp": self.last_timestamp,
        }


def analyze(events: list[dict]) -> DialogueMetrics:
    actors = Counter(e.get("actor", "unknown") for e in events)
    reactions: Counter = Counter()
    features: Counter = Counter()
    hours: Counter = Counter()
    text_lengths: list[int] = []
    timestamps: list[datetime] = []

    alternations = 0
    prev_actor = None

    for event in events:
        actor = event.get("actor", "unknown")
        if prev_actor is not None and actor != prev_actor:
            alternations += 1
        prev_actor = actor

        text = event.get("text") or ""
        if text:
            text_lengths.append(len(text))
            features.update(_text_features(text))

        for reaction in event.get("reactions") or []:
            reactions[str(reaction)] += 1

        dt = parse_timestamp(event.get("timestamp_raw", ""))
        if dt:
            timestamps.append(dt)
            hours[f"{dt.hour:02d}"] += 1

    total = len(events)
    return DialogueMetrics(
        total_events=total,
        actors=dict(actors),
        text_events=sum(1 for e in events if e.get("text")),
        media_events=sum(1 for e in events if e.get("media")),
        reactions=dict(reactions),
        feature_counts=dict(features),
        hourly_distribution=dict(sorted(hours.items())),
        mean_text_length=round(mean(text_lengths), 2) if text_lengths else 0.0,
        alternation_ratio=round(alternations / max(1, total - 1), 4),
        first_timestamp=min(timestamps).isoformat() if timestamps else None,
        last_timestamp=max(timestamps).isoformat() if timestamps else None,
    )


def render_report(metrics: DialogueMetrics) -> str:
    d = metrics.as_dict()
    lines = [
        "# Parousia Dialogue Mining Report",
        "",
        "This report is generated from the parsed Telegram event stream.",
        "",
        "## Core counts",
        "",
        f"- total_events: {d['total_events']}",
        f"- text_events: {d['text_events']}",
        f"- media_events: {d['media_events']}",
        f"- actors: {d['actors']}",
        f"- first_timestamp: {d['first_timestamp']}",
        f"- last_timestamp: {d['last_timestamp']}",
        "",
        "## Relational signal counts",
        "",
    ]
    for key, value in sorted(d["feature_counts"].items()):
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "",
            "These counts are not psychological truth. They are operational indicators.",
            "Any claim about Dasha's internal state requires Dasha's own answer.",
            "Any claim about hormones requires measured data.",
            "",
            "## System use",
            "",
            "Use this report to calibrate prototypes, retrieve memories, and ask better questions.",
            "Do not use it to win arguments.",
        ]
    )
    return "\n".join(lines)


def write_outputs(
    messages: Path = DEFAULT_MESSAGES,
    out_json: Path | None = None,
    out_md: Path | None = None,
) -> DialogueMetrics:
    events = load_events(messages)
    metrics = analyze(events)
    derived = messages.parent
    out_json = out_json or derived / "parousia_metrics.json"
    out_md = out_md or derived / "parousia_dialogue_report.md"
    out_json.write_text(json.dumps(metrics.as_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(render_report(metrics), encoding="utf-8")
    return metrics


def main() -> None:
    metrics = write_outputs()
    print(json.dumps(metrics.as_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
