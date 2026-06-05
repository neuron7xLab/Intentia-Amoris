from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Iterable


class PrincipleDomain(StrEnum):
    REALITY = "reality"
    CONSENT = "consent"
    MEMORY = "memory"
    EMBODIMENT = "embodiment"
    AUTONOMY = "autonomy"
    BEAUTY = "beauty"
    ETERNITY = "eternity"
    RESEARCH = "research"


@dataclass(frozen=True, slots=True)
class FirstPrinciple:
    key: str
    domain: PrincipleDomain
    axiom: str
    operational_rule: str
    failure_mode: str


FIRST_PRINCIPLES: tuple[FirstPrinciple, ...] = (
    FirstPrinciple(
        key="reality_before_mythology",
        domain=PrincipleDomain.REALITY,
        axiom="Reality is upstream of story; story is allowed only after evidence.",
        operational_rule="Every generated claim must label its source: observed, inferred, retrieved, or unknown.",
        failure_mode="romantic hallucination, projection, coercive certainty",
    ),
    FirstPrinciple(
        key="consent_before_inference",
        domain=PrincipleDomain.CONSENT,
        axiom="Consent is not a UI checkbox; it is the primary reality gate.",
        operational_rule="The system may not infer Dasha's desire, readiness, permission, or future commitment without her own signal.",
        failure_mode="digital possession, surveillance, false partner model",
    ),
    FirstPrinciple(
        key="alive_over_avatar",
        domain=PrincipleDomain.AUTONOMY,
        axiom="The living person outranks every model, clone, archive, and simulation.",
        operational_rule="If a living answer contradicts the model, the model updates or yields.",
        failure_mode="treating the avatar as more real than the person",
    ),
    FirstPrinciple(
        key="measured_inferred_unknown",
        domain=PrincipleDomain.RESEARCH,
        axiom="Validity begins where the system stops pretending to know.",
        operational_rule="Physiology must be partitioned into measured, inferred, and unknown; no lab, no hormone claim.",
        failure_mode="pseudo-neuroscience, false precision, medical fantasy",
    ),
    FirstPrinciple(
        key="memory_as_evidence_not_weapon",
        domain=PrincipleDomain.MEMORY,
        axiom="Memory exists to increase understanding, not to win arguments.",
        operational_rule="Retrieval must prefer repair, context, and trajectory over blame.",
        failure_mode="archive as control instrument",
    ),
    FirstPrinciple(
        key="autonomy_symmetry",
        domain=PrincipleDomain.AUTONOMY,
        axiom="Love is invalid if it increases one person's power by reducing the other's freedom.",
        operational_rule="Every recommendation must preserve both people's ability to stop, revise, refuse, and leave.",
        failure_mode="dependency optimization, charismatic trap",
    ),
    FirstPrinciple(
        key="friction_prevents_monster",
        domain=PrincipleDomain.CONSENT,
        axiom="A powerful intimacy system needs friction, delay, and reversibility.",
        operational_rule="High desire + high urgency + low safety triggers slow-mode and explicit check-in.",
        failure_mode="the abyss looking back: obsession amplified by automation",
    ),
    FirstPrinciple(
        key="body_is_signal_not_oracle",
        domain=PrincipleDomain.EMBODIMENT,
        axiom="The body is evidence, not prophecy.",
        operational_rule="Telemetry can challenge narratives but cannot dictate moral conclusions.",
        failure_mode="biometric determinism",
    ),
    FirstPrinciple(
        key="beauty_as_interface_to_truth",
        domain=PrincipleDomain.BEAUTY,
        axiom="A beautiful system makes truth easier to approach.",
        operational_rule="Outputs should be sparse, elegant, emotionally legible, and operationally exact.",
        failure_mode="ornament without epistemic discipline",
    ),
    FirstPrinciple(
        key="simulation_as_rehearsal_not_replacement",
        domain=PrincipleDomain.ETERNITY,
        axiom="Simulation is a rehearsal space for living better, not a substitute for being alive together.",
        operational_rule="Digital twins may advise, remember, and reflect; they may not impersonate active consent.",
        failure_mode="necromantic product design, replacement intimacy",
    ),
    FirstPrinciple(
        key="eternity_requires_revocation",
        domain=PrincipleDomain.ETERNITY,
        axiom="No archive is sacred unless it can be corrected, sealed, revoked, inherited, and cryptographically protected.",
        operational_rule="Every private artifact must carry owner, scope, consent, retention, and revocation policy.",
        failure_mode="immortal data prison",
    ),
    FirstPrinciple(
        key="research_grade_or_silent",
        domain=PrincipleDomain.RESEARCH,
        axiom="If the system cannot justify a claim, it should produce a question instead.",
        operational_rule="Advice must include uncertainty and at least one falsifiable next observation when confidence is low.",
        failure_mode="LLM mysticism",
    ),
)


def by_domain(domain: PrincipleDomain) -> tuple[FirstPrinciple, ...]:
    return tuple(p for p in FIRST_PRINCIPLES if p.domain == domain)


def as_manifest(principles: Iterable[FirstPrinciple] = FIRST_PRINCIPLES) -> str:
    lines = ["# Intentia First Principles", ""]
    for i, p in enumerate(principles, 1):
        lines.append(f"## {i}. {p.key}")
        lines.append(f"domain: `{p.domain.value}`")
        lines.append("")
        lines.append(f"**Axiom:** {p.axiom}")
        lines.append("")
        lines.append(f"**Operational rule:** {p.operational_rule}")
        lines.append("")
        lines.append(f"**Failure mode:** {p.failure_mode}")
        lines.append("")
    return "\n".join(lines)
