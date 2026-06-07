from __future__ import annotations

import importlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    json.loads((ROOT / 'repo_genome.json').read_text())
    for name in ('intentia_amoris', 'intentia_amoris.reasoning.entropy', 'intentia_amoris.reasoning.gates'):
        importlib.import_module(name)
    print('verification self-check ok')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
