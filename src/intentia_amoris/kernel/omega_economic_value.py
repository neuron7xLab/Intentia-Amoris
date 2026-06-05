from __future__ import annotations

from dataclasses import dataclass
from math import prod


@dataclass(frozen=True, slots=True)
class ReplacementCostInput:
    architecture_hours: float = 120
    backend_hours: float = 180
    data_pipeline_hours: float = 120
    research_docs_hours: float = 100
    security_ops_hours: float = 80
    hourly_rate_usd: float = 85
    overhead_multiplier: float = 1.25

    @property
    def total_hours(self) -> float:
        return (
            self.architecture_hours
            + self.backend_hours
            + self.data_pipeline_hours
            + self.research_docs_hours
            + self.security_ops_hours
        )


@dataclass(frozen=True, slots=True)
class SaaSScenario:
    couples: int
    price_per_couple_month_usd: float
    gross_margin: float = 0.80
    retention_factor: float = 0.85
    revenue_multiple_low: float = 3.1
    revenue_multiple_base: float = 4.5
    revenue_multiple_high: float = 8.1

    @property
    def arr(self) -> float:
        return self.couples * self.price_per_couple_month_usd * 12

    @property
    def risk_adjusted_arr(self) -> float:
        return self.arr * self.gross_margin * self.retention_factor

    def multiple_values(self) -> dict[str, float]:
        base = self.risk_adjusted_arr
        return {
            "low": round(base * self.revenue_multiple_low, 2),
            "base": round(base * self.revenue_multiple_base, 2),
            "high": round(base * self.revenue_multiple_high, 2),
        }


@dataclass(frozen=True, slots=True)
class OmegaAssetScore:
    consent_integrity: float
    reality_fidelity: float
    dyadic_safety: float
    archive_sovereignty: float
    originality: float
    execution_quality: float
    market_transferability: float
    abyss_risk: float

    def score(self) -> float:
        positive = [
            self.consent_integrity,
            self.reality_fidelity,
            self.dyadic_safety,
            self.archive_sovereignty,
            self.originality,
            self.execution_quality,
            self.market_transferability,
        ]
        geometric = prod(max(0.001, x) for x in positive) ** (1 / len(positive))
        return round(max(0.0, min(1.0, geometric * (1.0 - self.abyss_risk))), 4)


def replacement_cost_usd(inp: ReplacementCostInput) -> float:
    return round(inp.total_hours * inp.hourly_rate_usd * inp.overhead_multiplier, 2)


def dcf_npv(cashflows: list[float], discount_rate: float, terminal_value: float = 0.0) -> float:
    total = 0.0
    for idx, cf in enumerate(cashflows, start=1):
        total += cf / ((1.0 + discount_rate) ** idx)
    if terminal_value:
        total += terminal_value / ((1.0 + discount_rate) ** len(cashflows))
    return round(total, 2)


def relief_from_royalty(
    annual_revenue: float,
    royalty_rate: float,
    tax_rate: float,
    discount_rate: float,
    years: int,
    terminal_growth: float = 0.0,
) -> float:
    after_tax_royalty = annual_revenue * royalty_rate * (1.0 - tax_rate)
    cashflows = [after_tax_royalty for _ in range(years)]
    terminal = 0.0
    if terminal_growth < discount_rate:
        terminal = after_tax_royalty * (1.0 + terminal_growth) / (discount_rate - terminal_growth)
    return dcf_npv(cashflows, discount_rate, terminal)


def usd_to_uah(amount_usd: float, rate: float = 44.3793) -> float:
    return round(amount_usd * rate, 2)


def default_2026_valuation() -> dict[str, object]:
    prototype_cost = replacement_cost_usd(ReplacementCostInput(hourly_rate_usd=70, overhead_multiplier=1.15))
    production_cost = replacement_cost_usd(ReplacementCostInput(hourly_rate_usd=110, overhead_multiplier=1.35))
    scenarios = {
        "100_couples": SaaSScenario(couples=100, price_per_couple_month_usd=19).multiple_values(),
        "1000_couples": SaaSScenario(couples=1000, price_per_couple_month_usd=19).multiple_values(),
        "10000_couples": SaaSScenario(couples=10000, price_per_couple_month_usd=19).multiple_values(),
    }
    score = OmegaAssetScore(
        consent_integrity=0.86,
        reality_fidelity=0.82,
        dyadic_safety=0.78,
        archive_sovereignty=0.70,
        originality=0.93,
        execution_quality=0.68,
        market_transferability=0.42,
        abyss_risk=0.24,
    ).score()
    return {
        "replacement_cost_private_usd": prototype_cost,
        "replacement_cost_production_usd": production_cost,
        "omega_asset_score": score,
        "saas_scenarios_usd": scenarios,
        "uah_rate": 44.3793,
        "note": "Private love data is not transferable without active consent; market value is not the same as sacred value.",
    }
