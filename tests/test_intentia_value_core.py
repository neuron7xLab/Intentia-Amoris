from intentia_amoris.domain import Scales
from intentia_amoris.kernel.extrapolation import extrapolate
from intentia_amoris.kernel.principia import PRINCIPIA, hard_invariants
from intentia_amoris.kernel.value_core import compute_intentia_value, decision_from_value


def test_intentia_value_has_collapse_rule_for_low_consent():
    low = compute_intentia_value(
        Scales(autonomy=0.0, reciprocity=0.0, clarity=0.0),
        {"consent_freshness": 0.0, "partner_signal": 0.0},
    )
    assert low.financial_optionality == 0.0
    assert low.intentia <= 0.18


def test_intentia_value_rewards_verified_safe_conditions():
    value = compute_intentia_value(
        Scales(
            trust=0.8,
            desire=0.72,
            safety=0.8,
            reciprocity=0.78,
            clarity=0.76,
            autonomy=0.82,
            repair=0.72,
            future=0.78,
            reverence=0.74,
        ),
        {
            "partner_signal": 0.78,
            "retrieval_quality": 0.86,
            "archive_integrity": 0.90,
            "consent_freshness": 0.84,
            "privacy_quality": 0.88,
            "telemetry_quality": 0.60,
            "multimodal_density": 0.42,
            "reproducibility": 0.90,
            "auditability": 0.92,
        },
    )
    assert value.intentia > 0.50
    assert value.consent_integrity > 0.70
    assert decision_from_value(value) in {
        "SOFT_FORWARD_MOTION_ALLOWED",
        "CONTINUE_MEASURED_DIALOGUE",
    }


def test_extrapolation_outputs_falsifiable_scenarios():
    scales = Scales(desire=0.8, urgency=0.7, safety=0.48, uncertainty=0.64)
    value = compute_intentia_value(scales, {"auditability": 0.9, "privacy_quality": 0.8})
    scenarios = extrapolate(scales, value)
    assert len(scenarios) == 4
    assert all(s.falsifier for s in scenarios)
    assert abs(sum(s.probability for s in scenarios) - 1.0) < 1e-6


def test_principia_has_hard_invariants():
    assert len(PRINCIPIA) >= 8
    keys = {p.key for p in hard_invariants()}
    assert "consent_as_computation_gate" in keys
    assert "living_over_digital" in keys
    assert "eternity_requires_exit" in keys
