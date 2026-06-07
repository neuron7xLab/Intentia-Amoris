#!/usr/bin/env bash
set -euo pipefail

python -m compileall -q src
pytest -q
python - <<'PY'
import json
from pathlib import Path
for path in ['repo_genome.json','artifacts/evidence_bundle/manifest.json']:
    p = Path(path)
    if p.exists():
        json.loads(p.read_text(encoding='utf-8'))
PY

echo 'verify_all PASS'
