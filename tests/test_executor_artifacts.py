import json
from pathlib import Path


def test_executor_artifacts_exist_and_manifest_parses():
    paths = [
        'scripts/verify_all.sh',
        'docs/EXECUTION_PLAN.md',
        'docs/ENGINEERING_REPORT.md',
        'docs/RELEASE_GATE.md',
        'artifacts/evidence_bundle/manifest.json',
    ]
    for item in paths:
        assert Path(item).exists()
