from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Hypothesis:
    key: str
    claim: str
    measurement: str
    falsifier: str
    minimum_evidence: str
    status: str = "preregistered"

    def as_dict(self) -> dict[str, str]:
        return {
            "key": self.key,
            "claim": self.claim,
            "measurement": self.measurement,
            "falsifier": self.falsifier,
            "minimum_evidence": self.minimum_evidence,
            "status": self.status,
        }


HYPOTHESES: tuple[Hypothesis, ...] = (
    Hypothesis(
        key="H1_co_regulation",
        claim="Daily Intentia check-ins reduce unresolved conflict duration without increasing pressure.",
        measurement="median time from conflict signal to repair signal; pressure score before/after advice",
        falsifier="conflict duration or pressure increases for 3 consecutive weeks versus baseline",
        minimum_evidence=">=14 days baseline, >=30 days intervention, both partners' consented labels",
    ),
    Hypothesis(
        key="H2_reality_fidelity",
        claim="Separating facts/inferences/unknowns reduces hallucinated interpretations of the partner.",
        measurement="rate of unsupported claims per 100 messages in manual audit",
        falsifier="unsupported-claim rate does not decrease by >=20% after reality gate",
        minimum_evidence="blind-coded sample of >=200 messages",
    ),
    Hypothesis(
        key="H3_consent_integrity",
        claim="Consent-gated advice preserves autonomy while allowing intimacy to increase.",
        measurement="intimacy signals, boundary respect signals, post-event comfort ratings",
        falsifier="boundary violations or regret labels increase above baseline",
        minimum_evidence="paired pre/post ratings and explicit revocation channel",
    ),
    Hypothesis(
        key="H4_memory_continuity",
        claim="Event-sourced multimodal memory improves narrative continuity and reduces rupture amnesia.",
        measurement="recall agreement between partners and archive-derived timeline",
        falsifier="archive-derived summaries mismatch partner accounts in >15% of audited episodes",
        minimum_evidence=">=20 episodes manually reviewed by both partners",
    ),
    Hypothesis(
        key="H5_value_creation",
        claim="The repository becomes investable only when reproducibility, consent, and product metrics are measurable.",
        measurement="CI pass rate, reproducible report hash, pilot retention, willingness-to-pay",
        falsifier="valuation claim cannot be reproduced from public/sanitized evidence bundle",
        minimum_evidence="signed pilot LOIs or paid users plus reproducible benchmarks",
    ),
)


def claim_boundary() -> dict:
    return {
        "can_claim": [
            "Intentia stores and analyzes consented relationship events",
            "Intentia computes operational scores from defined metrics",
            "Intentia can generate hypotheses and advice with uncertainty labels",
            "Intentia can be valued by cost, income, market, royalty, and option methods when inputs exist",
        ],
        "cannot_claim_without_evidence": [
            "Intentia understands Dasha better than Dasha",
            "Intentia measures hormones without lab data",
            "Intentia guarantees eternal consciousness",
            "Intentia is worth $23M as fair-market value without revenue, rights, audits, or comparable transactions",
        ],
        "upgrade_rule": "Every extraordinary claim must map to a test, dataset, reproduction script, and falsifier.",
    }


def build_falsification_report() -> dict:
    return {
        "version": "v6",
        "hypotheses": [h.as_dict() for h in HYPOTHESES],
        "claim_boundary": claim_boundary(),
    }


def main() -> None:
    print(json.dumps(build_falsification_report(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
