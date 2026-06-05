from pathlib import Path

from intentia_amoris.quality.product_audit import run_product_audit


def test_product_audit_passes_repository_root():
    report = run_product_audit(Path("."))
    assert report["ok"], report["failed"]
    assert report["score"] == 1.0
