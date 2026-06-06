from __future__ import annotations

from intentia_amoris.consent import ConsentGrant, ConsentLedger
from intentia_amoris.memory.retrieval_contract import EvidenceClass, RetrievalItem, filter_items


def item(item_id: str, subject: str = "alpha") -> RetrievalItem:
    return RetrievalItem(
        item_id=item_id,
        subject_id=subject,
        stream="messages",
        purpose="repair",
        content="bounded