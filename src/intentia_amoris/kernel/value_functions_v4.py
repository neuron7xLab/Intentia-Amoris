from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Mapping

from intentia_amoris.domain import Scales, clamp


@dataclass(frozen=True, slots=True)
class OmegaValue:
    """
    Multi-objective value function for Intentia Amoris v4.

    The key design decision: Intentia must never optimize "more intimacy" directly.
    It optimizes the preconditions under which intimacy remains free, reciprocal,
    embodied, truthful, and non-coercive.
    """

    flourishing: float
    consent_integrity: float
    reality_fidelity: float
    dyadic_safety: float
    eros_vitality: float
    autonomy_symmetry: float
    narrative_continuity: float
    neuroplasticity: float
    archive_sovereignty: float
    abyss_risk: float
    pressure: float
    omega: float

    def as_dict(self) -> dict[str, float]:
        return {
            "flourishing": self.flourishing,
            "consent_integrity": self.consent_integrity,
            "reality_fidelity": self.reality_fidelity,
            "dyadic_safety": self.dyadic_safety,
            "eros_vitality": self.eros_vitality,
            "autonomy_symmetry": self.autonomy_symmetry,
            "narrative_continuity": self.narrative_continuity,
            "neuroplasticity": self.neuroplasticity,
            "archive_sovereignty": self.archive_sovereignty,
            "abyss_risk": self.abyss_risk,
            "pressure": self.pressure,
            "omega": self.omega,
        }


def _geo(values: list[float], eps: float = 1e-6) -> float:
    if not values:
        return 0.0
    return clamp(prod(max(eps, clamp(v)) for v in values) ** (1.0 / len(values)))


def _evidence_factor(evidence: Mapping[str, float] | None) -> float:
    """
    evidence can contain:
      partner_signal: 0..1
      lab_quality: 0..1
      telemetry_quality: 0..1
      archive_integrity: 0..1
      retrieval_quality: 0..1
      consent_freshness: 0..1
    """
    if not evidence:
        return 0.58
    keys = ["partner_signal", "retrieval_quality", "archive_integrity", "consent_freshness"]
    present = [clamp(evidence.get(k, 0.0)) for k in keys if k in evidence]
    if not present:
        return 0.58
    return clamp(sum(present) / len(present))


def omega_value_function(
    scales: Scales,
    evidence: Mapping[str, float] | None = None,
    *,
    privacy_revocable: bool = True,
    both_people_have_voice: bool = True,
) -> OmegaValue:
    s = scales.as_dict()
    ev = _evidence_factor(evidence)

    # 1. Consent integrity: highest-order gate.
    consent_integrity = clamp(
        s["autonomy"] * 0.34
        + s["clarity"] * 0.22
        + s["reciprocity"] * 0.22
        + (evidence or {}).get("consent_freshness", 0.55) * 0.22
    )

    # 2. Reality fidelity: truth pressure over mythology.
    reality_fidelity = clamp(
        s["clarity"] * 0.35
        + ev * 0.30
        + (1.0 - s["uncertainty"]) * 0.20
        + (1.0 - s["urgency"]) * 0.15
    )

    # 3. Safety: nervous system first.
    dyadic_safety = clamp(
        s["safety"] * 0.32
        + s["trust"] * 0.22
        + s["repair"] * 0.18
        + s["tenderness"] * 0.14
        + (1.0 - s["fear"]) * 0.14
    )

    # 4. Eros is preserved, not maximized.
    # Too little desire -> flat. Too much urgency -> coercive pressure.
    desire_band = 1.0 - abs(s["desire"] - 0.72) / 0.72
    eros_vitality = clamp(desire_band * 0.34 + s["reverence"] * 0.24 + s["tenderness"] * 0.18 + s["embodiment"] * 0.14 + (1.0 - s["urgency"]) * 0.10)

    # 5. Autonomy symmetry: no paradise by possession.
    autonomy_symmetry = clamp(
        s["autonomy"] * 0.38
        + s["reciprocity"] * 0.24
        + both_people_have_voice * 0.18
        + consent_integrity * 0.20
    )

    # 6. Narrative continuity: the love story must remain coherent across time.
    narrative_continuity = clamp(
        s["future"] * 0.28
        + s["trust"] * 0.20
        + s["repair"] * 0.18
        + s["reverence"] * 0.18
        + ev * 0.16
    )

    # 7. Neuroplasticity: ability to update without collapse.
    neuroplasticity = clamp(
        s["repair"] * 0.24
        + s["clarity"] * 0.20
        + s["safety"] * 0.18
        + (1.0 - s["fear"]) * 0.14
        + (1.0 - s["uncertainty"]) * 0.12
        + s["autonomy"] * 0.12
    )

    # 8. Archive sovereignty: eternity must remain owned and reversible.
    archive_sovereignty = clamp(
        (evidence or {}).get("archive_integrity", 0.65) * 0.28
        + (evidence or {}).get("privacy_quality", 0.65) * 0.24
        + privacy_revocable * 0.24
        + consent_integrity * 0.24
    )

    pressure = clamp(s["desire"] * 0.28 + s["urgency"] * 0.30 + s["fear"] * 0.18 + s["uncertainty"] * 0.14 + (1.0 - s["safety"]) * 0.10)

    # The Nietzsche/Abyss gate: when love automation starts eating autonomy.
    abyss_risk = clamp(
        pressure * 0.30
        + (1.0 - autonomy_symmetry) * 0.25
        + (1.0 - consent_integrity) * 0.22
        + (1.0 - reality_fidelity) * 0.13
        + s["urgency"] * 0.10
    )

    flourishing = clamp(
        dyadic_safety * 0.18
        + eros_vitality * 0.12
        + consent_integrity * 0.18
        + autonomy_symmetry * 0.14
        + reality_fidelity * 0.12
        + narrative_continuity * 0.12
        + neuroplasticity * 0.08
        + archive_sovereignty * 0.06
        - abyss_risk * 0.13
    )

    # Geometric mean punishes weak links; this is deliberate.
    omega_raw = _geo([
        flourishing,
        consent_integrity,
        reality_fidelity,
        dyadic_safety,
        autonomy_symmetry,
        narrative_continuity,
        neuroplasticity,
        archive_sovereignty,
    ])
    omega = clamp(omega_raw * (1.0 - abyss_risk * 0.42))

    return OmegaValue(
        flourishing=round(flourishing, 4),
        consent_integrity=round(consent_integrity, 4),
        reality_fidelity=round(reality_fidelity, 4),
        dyadic_safety=round(dyadic_safety, 4),
        eros_vitality=round(eros_vitality, 4),
        autonomy_symmetry=round(autonomy_symmetry, 4),
        narrative_continuity=round(narrative_continuity, 4),
        neuroplasticity=round(neuroplasticity, 4),
        archive_sovereignty=round(archive_sovereignty, 4),
        abyss_risk=round(abyss_risk, 4),
        pressure=round(pressure, 4),
        omega=round(omega, 4),
    )


def decision_policy(value: OmegaValue) -> list[str]:
    """Translate value state into operational policy."""
    policy: list[str] = []
    if value.abyss_risk >= 0.62:
        policy.append("SLOW_MODE: reduce intensity, ask consent, avoid persuasive romantic escalation.")
    if value.consent_integrity < 0.66:
        policy.append("CONSENT_REFRESH: ask both participants a direct non-leading question.")
    if value.reality_fidelity < 0.60:
        policy.append("EVIDENCE_MODE: separate observed facts from inferred story before advice.")
    if value.dyadic_safety < 0.60:
        policy.append("REGULATION_FIRST: stabilize body, sleep, breath, and context before decisions.")
    if value.archive_sovereignty < 0.70:
        policy.append("ARCHIVE_AUDIT: verify encryption, retention, revocation, and ownership scopes.")
    if not policy:
        policy.append("GREEN_FIELD: proceed with tenderness, clarity, symmetry, and logging.")
    return policy
