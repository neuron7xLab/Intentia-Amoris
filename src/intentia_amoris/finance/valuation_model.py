from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from intentia_amoris.kernel.value_engine_v6 import OmegaVector, compute_omega_score, uplift_actions


@dataclass(frozen=True, slots=True)
class ValuationInputs:
    rebuild_cost_usd: float = 180_000.0
    arr_usd: float = 0.0
    arr_multiple: float = 7.0
    royalty_rate: float = 0.08
    addressable_pairs: int = 10_000
    price_per_pair_month: float = 29.0
    adoption_probability: float = 0.06
    gross_margin: float = 0.82
    discount_rate: float = 0.35
    technical_readiness: float = 0.45
    consent_transferability: float = 0.55


@dataclass(frozen=True, slots=True)
class ValuationBand:
    floor: float
    base: float
    ambition: float
    sovereign: float

    def as_dict(self) -> dict[str, float]:
        return {
            "floor_usd": round(self.floor, 2),
            "base_usd": round(self.base, 2),
            "ambition_usd": round(self.ambition, 2),
            "sovereign_usd": round(self.sovereign, 2),
        }


def dcf_value(
    pairs: int,
    price_month: float,
    adoption_probability: float,
    gross_margin: float,
    discount_rate: float,
    years: int = 5,
    growth: float = 0.65,
) -> float:
    users = pairs * adoption_probability
    annual_revenue = users * price_month * 12
    value = 0.0
    for year in range(1, years + 1):
        revenue = annual_revenue * ((1 + growth) ** (year - 1))
        cash = revenue * gross_margin * 0.28
        value += cash / ((1 + discount_rate) ** year)
    terminal = annual_revenue * ((1 + growth) ** years) * gross_margin * 0.28 * 5.0
    value += terminal / ((1 + discount_rate) ** years)
    return value


def value_repo(score, inputs: ValuationInputs = ValuationInputs()) -> ValuationBand:
    """Compute a reasoning-based valuation band.

    floor: replacement cost adjusted by technical readiness and reproducibility
    base: floor plus option value from product/research defensibility
    ambition: income/ARR style value once pilot traction exists
    sovereign: category-level value if the repo becomes a defensible Relationship Intelligence OS
    """

    reproducibility = score.vector.reproducibility
    product = score.vector.product_surface
    research = score.research_validity
    defensibility = score.defensibility
    consent = inputs.consent_transferability * score.vector.consent_integrity

    floor = inputs.rebuild_cost_usd * (0.60 + 0.55 * score.research_validity + 0.35 * reproducibility) * consent

    option_dcf = dcf_value(
        pairs=inputs.addressable_pairs,
        price_month=inputs.price_per_pair_month,
        adoption_probability=inputs.adoption_probability,
        gross_margin=inputs.gross_margin,
        discount_rate=inputs.discount_rate,
    )
    base = floor + option_dcf * (0.20 * product + 0.28 * research + 0.22 * defensibility) * consent

    implied_arr = (
        inputs.addressable_pairs
        * inputs.adoption_probability
        * inputs.price_per_pair_month
        * 12
    )
    arr_value = implied_arr * inputs.arr_multiple * (0.40 + 0.50 * score.investability) * consent
    ambition = max(base * 2.4, arr_value + floor)

    sovereign = ambition * (1.6 + 2.4 * score.defensibility + 1.7 * score.eternity_readiness)

    return ValuationBand(floor=floor, base=base, ambition=ambition, sovereign=sovereign)


def load_metrics(path: Path | None = None) -> dict:
    if path is None:
        path = Path("data/derived/telegram/parousia_metrics.json")
    return json.loads(path.read_text(encoding="utf-8"))



def required_arr_for_target(target_usd: float, arr_multiple: float) -> float:
    if arr_multiple <= 0:
        raise ValueError("arr_multiple must be positive")
    return target_usd / arr_multiple


def required_paying_pairs(target_usd: float, price_per_pair_month: float, arr_multiple: float) -> int:
    arr = required_arr_for_target(target_usd, arr_multiple)
    annual_per_pair = price_per_pair_month * 12
    if annual_per_pair <= 0:
        raise ValueError("price_per_pair_month must be positive")
    return int(arr / annual_per_pair) + 1


def target_scenarios(target_usd: float = 23_000_000.0) -> list[dict[str, float | int | str]]:
    scenarios = []
    for price in (19.0, 29.0, 49.0, 99.0, 249.0):
        for multiple in (5.0, 7.0, 10.0, 12.0):
            scenarios.append(
                {
                    "model": "ARR_multiple",
                    "target_usd": target_usd,
                    "price_per_pair_month": price,
                    "arr_multiple": multiple,
                    "required_arr_usd": round(required_arr_for_target(target_usd, multiple), 2),
                    "required_paying_pairs": required_paying_pairs(target_usd, price, multiple),
                }
            )
    return scenarios


def milestone_ladder() -> list[dict[str, object]]:
    return [
        {
            "stage": "S0 private sacred system",
            "valuation_logic": "replacement cost + option value",
            "hard_metric": "reproducible import, tests, consent contract",
            "target": "$100k-$500k",
        },
        {
            "stage": "S1 research artifact",
            "valuation_logic": "evidence bundle + falsifiable hypotheses",
            "hard_metric": "preprint, public sanitized demo, external audit",
            "target": "$500k-$2M",
        },
        {
            "stage": "S2 pilot product",
            "valuation_logic": "LOIs + paid pilots + retention",
            "hard_metric": "50-200 couples, 60d retention, willingness-to-pay",
            "target": "$2M-$8M",
        },
        {
            "stage": "S3 category company",
            "valuation_logic": "ARR multiple + strategic data moat",
            "hard_metric": ">$1M ARR or enterprise contracts",
            "target": "$8M-$23M+",
        },
        {
            "stage": "S4 neurointerface continuity protocol",
            "valuation_logic": "strategic acquisition / protocol layer",
            "hard_metric": "device integrations, longitudinal outcome evidence, regulated-grade governance",
            "target": "$23M-$100M+",
        },
    ]


def build_report(metrics: dict) -> dict:
    vector = OmegaVector.from_metrics(metrics)
    score = compute_omega_score(vector)
    band = value_repo(score)
    return {
        "version": "v6",
        "interpretation": "valuation engineering model, not a sale price and not a price of love",
        "score": score.as_dict(),
        "valuation_band": band.as_dict(),
        "uplift_actions": uplift_actions(vector),
        "target_scenarios_23m": target_scenarios(),
        "milestone_ladder": milestone_ladder(),
        "gates_to_23m_plus": [
            "public sanitized demo and reproducible benchmark",
            "bilateral consent receipts and revocation protocol",
            "10-50 real couples pilot with retention metrics",
            "published claim boundary and falsification report",
            "defensible private dataset rights and licensing model",
            "security audit and encrypted archive sovereignty",
            "ARR or signed LOIs; without revenue, $23M is strategic-option value, not fair-market value",
        ],
    }


def main() -> None:
    report = build_report(load_metrics())
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
