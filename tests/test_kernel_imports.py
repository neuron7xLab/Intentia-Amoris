import importlib


def test_core_modules_import() -> None:
    assert importlib.import_module("intentia_amoris.consent.ledger")
    assert importlib.import_module("intentia_amoris.memory.retrieval_contract")
