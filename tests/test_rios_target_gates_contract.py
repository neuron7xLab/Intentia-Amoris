from pathlib import Path


def test_target_gate_contract_lists_all_seven_epics() -> None:
    text = Path('contracts/RIOS_TARGET_GATES_2026.yaml').read_text(encoding='utf-8')
    expected = {
        'P0_STATE_SERIALIZATION',
        'P0_VECTOR_SEARCH',
        'P0_AUDIT_RATE_LIMIT',
        'P1_EMBEDDING_BULKHEAD',
        'P1_MEDIA_STREAMING',
        'P1_IMPORT_CHECKPOINTS',
        'P2_REPO_GOVERN