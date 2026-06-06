import json
from pathlib import Path


def test_repo_genome_json_is_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "repo_genome.json").read_text(encoding="utf-8"))
    assert isinstance(data, dict)
