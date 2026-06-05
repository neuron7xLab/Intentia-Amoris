from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Iterable


class ConsentLevel(StrEnum):
    NONE = "none"
    AGGREGATE = "aggregate"
    GRADIENT = "gradient"
    FULL = "full"


_LEVEL_RANK: dict[ConsentLevel, int] = {
    ConsentLevel.NONE: 0,
    ConsentLevel.AGGREGATE: 1,
    ConsentLevel.GRADIENT: 2,
    ConsentLevel.FULL: 3,
}


@dataclass(frozen=True, slots=True)
class ConsentGrant:
    subject_id: str
    recipient_id: str
    stream: str
    purpose: str
    level: ConsentLevel
    granted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    revoked_at: datetime | None = None
    expires_at: datetime | None = None
    evidence_ref: str = "manual"

    @property
    def active(self) -> bool:
        now = datetime.now(timezone.utc)
        if self.revoked_at is not None:
            return False
        if self.expires_at is not None and self.expires_at <= now:
            return False
        return self.level != ConsentLevel.NONE

    def permits(self, required_level: ConsentLevel) -> bool:
        return self.active and _LEVEL_RANK[self.level] >= _LEVEL_RANK[required_level]


@dataclass(slots=True)
class ConsentDecision:
    allowed: bool
    reason: str
    matched_grant: ConsentGrant | None = None


class ConsentLedger:
    """Small deterministic consent kernel for retrieval-time authorization.

    The ledger is intentionally boring: exact subject, recipient, stream and purpose
    match. No fuzzy inference. No "probably allowed". Romance already produces enough
    undefined behavior without software helping it.
    """

    def __init__(self, grants: Iterable[ConsentGrant] | None = None) -> None:
        self._grants: list[ConsentGrant] = list(grants or [])

    def add(self, grant: ConsentGrant) -> None:
        self._grants.append(grant)

    def revoke(
        self,
        *,
        subject_id: str,
        recipient_id: str,
        stream: str,
        purpose: str,
        revoked_at: datetime | None = None,
    ) -> None:
        stamp = revoked_at or datetime.now(timezone.utc)
        updated: list[ConsentGrant] = []
        for grant in self._grants:
            if (
                grant.subject_id == subject_id
                and grant.recipient_id == recipient_id
                and grant.stream == stream
                and grant.purpose == purpose
                and grant.revoked_at is None
            ):
                updated.append(
                    ConsentGrant(
                        subject_id=grant.subject_id,
                        recipient_id=grant.recipient_id,
                        stream=grant.stream,
                        purpose=grant.purpose,
                        level=grant.level,
                        granted_at=grant.granted_at,
                        revoked_at=stamp,
                        expires_at=grant.expires_at,
                        evidence_ref=grant.evidence_ref,
                    )
                )
            else:
                updated.append(grant)
        self._grants = updated

    def decision(
        self,
        *,
        subject_id: str,
        recipient_id: str,
        stream: str,
        purpose: str,
        required_level: ConsentLevel = ConsentLevel.FULL,
    ) -> ConsentDecision:
        matches = [
            grant
            for grant in self._grants
            if grant.subject_id == subject_id
            and grant.recipient_id == recipient_id
            and grant.stream == stream
            and grant.purpose == purpose
        ]
        if not matches:
            return ConsentDecision(False, "NO_MATCHING_GRANT")

        active = [grant for grant in matches if grant.permits(required_level)]
        if not active:
            return ConsentDecision(False, "GRANT_INACTIVE_OR_INSUFFICIENT", matches[-1])

        return ConsentDecision(True, "AUTHORIZED", active[-1])

    def permits(
        self,
        *,
        subject_id: str,
        recipient_id: str,
        stream: str,
        purpose: str,
        required_level: ConsentLevel = ConsentLevel.FULL,
    ) -> bool:
        return self.decision(
            subject_id=subject_id,
            recipient_id=recipient_id,
            stream=stream,
            purpose=purpose,
            required_level=required_level,
        ).allowed
