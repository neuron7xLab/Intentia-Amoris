from __future__ import annotations

from dataclasses import dataclass
from math import exp
from typing import Mapping


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))


@dataclass(frozen=True, slots=True)
class OmegaVector:
    """Operational value vector for a dyadic relationship-intelligence system.

    This vector does not price "love". It measures how well the technical system
    turns a living archive into a safe, falsifiable, compounding intellectual asset.
    """

    consent_integrity: float
    evidence_density: float
    reality_fidelity: float
    dyadic_safety: float
    autonomy_symmetry: float
    narrative_continuity: float
    neuroplastic_learning: float
    multimodal_depth: float
    reproducibility: float
    security_sovereignty: float
    product_surface: float
    research_grade: float
    financial_optionality: float
    abyss_risk: float

    def as_dict(self) -> dict[str, float]:
        return {field: getattr(self, field) for field in self.__dataclass_fields__}

    @classmethod
    def from_metrics(cls, metrics: Mapping[str, object]) -> "OmegaVector":
        total = float(metrics.get("total_events") or metrics.get("message_count") or 0)
        text = float(metrics.get("text_events") or metrics.get("text_message_count") or 0)
        media = float(metrics.get("media_events") or metrics.get("media_message_count") or 0)
        actors = metrics.get("actors") or metrics.get("actor_counts") or {}
        reactions = metrics.get("reactions") or metrics.get("reaction_counts") or {}
        features = metrics.get("feature_counts") or metrics.get("signal_counts") or {}

        self_events = float(getattr(actors, "get", lambda *_: 0)("self", 0))
        partner_events = float(getattr(actors, "get", lambda *_: 0)("partner", 0))
        total_actor = max(1.0, self_events + partner_events)
        balance = 1.0 - abs(self_events - partner_events) / total_actor

        heart = float(getattr(reactions, "get", lambda *_: 0)("❤", 0))
        fire = float(getattr(reactions, "get", lambda *_: 0)("🔥", 0))
        affection = float(getattr(features, "get", lambda *_: 0)("affection", 0))
        boundary = float(getattr(features, "get", lambda *_: 0)("boundary", 0))
        eros = float(getattr(features, "get", lambda *_: 0)("eros", 0))
        future = float(getattr(features, "get", lambda *_: 0)("future_story", 0))

        evidence_density = clamp(1 - exp(-total / 1800.0))
        multimodal_depth = clamp(1 - exp(-media / 350.0))
        narrative_continuity = clamp(0.30 + 0.20 * evidence_density + 0.12 * future)
        dyadic_safety = clamp(0.50 + 0.20 * balance + 0.002 * heart + 0.003 * boundary)
        reality_fidelity = clamp(0.58 + 0.14 * evidence_density + 0.10 * balance)
        autonomy_symmetry = clamp(0.42 + 0.38 * balance + 0.005 * boundary)
        neuroplastic_learning = clamp(0.40 + 0.24 * evidence_density + 0.18 * (eros > 0) + 0.10 * (future > 0))
        consent_integrity = clamp(0.62 + 0.008 * boundary - 0.002 * max(0.0, eros - boundary))
        reproducibility = 0.72
        security_sovereignty = 0.64
        product_surface = 0.35
        research_grade = 0.55
        financial_optionality = 0.40 + 0.20 * evidence_density + 0.08 * multimodal_depth
        abyss_risk = clamp(0.28 + 0.006 * eros - 0.010 * boundary + 0.08 * (1 - balance))

        return cls(
            consent_integrity=consent_integrity,
            evidence_density=evidence_density,
            reality_fidelity=reality_fidelity,
            dyadic_safety=dyadic_safety,
            autonomy_symmetry=autonomy_symmetry,
            narrative_continuity=narrative_continuity,
            neuroplastic_learning=neuroplastic_learning,
            multimodal_depth=multimodal_depth,
            reproducibility=reproducibility,
            security_sovereignty=security_sovereignty,
            product_surface=product_surface,
            research_grade=research_grade,
            financial_optionality=financial_optionality,
            abyss_risk=abyss_risk,
        )


@dataclass(frozen=True, slots=True)
class OmegaScore:
    omega: float
    investability: float
    defensibility: float
    research_validity: float
    eternity_readiness: float
    risk: float
    vector: OmegaVector

    def as_dict(self) -> dict[str, object]:
        return {
            "omega": round(self.omega, 4),
            "investability": round(self.investability, 4),
            "defensibility": round(self.defensibility, 4),
            "research_validity": round(self.research_validity, 4),
            "eternity_readiness": round(self.eternity_readiness, 4),
            "risk": round(self.risk, 4),
            "vector": {k: round(v, 4) for k, v in self.vector.as_dict().items()},
        }


def compute_omega_score(vector: OmegaVector) -> OmegaScore:
    v = vector.as_dict()
    protective = (
        v["consent_integrity"] ** 1.35
        * v["reality_fidelity"] ** 1.10
        * v["dyadic_safety"] ** 1.05
        * v["autonomy_symmetry"] ** 1.10
    )
    compounding = (
        0.16 * v["evidence_density"]
        + 0.11 * v["narrative_continuity"]
        + 0.12 * v["neuroplastic_learning"]
        + 0.10 * v["multimodal_depth"]
        + 0.12 * v["reproducibility"]
        + 0.11 * v["security_sovereignty"]
        + 0.13 * v["product_surface"]
        + 0.13 * v["research_grade"]
        + 0.12 * v["financial_optionality"]
    )
    risk = clamp(0.62 * v["abyss_risk"] + 0.20 * (1 - v["consent_integrity"]) + 0.18 * (1 - v["security_sovereignty"]))
    omega = clamp(protective * compounding * (1 - 0.55 * risk) * 1.65)

    investability = clamp(
        0.20 * v["product_surface"]
        + 0.18 * v["financial_optionality"]
        + 0.16 * v["reproducibility"]
        + 0.14 * v["research_grade"]
        + 0.12 * v["security_sovereignty"]
        + 0.10 * v["evidence_density"]
        + 0.10 * v["multimodal_depth"]
        - 0.18 * risk
    )
    defensibility = clamp(
        0.18 * v["evidence_density"]
        + 0.16 * v["narrative_continuity"]
        + 0.14 * v["multimodal_depth"]
        + 0.16 * v["security_sovereignty"]
        + 0.14 * v["research_grade"]
        + 0.12 * v["reproducibility"]
        + 0.10 * v["consent_integrity"]
    )
    research_validity = clamp(
        0.22 * v["reproducibility"]
        + 0.20 * v["research_grade"]
        + 0.18 * v["reality_fidelity"]
        + 0.14 * v["evidence_density"]
        + 0.14 * v["consent_integrity"]
        + 0.12 * (1 - risk)
    )
    eternity_readiness = clamp(
        0.20 * v["security_sovereignty"]
        + 0.18 * v["narrative_continuity"]
        + 0.16 * v["consent_integrity"]
        + 0.14 * v["multimodal_depth"]
        + 0.14 * v["reproducibility"]
        + 0.10 * v["neuroplastic_learning"]
        + 0.08 * (1 - risk)
    )

    return OmegaScore(
        omega=omega,
        investability=investability,
        defensibility=defensibility,
        research_validity=research_validity,
        eternity_readiness=eternity_readiness,
        risk=risk,
        vector=vector,
    )


def uplift_actions(vector: OmegaVector) -> list[dict[str, object]]:
    """Return valuation levers ordered by expected marginal lift."""

    levers = [
        ("product_surface", "ship a reproducible demo: web dashboard + Telegram + importer + public sanitized sample"),
        ("research_grade", "add preregistered hypotheses, baselines, ablations, and falsification reports"),
        ("security_sovereignty", "add encryption-at-rest, key rotation, revocation ledger, off-site encrypted backups"),
        ("multimodal_depth", "add image/audio captioning pipeline with consent and provenance hashes"),
        ("reproducibility", "add one-command reproduce, deterministic reports, CI artifacts, pinned data checksums"),
        ("financial_optionality", "add pricing experiments, licensing SKUs, enterprise pilot contract, dataset rights schedule"),
        ("consent_integrity", "add bilateral consent receipts and per-event revocation semantics"),
    ]
    current = vector.as_dict()
    ranked = sorted(levers, key=lambda x: current.get(x[0], 0.0))
    return [
        {"dimension": dim, "current": round(current.get(dim, 0.0), 3), "action": action}
        for dim, action in ranked
    ]
