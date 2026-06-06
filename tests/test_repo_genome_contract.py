import json
from pathlib import Path


def test_repo_genome_contract_shape() -> None:
    root = Path(__file__).resolve().parents[1]
    data = json.loads((root / "repo_genome.json").read_text(encoding="utf-8"))
    assert data["repo"] == "intentia_amoris"
    assert isinstance(data["gates"], int)
    assert data["gates"] > 0
    assert isinstance(data["verdict"], str)


def test_risk_lattice_has