from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Literal


MetricEvidence = Literal["measured", "inferred", "unknown"]


@dataclass(frozen=True, slots=True)
class Metric:
    name: str
    value: float
    unit: str
    evidence: MetricEvidence = "measured"


@dataclass(frozen=True, slots=True)
class PhoneTelemetryPacket:
    actor: str
    source: Literal["healthkit", "google_fit", "garmin", "manual", "homeassistant"]
    metrics: list[Metric]
    mood_label: str | None = None
    timestamp: datetime = datetime.now(timezone.utc)

    def to_event_content(self) -> str:
        metric_line = ", ".join(f"{m.name}={m.value}{m.unit}" for m in self.metrics)
        mood = f", mood_label={self.mood_label}" if self.mood_label else ""
        return f"telemetry source={self.source}: {metric_line}{mood}"

    def to_json(self) -> dict:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        return data


def classify_telemetry_risk(metrics: dict[str, float]) -> dict[str, float | str]:
    """
    Simple deterministic gate for v0/v1.
    This is not medical interpretation. It only flags patterns for reflection.
    """
    risk = 0.0
    if metrics.get("sleep_hours", 8.0) < 5.5:
        risk += 0.22
    if metrics.get("hrv_ms", 50.0) < 25.0:
        risk += 0.18
    if metrics.get("resting_hr", 60.0) > 85.0:
        risk += 0.16
    if metrics.get("steps", 7000.0) < 2000.0:
        risk += 0.08
    risk = max(0.0, min(1.0, risk))
    label = "steady"
    if risk > 0.55:
        label = "high_load"
    elif risk > 0.28:
        label = "watch"
    return {"risk": round(risk, 3), "label": label}
