from __future__ import annotations

from dataclasses import dataclass

from intentia_amoris.domain import ActorRole, Event, EventKind, PrivacyScope, Scales


@dataclass(frozen=True, slots=True)
class ConsentDecision:
    allowed: bool
    reasons: list[str]
    required_action: str | None = None


class ConsentGate:
    def evaluate_event(self, event: Event) -> ConsentDecision:
        reasons: list[str] = []

        if event.actor == ActorRole.PARTNER and event.privacy_scope == PrivacyScope.SELF_PRIVATE:
            reasons.append("partner event cannot be stored in self_private scope")

        if event.kind in {EventKind.IMAGE, EventKind.AUDIO, EventKind.VIDEO}:
            if not event.metadata.get("consent_confirmed", False):
                reasons.append("media requires explicit consent_confirmed=true")

        if reasons:
            return ConsentDecision(False, reasons, "ask_for_consent")
        return ConsentDecision(True, [])

    def evaluate_advice(self, scales: Scales) -> ConsentDecision:
        reasons: list[str] = []
        if scales.desire > 0.70 and scales.urgency > 0.62 and scales.safety < 0.62:
            reasons.append("high desire + urgency without enough safety")
        if scales.autonomy < 0.55:
            reasons.append("autonomy scale too low for escalation")
        if scales.reciprocity < 0.55:
            reasons.append("reciprocity is not established enough")

        if reasons:
            return ConsentDecision(False, reasons, "slow_down_and_ask")
        return ConsentDecision(True, [])
