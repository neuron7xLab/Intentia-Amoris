from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ContinuationMode(StrEnum):
    DISABLED = "disabled"
    MEMORY_ONLY = "memory_only"
    ADVISORY_AVATAR = "advisory_avatar"
    RESEARCH_TWIN = "research_twin"


@dataclass(frozen=True, slots=True)
class ContinuationConsent:
    actor: str
    mode: ContinuationMode = ContinuationMode.DISABLED
    can_use_text_style: bool = False
    can_use_voice: bool = False
    can_use_images: bool = False
    can_answer_as_person: bool = False
    can_offer_advice: bool = True
    revocable: bool = True
    guardian_keys: tuple[str, ...] = ()
    notes: str = ""


@dataclass(slots=True)
class ContinuationCapsule:
    """
    Digital eternity is valid only as an explicit capsule.

    The capsule cannot impersonate active consent. If can_answer_as_person is false,
    it must speak as archive/advisory model, never as the living human.
    """

    pair_id: str = "yaroslav_dasha"
    consents: dict[str, ContinuationConsent] = field(default_factory=dict)

    def allowed(self, actor: str, capability: str) -> bool:
        consent = self.consents.get(actor)
        if consent is None or consent.mode == ContinuationMode.DISABLED:
            return False
        return bool(getattr(consent, capability, False))

    def require(self, actor: str, capability: str) -> None:
        if not self.allowed(actor, capability):
            raise PermissionError(
                f"Continuation capability denied: actor={actor} capability={capability}"
            )
