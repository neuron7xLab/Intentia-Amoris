import importlib


def test_verification_helper_has_entrypoint():
    module = importlib.import_module('scripts.verify_all')
    assert callable(module.main)
