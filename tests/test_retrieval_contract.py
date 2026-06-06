from intentia_amoris.memory.retrieval_contract import EvidenceClass, RetrievalItem


def test_retrieval_item_hash_is_stable() -> None:
    item = RetrievalItem("r1", "alpha", "journal", "analysis", "ok", EvidenceClass.EVENT_LOG)
    assert item.stable_hash() == item.stable_hash()
    assert len(item.stable_hash()) == 64
