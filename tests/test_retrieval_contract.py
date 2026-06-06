from __future__ import annotations

from intentia_amoris.consent import ConsentGrant, ConsentLedger, ConsentLevel
from intentia_amoris.memory.retrieval_contract import EvidenceClass, RetrievalItem, filter_items


def test_filter_items_selects_only_matching_grant_context() -> None:
    ledger = ConsentLedger(
        [
            ConsentGrant(
                subject_id="alpha",
                recipient_id="beta",