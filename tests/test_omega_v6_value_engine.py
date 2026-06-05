from intentia_amoris.kernel.value_engine_v6 import OmegaVector, compute_omega_score, uplift_actions
from intentia_amoris.finance.valuation_model import build_report, value_repo, target_scenarios, required_paying_pairs
from intentia_amoris.research.falsification import build_falsification_report


def sample_metrics():
    return {
        "total_events": 1000,
        "text_events": 882,
        "media_events": 117,
        "actors": {"self": 544, "partner": 456},
        "reactions": {"❤": 107, "🔥": 17},
        "feature_counts": {"eros": 57, "boundary": 25, "affection": 23, "future_story": 6},
    }


def test_omega_vector_from_metrics_bounds():
    vector = OmegaVector.from_metrics(sample_metrics())
    for value in vector.as_dict().values():
        assert 0 <= value <= 1


def test_omega_score_is_computable():
    vector = OmegaVector.from_metrics(sample_metrics())
    score = compute_omega_score(vector)
    assert 0 <= score.omega <= 1
    assert 0 <= score.investability <= 1
    assert score.research_validity > 0


def test_valuation_band_monotonic():
    score = compute_omega_score(OmegaVector.from_metrics(sample_metrics()))
    band = value_repo(score)
    assert band.floor > 0
    assert band.base >= band.floor
    assert band.ambition >= band.base
    assert band.sovereign >= band.ambition


def test_build_report_contains_gates():
    report = build_report(sample_metrics())
    assert report["valuation_band"]["sovereign_usd"] > report["valuation_band"]["floor_usd"]
    assert report["gates_to_23m_plus"]


def test_uplift_actions_ordered():
    actions = uplift_actions(OmegaVector.from_metrics(sample_metrics()))
    assert actions
    assert "dimension" in actions[0]


def test_falsification_report_has_forbidden_claims():
    report = build_falsification_report()
    assert report["hypotheses"]
    assert report["claim_boundary"]["cannot_claim_without_evidence"]


def test_target_scenarios_23m_have_required_pairs():
    scenarios = target_scenarios(23_000_000)
    assert scenarios
    assert required_paying_pairs(23_000_000, 99, 10) > 0
    assert min(s["required_paying_pairs"] for s in scenarios) < max(s["required_paying_pairs"] for s in scenarios)
