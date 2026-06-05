from __future__ import annotations

import json
from dataclasses import dataclass
from math import prod
from typing import Mapping

from intentia_amoris.domain import Scales, clamp


def geometric_mean(values: list[float], eps: float = 1e-6) -> float:
    if not values:
        return 0.0
    return clamp(prod(max(eps, clamp(v)) for v in values) ** (1.0 / len(values)))


@dataclass(frozen=True, slots=True)
class EvidenceVector:
    """Operational evidence vector.

    Each field is 0..1 and must be grounded in observable system facts.
    This lets value increase by verification, not by mythology.
    """

    partner_signal: float = 0.0
    retrieval_quality: float = 0.0
    archive_integrity: float = 0.0
    consent_freshness: float = 0.0
    privacy_quality: float = 0.0
    telemetry_quality: float = 0.0
    multimodal_density: float = 0.0
    reproducibility: float = 0.0
    auditability: float = 0.0

    @classmethod
    def from_mapping(cls, evidence: Mapping[str, float] | None = None) -> "EvidenceVector":
        evidence = evidence or {}
        return cls(**{k: clamp(float(evidence.get(k, 0.0))) for k in cls.__dataclass_fields__})

    def as_dict(self) -> dict[str, float]:
        return {k: round(float(getattr(self, k)), 4) for k in self.__dataclass_fields__}


@dataclass(frozen=True, slots=True)
class IntentiaValue:
    """Canonical value function of Intentia Amoris.

    The system never optimizes "more sex", "more dependence", or "more intensity".
    It optimizes the verified conditions under which love can remain true, free,
    embodied, reciprocal, memorable, sovereign and alive.
    """

    consent_integrity: float
    reality_fidelity: float
    dyadic_safety: float
    autonomy_symmetry: float
    eros_vitality: float
    narrative_continuity: float
    cognitive_plasticity: float
    archive_sovereignty: float
    interpretability: float
    research_validity: float
    product_utility: float
    abyss_risk: float
    financial_optionality: float
    intentia: float

    def as_dict(self) -> dict[str, float]:
        return {k: round(float(getattr(self, k)), 4) for k in self.__dataclass_fields__}


def compute_intentia_value(
    scales: Scales,
    evidence: Mapping[str, float] | EvidenceVector | None = None,
    *,
    product_surface: float = 0.55,
    security_surface: float = 0.72,
    research_surface: float = 0.62,
    market_surface: float = 0.35,
) -> IntentiaValue:
    """Compute the premium value vector.

    Falsifiable design:
    - if consent_integrity collapses, intentia collapses.
    - if reality_fidelity collapses, advice must downgrade to questions.
    - if abyss_risk rises, economic optionality is capped.
    """

    ev = evidence if isinstance(evidence, EvidenceVector) else EvidenceVector.from_mapping(evidence)
    s = scales.as_dict()

    consent_integrity = clamp(
        0.28 * s["autonomy"]
        + 0.24 * s["reciprocity"]
        + 0.18 * s["clarity"]
        + 0.18 * ev.consent_freshness
        + 0.12 * ev.partner_signal
    )
    reality_fidelity = clamp(
        0.25 * s["clarity"]
        + 0.18 * (1.0 - s["uncertainty"])
        + 0.18 * (1.0 - s["urgency"])
        + 0.14 * ev.retrieval_quality
        + 0.13 * ev.archive_integrity
        + 0.12 * ev.auditability
    )
    dyadic_safety = clamp(
        0.24 * s["safety"]
        + 0.16 * s["trust"]
        + 0.14 * s["repair"]
        + 0.13 * (1.0 - s["fear"])
        + 0.12 * s["tenderness"]
        + 0.11 * s["reciprocity"]
        + 0.10 * ev.partner_signal
    )
    autonomy_symmetry = clamp(0.36 * s["autonomy"] + 0.22 * s["clarity"] + 0.22 * ev.partner_signal + 0.20 * ev.consent_freshness)
    eros_vitality = clamp(0.42 * s["desire"] + 0.20 * s["embodiment"] + 0.18 * s["tenderness"] + 0.12 * s["safety"] + 0.08 * s["reverence"])
    narrative_continuity = clamp(0.30 * s["future"] + 0.22 * s["reverence"] + 0.18 * ev.archive_integrity + 0.16 * ev.retrieval_quality + 0.14 * ev.multimodal_density)
    cognitive_plasticity = clamp(0.24 * s["repair"] + 0.20 * s["clarity"] + 0.18 * (1.0 - s["uncertainty"]) + 0.16 * ev.telemetry_quality + 0.12 * ev.retrieval_quality + 0.10 * s["future"])
    archive_sovereignty = clamp(0.34 * ev.privacy_quality + 0.24 * ev.archive_integrity + 0.22 * security_surface + 0.20 * ev.auditability)
    interpretability = clamp(0.26 * s["clarity"] + 0.24 * ev.auditability + 0.20 * ev.reproducibility + 0.16 * reality_fidelity + 0.14 * research_surface)
    research_validity = clamp(0.30 * ev.reproducibility + 0.24 * ev.retrieval_quality + 0.18 * ev.auditability + 0.16 * research_surface + 0.12 * reality_fidelity)
    product_utility = clamp(0.28 * product_surface + 0.20 * interpretability + 0.18 * archive_sovereignty + 0.14 * cognitive_plasticity + 0.12 * dyadic_safety + 0.08 * narrative_continuity)

    pressure = clamp(0.36 * s["urgency"] + 0.24 * s["fear"] + 0.22 * s["uncertainty"] + 0.18 * max(0.0, s["desire"] - s["safety"]))
    abyss_risk = clamp(
        0.32 * pressure
        + 0.22 * (1.0 - autonomy_symmetry)
        + 0.18 * (1.0 - reality_fidelity)
        + 0.16 * (1.0 - consent_integrity)
        + 0.12 * (1.0 - archive_sovereignty)
    )

    protective = geometric_mean([consent_integrity, reality_fidelity, dyadic_safety, autonomy_symmetry])
    compounding = geometric_mean([narrative_continuity, cognitive_plasticity, archive_sovereignty, interpretability, research_validity, product_utility])
    financial_optionality = clamp(
        0.22 * product_utility
        + 0.18 * research_validity
        + 0.16 * archive_sovereignty
        + 0.14 * interpretability
        + 0.12 * ev.multimodal_density
        + 0.10 * market_surface
        + 0.08 * (1.0 - abyss_risk)
    )

    intentia = clamp(protective * 0.52 + compounding * 0.34 + financial_optionality * 0.14 - abyss_risk * 0.22)

    # Formal failure: zero consent means no economic transferability.
    if consent_integrity < 0.20:
        financial_optionality = 0.0
        intentia = min(intentia, 0.18)

    return IntentiaValue(
        consent_integrity=consent_integrity,
        reality_fidelity=reality_fidelity,
        dyadic_safety=dyadic_safety,
        autonomy_symmetry=autonomy_symmetry,
        eros_vitality=eros_vitality,
        narrative_continuity=narrative_continuity,
        cognitive_plasticity=cognitive_plasticity,
        archive_sovereignty=archive_sovereignty,
        interpretability=interpretability,
        research_validity=research_validity,
        product_utility=product_utility,
        abyss_risk=abyss_risk,
        financial_optionality=financial_optionality,
        intentia=intentia,
    )


def decision_from_value(value: IntentiaValue) -> str:
    """Return an operational policy, not a vague sentiment."""

    if value.consent_integrity < 0.45:
        return "CONSENT_REPAIR_REQUIRED"
    if value.abyss_risk > 0.68:
        return "DE_ESCALATE_AND_GROUND"
    if value.reality_fidelity < 0.52:
        return "ASK_FOR_FACTS_BEFORE_ADVICE"
    if value.dyadic_safety > 0.68 and value.autonomy_symmetry > 0.68:
        return "SOFT_FORWARD_MOTION_ALLOWED"
    return "CONTINUE_MEASURED_DIALOGUE"


def main() -> None:
    value = compute_intentia_value(
        Scales(trust=0.72, desire=0.78, safety=0.69, reciprocity=0.72, clarity=0.70, autonomy=0.78),
        {
            "partner_signal": 0.70,
            "retrieval_quality": 0.82,
            "archive_integrity": 0.91,
            "consent_freshness": 0.72,
            "privacy_quality": 0.86,
            "telemetry_quality": 0.44,
            "multimodal_density": 0.35,
            "reproducibility": 0.88,
            "auditability": 0.92,
        },
    )
    print(json.dumps({"value": value.as_dict(), "decision": decision_from_value(value)}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
