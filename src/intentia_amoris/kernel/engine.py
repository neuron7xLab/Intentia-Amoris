from __future__ import annotations

from intentia_amoris.domain import ActorRole, Event, EventKind, Scales, Telemetry
from intentia_amoris.kernel.agents import advice, duet, questions
from intentia_amoris.kernel.embeddings import EmbeddingProvider
from intentia_amoris.kernel.extrapolation import extrapolate
from intentia_amoris.kernel.scales import DynamicScalesKernel, value_function
from intentia_amoris.kernel.value_core import compute_intentia_value, decision_from_value
from intentia_amoris.kernel.value_functions_v4 import decision_policy, omega_value_function
from intentia_amoris.policies.consent import ConsentGate


class IntentiaAmorisEngine:
    """Operational cognitive engine.

    Pipeline:
    event → consent gate → vector scale update → value function → scenario extrapolation
    → duet/questions/advice → auditable result.
    """

    def __init__(self, embedding_provider: EmbeddingProvider) -> None:
        self.embedding_provider = embedding_provider
        self.scale_kernel = DynamicScalesKernel(embedding_provider)

    async def process_event(self, current: Scales, event: Event, retrieved: list[str]) -> dict:
        gate = ConsentGate().evaluate_event(event)
        if not gate.allowed:
            return {
                "blocked": True,
                "reasons": gate.reasons,
                "required_action": gate.required_action,
                "scales": current.as_dict(),
                "policy": "CONSENT_GATE_BLOCKED",
            }

        update = await self.scale_kernel.update(current, event.content)

        evidence = {
            "partner_signal": 0.64 if event.actor == ActorRole.PARTNER else 0.0,
            "retrieval_quality": min(1.0, len(retrieved) / 3.0),
            "archive_integrity": 0.88,
            "privacy_quality": 0.82,
            "consent_freshness": 0.62,
            "telemetry_quality": 0.55 if event.kind == EventKind.TELEMETRY else 0.25,
            "multimodal_density": 0.60 if event.kind in {EventKind.IMAGE, EventKind.AUDIO, EventKind.VIDEO} else 0.20,
            "reproducibility": 0.84,
            "auditability": 0.90,
        }

        vf = value_function(update.new_scales)
        intentia_value = compute_intentia_value(update.new_scales, evidence)
        omega = omega_value_function(update.new_scales, evidence)
        scenarios = extrapolate(update.new_scales, intentia_value)

        uncertainty = [
            "почуття партнера не стверджуються без відповіді партнера",
            "гормони не стверджуються без лабораторного вимірювання",
            "модель є картою, не самою реальністю",
        ]
        if event.kind in {EventKind.IMAGE, EventKind.AUDIO, EventKind.VIDEO}:
            uncertainty.append("мультимодальний опис є інтерпретацією, не фактом наміру")
        if intentia_value.reality_fidelity < 0.55:
            uncertainty.append("низька reality_fidelity: порада має бути питанням, а не твердженням")

        return {
            "blocked": False,
            "observed_facts": [
                f"actor={event.actor.value}",
                f"kind={event.kind.value}",
                f"source={event.source}",
                f"privacy_scope={event.privacy_scope.value}",
            ],
            "retrieved_memories": retrieved[:3],
            "inferred_states": update.signals,
            "prototype_hits": update.prototype_hits,
            "uncertainty": uncertainty,
            "duet": duet(update.new_scales),
            "questions": questions(update.new_scales),
            "advice": advice(update.new_scales, retrieved),
            "scales": update.new_scales.as_dict(),
            "value_function": vf,
            "intentia_value": intentia_value.as_dict(),
            "intentia_policy": decision_from_value(intentia_value),
            "scenario_extrapolation": [s.as_dict() for s in scenarios],
            "omega_value": omega.as_dict(),
            "omega_policy": decision_policy(omega),
        }

    async def telemetry_to_event(self, telemetry: Telemetry) -> Event:
        fragments = [f"{k}={v}" for k, v in sorted(telemetry.metrics.items())]
        if telemetry.raw_mood:
            fragments.append(f"raw_mood={telemetry.raw_mood}")
        content = "telemetry " + " ".join(fragments)
        return Event(
            actor=telemetry.actor,
            kind=EventKind.TELEMETRY,
            content=content,
            source=telemetry.source,
            confidence=0.85,
            metadata={"metrics": telemetry.metrics, "raw_mood": telemetry.raw_mood},
        )


# Backward-compatible alias for older tests/imports from the ARIS lineage.
IntentiaEternityEngine = IntentiaAmorisEngine
ARISEternityEngine = IntentiaAmorisEngine
