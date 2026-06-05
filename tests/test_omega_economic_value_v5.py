from intentia_amoris.kernel.omega_economic_value import (
    ReplacementCostInput,
    SaaSScenario,
    dcf_npv,
    default_2026_valuation,
    replacement_cost_usd,
    relief_from_royalty,
    usd_to_uah,
)


def test_replacement_cost_is_positive():
    assert replacement_cost_usd(ReplacementCostInput(hourly_rate_usd=70)) > 0


def test_saas_scenario_values_ordered():
    values = SaaSScenario(couples=1000, price_per_couple_month_usd=19).multiple_values()
    assert values["low"] < values["base"] < values["high"]


def test_dcf_discounting():
    assert dcf_npv([100, 100], 0.10) < 200


def test_relief_from_royalty_positive():
    assert relief_from_royalty(100000, 0.05, 0.20, 0.25, 5) > 0


def test_usd_to_uah():
    assert usd_to_uah(1, 44.3793) == 44.38


def test_default_valuation_shape():
    v = default_2026_valuation()
    assert v["omega_asset_score"] > 0
    assert "1000_couples" in v["saas_scenarios_usd"]
