from __future__ import annotations

from dataclasses import dataclass

from intentia_amoris.domain import Scales


@dataclass(frozen=True, slots=True)
class Prototype:
    key: str
    text: str
    scale_deltas: dict[str, float]
    threshold: float = 0.18


PROTOTYPES: tuple[Prototype, ...] = (
    Prototype(
        key="secure_tender_closeness",
        text=(
            "Ми говоримо спокійно, прямо, ніжно і взаємно. "
            "Кожен дотик має згоду. Поруч безпечно. Ніхто не тисне."
        ),
        scale_deltas={
            "trust": 0.045,
            "safety": 0.055,
            "tenderness": 0.055,
            "reciprocity": 0.050,
            "fear": -0.035,
            "uncertainty": -0.025,
        },
    ),
    Prototype(
        key="high_desire_high_urgency",
        text=(
            "Я не можу терпіти, тіло дуже хоче, напруга висока, "
            "є ризик поспіху і тиску."
        ),
        scale_deltas={
            "desire": 0.060,
            "urgency": 0.070,
            "embodiment": 0.040,
            "safety": -0.025,
            "uncertainty": 0.020,
        },
    ),
    Prototype(
        key="trauma_threat_projection",
        text=(
            "Я боюся, підозрюю, очікую зради, читаю небезпеку там, "
            "де ще немає фактів."
        ),
        scale_deltas={
            "fear": 0.070,
            "uncertainty": 0.050,
            "clarity": -0.035,
            "safety": -0.035,
            "trust": -0.020,
        },
    ),
    Prototype(
        key="future_commitment",
        text=(
            "Я бачу майбутнє, дім, спільний шлях, довгу вірність, "
            "бажання будувати життя разом."
        ),
        scale_deltas={
            "future": 0.075,
            "trust": 0.035,
            "reverence": 0.055,
            "tenderness": 0.025,
        },
    ),
    Prototype(
        key="autonomy_and_consent",
        text=(
            "Я хочу тебе, але не хочу тиснути. Твоє так має бути вільним. "
            "Твоє ні зберігає любов."
        ),
        scale_deltas={
            "autonomy": 0.060,
            "safety": 0.055,
            "reciprocity": 0.050,
            "clarity": 0.030,
            "urgency": -0.035,
        },
    ),
    Prototype(
        key="repair_after_noise",
        text=(
            "Ми визнаємо помилку, говоримо прямо, не караємо мовчанням, "
            "повертаємося до тепла і факту."
        ),
        scale_deltas={
            "repair": 0.070,
            "trust": 0.035,
            "clarity": 0.045,
            "fear": -0.030,
        },
    ),
)


def initial_scales_for_yaroslav_dasha() -> Scales:
    return Scales(
        trust=0.62,
        desire=0.72,
        fear=0.42,
        safety=0.58,
        tenderness=0.66,
        reciprocity=0.54,
        clarity=0.56,
        future=0.76,
        urgency=0.56,
        uncertainty=0.48,
        embodiment=0.64,
        repair=0.52,
        autonomy=0.66,
        reverence=0.78,
    )
