from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from intentia_amoris.domain import EvidenceLevel


class ClaimKind(StrEnum):
    FACT = "fact"
    FEELING = "feeling"
    HORMONE = "hormone"
    INTENT = "intent"
    FORECAST = "forecast"
    VALUE = "value"


@dataclass(frozen=True, slots=True)
class Claim:
    kind: ClaimKind
    subject: str
    statement: str
    evidence_level: EvidenceLevel = EvidenceLevel.UNKNOWN
    confidence: float = 0.5
    evidence: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CalibratedClaim:
    claim: Claim
    allowed: bool
    calibrated_confidence: float
    caveats: tuple[str, ...]


def clamp(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def calibrate_claim(claim: Claim) -> CalibratedClaim:
    caveats: list[str] = []
    confidence = clamp(claim.confidence)

    if claim.kind == ClaimKind.HORMONE and claim.evidence_level != EvidenceLevel.MEASURED:
        return CalibratedClaim(
            claim=claim,
            allowed=False,
            calibrated_confidence=0.0,
            caveats=("hormone claims require measured lab data",),
        )

    if claim.kind in {ClaimKind.FEELING, ClaimKind.INTENT} and claim.subject in {"partner", "dasha"}:
        if claim.evidence_level == EvidenceLevel.UNKNOWN:
            return CalibratedClaim(
                claim=claim,
                allowed=False,
                calibrated_confidence=0.0,
                caveats=("partner inner state requires explicit partner signal",),
            )
        caveats.append("partner inner state is modeled as reported/inferred, not known")

    if claim.evidence_level == EvidenceLevel.MEASURED:
        confidence = min(0.98, max(confidence, 0.70))
    elif claim.evidence_level == EvidenceLevel.INFERRED:
        confidence = min(confidence, 0.72)
        caveats.append("inference not measurement")
    else:
        confidence = min(confidence, 0.45)
        caveats.append("unknown evidence level")

    return CalibratedClaim(
        claim=claim,
        allowed=True,
        calibrated_confidence=round(confidence, 3),
        caveats=tuple(caveats),
    )


def evidence_manifest(claims: list[Claim]) -> dict[str, Any]:
    calibrated = [calibrate_claim(c) for c in claims]
    return {
        "total_claims": len(calibrated),
        "allowed": sum(1 for c in calibrated if c.allowed),
        "blocked": sum(1 for c in calibrated if not c.allowed),
        "claims": [
            {
                "kind": c.claim.kind.value,
                "subject": c.claim.subject,
                "statement": c.claim.statement,
                "evidence_level": c.claim.evidence_level.value,
                "allowed": c.allowed,
                "confidence": c.calibrated_confidence,
                "caveats": list(c.caveats),
                "evidence": list(c.claim.evidence),
            }
            for c in calibrated
        ],
    }
