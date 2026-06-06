import json
from pathlib import Path


def test_repo_genome_contract_shape() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "repo_genome.json").read_text(encoding="utf-8"))
    assert data["repo"] == "neuron7xLab/Intentia-Amoris"
    assert data["ci_gate"] == "make check"
    assert data["genome_status"] == "indexed