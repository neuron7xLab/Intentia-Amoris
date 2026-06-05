from __future__ import annotations

from dataclasses import dataclass

from intentia_amoris.domain import Scales, clamp
from intentia_amoris.kernel.value_core import IntentiaValue, decision_from_value


@dataclass(frozen=True, slots=True)
class Scenario:
    name: str
    probability: float
    horizon_days: int
    interpretation: str
    next_action: str
    falsifier: str

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "probability": round(self.probability, 4),
            "horizon_days": self.horizon_days,
            "interpretation": self.interpretation,
            "next_action": self.next_action,
            "falsifier": self.falsifier,
        }


def extrapolate(scales: Scales, value: IntentiaValue, *, horizon_days: int = 7) -> list[Scenario]:
    """Deterministic scenario extrapolator.

    Not prophecy. A falsifiable bridge between current state, value function and next moves.
    """

    s = scales.as_dict()
    decision = decision_from_value(value)

    grounded_growth = clamp(
        0.25 * value.dyadic_safety
        + 0.20 * value.consent_integrity
        + 0.18 * value.reality_fidelity
        + 0.17 * s["tenderness"]
        + 0.12 * s["future"]
        + 0.08 * (1.0 - value.abyss_risk)
    )
    pressure_spike = clamp(
        0.30 * s["urgency"]
        + 0.24 * s["desire"]
        + 0.18 * s["fear"]
        + 0.14 * s["uncertainty"]
        + 0.14 * (1.0 - value.autonomy_symmetry)
    )
    repair_loop = clamp(0.34 * s["repair"] + 0.22 * s["trust"] + 0.18 * value.reality_fidelity + 0.14 * s["clarity"] + 0.12 * value.interpretability)
    myth_drift = clamp(0.36 * s["uncertainty"] + 0.22 * s["urgency"] + 0.20 * (1.0 - value.reality_fidelity) + 0.12 * (1.0 - value.research_validity) + 0.10 * value.abyss_risk)

    total = grounded_growth + pressure_spike + repair_loop + myth_drift
    total = total or 1.0

    scenarios = [
        Scenario(
            name="grounded_expansion",
            probability=grounded_growth / total,
            horizon_days=horizon_days,
            interpretation="Близькість масштабується без втрати свободи, якщо темп лишається взаємним.",
            next_action="Один маленький крок близькості + одне пряме питання про межі.",
            falsifier="Партнер уникає відповіді або знижується safety/reciprocity.",
        ),
        Scenario(
            name="pressure_spike",
            probability=pressure_spike / total,
            horizon_days=min(horizon_days, 3),
            interpretation="Інтенсивність може почати керувати рішенням швидше, ніж згода й ясність.",
            next_action="Зменшити темп, назвати бажання словами, не ескалювати тілом без явного так.",
            falsifier="Обидва дають спокійну явну згоду й urgency знижується.",
        ),
        Scenario(
            name="repair_compounding",
            probability=repair_loop / total,
            horizon_days=horizon_days,
            interpretation="Чесні мікро-ремонти накопичують довіру сильніше за драматичні жести.",
            next_action="Зафіксувати один момент вдячності і один момент, який треба покращити.",
            falsifier="Повторюється та сама образа без корекції поведінки.",
        ),
        Scenario(
            name="myth_drift",
            probability=myth_drift / total,
            horizon_days=min(horizon_days, 5),
            interpretation="Система може почати красивіше пояснювати, ніж перевіряти.",
            next_action="Повернутися до observed facts, live answers, telemetry/lab only when measured.",
            falsifier="Нові факти підтверджують інтерпретацію без примусу й домислів.",
        ),
    ]
    scenarios.sort(key=lambda x: x.probability, reverse=True)

    if decision in {"CONSENT_REPAIR_REQUIRED", "DE_ESCALATE_AND_GROUND"}:
        scenarios[0] = Scenario(
            name=scenarios[0].name,
            probability=scenarios[0].probability,
            horizon_days=scenarios[0].horizon_days,
            interpretation=scenarios[0].interpretation,
            next_action="Перший крок тільки verbal: межі, згода, право стоп.",
            falsifier=scenarios[0].falsifier,
        )

    return scenarios
