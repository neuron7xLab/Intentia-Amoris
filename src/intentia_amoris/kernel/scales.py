from __future__ import annotations

from dataclasses import dataclass

from intentia_amoris.domain import Scales, clamp
from intentia_amoris.kernel.embeddings import EmbeddingProvider, cosine
from intentia_amoris.kernel.prototypes import PROTOTYPES, Prototype


@dataclass(slots=True)
class ScaleUpdate:
    signals: dict[str, float]
    prototype_hits: dict[str, float]
    new_scales: Scales


class DynamicScalesKernel:
    """
    Neural-ish plasticity kernel.

    v0 used keyword increments.
    v2 uses prototype similarity + small constraints.
    """

    def __init__(self, embedding_provider: EmbeddingProvider, learning_rate: float = 0.72) -> None:
        self.embedding_provider = embedding_provider
        self.learning_rate = learning_rate
        self._prototype_vectors: dict[str, list[float]] = {}

    async def warmup(self) -> None:
        for prototype in PROTOTYPES:
            self._prototype_vectors[prototype.key] = await self.embedding_provider.embed(prototype.text)

    async def update(self, current: Scales, text: str) -> ScaleUpdate:
        if not self._prototype_vectors:
            await self.warmup()

        event_vec = await self.embedding_provider.embed(text)
        signals = {k: 0.0 for k in current.as_dict()}
        hits: dict[str, float] = {}

        for prototype in PROTOTYPES:
            sim = cosine(event_vec, self._prototype_vectors[prototype.key])
            if sim <= prototype.threshold:
                continue

            strength = (sim - prototype.threshold) / max(1e-6, 1.0 - prototype.threshold)
            hits[prototype.key] = round(float(sim), 4)

            for scale, delta in prototype.scale_deltas.items():
                signals[scale] = signals.get(scale, 0.0) + delta * strength

        values = current.as_dict()
        for scale, signal in signals.items():
            values[scale] = clamp(values[scale] + signal * self.learning_rate)

        self._apply_homeostasis(values)
        new_scales = current.updated(values)

        return ScaleUpdate(
            signals={k: round(v, 4) for k, v in signals.items() if abs(v) > 0.0001},
            prototype_hits=hits,
            new_scales=new_scales,
        )

    def _apply_homeostasis(self, values: dict[str, float]) -> None:
        # If desire and urgency rise faster than safety/reciprocity, risk grows.
        if values["desire"] > 0.74 and values["urgency"] > 0.62 and values["safety"] < 0.62:
            values["uncertainty"] = clamp(values["uncertainty"] + 0.035)
            values["autonomy"] = clamp(values["autonomy"] - 0.020)

        # Consent/autonomy calms the system without killing desire.
        if values["autonomy"] > 0.70 and values["clarity"] > 0.58:
            values["safety"] = clamp(values["safety"] + 0.018)
            values["fear"] = clamp(values["fear"] - 0.014)

        # Repair protects future from fear.
        if values["repair"] > 0.62 and values["trust"] > 0.58:
            values["future"] = clamp(values["future"] + 0.012)
            values["uncertainty"] = clamp(values["uncertainty"] - 0.012)


def value_function(scales: Scales) -> dict[str, float]:
    s = scales.as_dict()
    flourishing = (
        s["trust"] * 0.13
        + s["safety"] * 0.14
        + s["tenderness"] * 0.11
        + s["reciprocity"] * 0.12
        + s["clarity"] * 0.10
        + s["future"] * 0.11
        + s["autonomy"] * 0.12
        + s["repair"] * 0.07
        + s["reverence"] * 0.08
        + s["desire"] * 0.08
        - s["fear"] * 0.10
        - s["urgency"] * 0.08
        - s["uncertainty"] * 0.07
    )
    pressure = s["desire"] * 0.30 + s["urgency"] * 0.32 + s["fear"] * 0.17 + s["uncertainty"] * 0.10
    readiness = s["safety"] * 0.25 + s["reciprocity"] * 0.22 + s["clarity"] * 0.18 + s["autonomy"] * 0.22 + s["trust"] * 0.13
    risk = pressure * 0.65 + (1.0 - readiness) * 0.35
    return {
        "flourishing": round(clamp(flourishing), 3),
        "pressure": round(clamp(pressure), 3),
        "readiness": round(clamp(readiness), 3),
        "risk": round(clamp(risk), 3),
    }
