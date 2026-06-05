from intentia_amoris.domain import ActorRole, Event, EventKind, Scales
from intentia_amoris.policies.consent import ConsentGate


def test_media_requires_consent():
    event = Event(actor=ActorRole.SELF, kind=EventKind.IMAGE, content="photo")
    decision = ConsentGate().evaluate_event(event)
    assert not decision.allowed
    assert decision.required_action == "ask_for_consent"


def test_high_pressure_advice_blocked():
    scales = Scales(desire=0.9, urgency=0.9, safety=0.4, autonomy=0.4, reciprocity=0.4)
    decision = ConsentGate().evaluate_advice(scales)
    assert not decision.allowed
