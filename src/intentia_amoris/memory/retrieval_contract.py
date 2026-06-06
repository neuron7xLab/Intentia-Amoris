from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from typing import Iterable

from intentia_amoris.consent import ConsentLedger, ConsentLevel


class EvidenceClass(StrEnum):
    HARD_TELEMETRY = "hard_telemetry"
    SUBJECTIVE_TELEMETRY = "subjective_telemetry"
    EVENT_LOG = "event_log"
    CONSENT_LEDGER = "consent_ledger"
    DERIVED_INFERENCE = "derived_inference"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class RetrievalItem:
    item_id: str
    subject_id: str
    stream: str
    purpose: str
    content: str
    evidence_class: EvidenceClass
    score: float = 0.0
    required_level: ConsentLevel = ConsentLevel.FULL
    metadata: dict[str, str] = field(default_factory=dict)

    def stable_hash(self) -> str:
        payload = "|".join(
            [
                self.item_id,
                self.subject_id,
                self.stream,
                self.purpose,
                self.evidence_class.value,
                self.content,
            ]
        )
        return sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class OmittedItem:
    item_id: str
    subject_id: str
    stream: str
    purpose: str
    reason: str


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    selected: tuple[RetrievalItem, ...]
    omitted: tuple[OmittedItem, ...]

    @property
    def selected_count(self) -> int:
        return len(self.selected)

    @property
    def omitted_count(self) -> int:
        return len(self.omitted)


def filter_items(
    *,
    items: Iterable[RetrievalItem],
    ledger: ConsentLedger,
    recipient_id: str,
) -> RetrievalResult:
    selected: list[RetrievalItem] = []
    omitted: list[OmittedItem] = []

    for item in items:
        decision = ledger.decision(
            subject_id=item.subject_id,
            recipient_id=recipient_id,
            stream=item.stream,
            purpose=item.purpose,
            required_level=item.required_level,
        )
        if decision.allowed:
            selected.append(item)
        else:
            omitted.append(
                OmittedItem(
                    item_id=item.item_id,
                    subject_id=item.subject_id,
                    stream=item.stream,
                    purpose=item.purpose,
                    reason=decision.reason,
                )
            )

    selected.sort(key=lambda row: (row.score, row.item_id), reverse=True)
    omitted.sort(key=lambda row: row.item_id)
    return RetrievalResult(tuple(selected), tuple(omitted))
