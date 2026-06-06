from pathlib import Path


def test_repo_audit_files_exist() -> None:
    root = Path(__file__).resolve().parents[1]
    assert (root / "repo_genome.json").exists()
    assert (root / "risk_lattice.md").exists()
    assert (root / "audit_verdict.md").exists()
