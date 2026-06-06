from __future__ import annotations

from datetime import datetime, timedelta, timezone

from intentia_amoris.consent import ConsentGrant, ConsentLedger, ConsentLevel
from intentia_amoris.memory.retrieval_contract import EvidenceClass, RetrievalItem, filter_items


def _item(
    item_id: str,
    *,
    subject_id: str = "alpha",
    stream: str = "messages