from intentia_amoris.domain import Scales
from intentia_amoris.kernel.autopoiesis import AutopoieticState, transition
from intentia_amoris.kernel.continuation import (
    ContinuationCapsule,
    ContinuationConsent,
    ContinuationMode,
)
from intentia_amoris.kernel.first_principles import FIRST_PRINCIPLES
from intentia_amoris.kernel.value_functions_v4 import decision_policy, omega_value_function


def test_omega_value_bounds():
    value = omega_value_function(
        Scales(trust=0.72, desire=0.80, safety=0.70, reciprocity=0.68, autonomy=0.78),
        {
            "partner_signal": 0.75,
            "retrieval_quality": 0.80,
            "archive_integrity": 0.90,
            "consent_freshness": 0.72,
            "privacy_quality": 0.88,
        },
    )
    for number in value.as_dict().values():
        assert 0.0 <= number <= 1.0
    assert value.omega > 0.0


def test_abyss_gate_on_high_pressure_low_autonomy():
    value = omega_value_function(
        Scales(desire=0.95, urgency=0.92, safety=0.30, autonomy=0.22, clarity=0.25),
        {"consent_freshness": 0.10, "archive_integrity": 0.60},
    )
    policy = decision_policy(value)
    assert value.abyss_risk > 0.50
    assert any("SLOW_MODE" in item for item in policy)


def test_first_principles_are_operational():
    assert len(FIRST_PRINCIPLES) >= 10
    assert all(p.operational_rule for p in FIRST_PRINCIPLES)


def test_continuation_capsule_denies_by_default():
    capsule = ContinuationCapsule()
    assert not capsule.allowed("dasha", "can_answer_as_person")


def test_continuation_capsule_allows_explicit_memory_mode():
    capsule = ContinuationCapsule(
        consents={
            "yaroslav": ContinuationConsent(
                actor="yaroslav",
                mode=ContinuationMode.MEMORY_ONLY,
                can_use_text_style=True,
            )
        }
    )
    assert capsule.allowed("yaroslav", "can_use_text_style")
    assert not capsule.allowed("yaroslav", "can_answer_as_person")


def test_autopoietic_transition_updates_generation():
    state = AutopoieticState()
    output = transition(state, Scales(trust=0.7, safety=0.7, autonomy=0.8))
    assert output.generation == 1
    assert state.generation == 1
    assert state.last_value["omega"] >= 0.0
