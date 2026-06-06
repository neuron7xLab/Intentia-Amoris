# Verification Report

Verdict: PARTIAL

Verified:
- repo_genome.json is parsed by pytest.
- CI uses make check.
- make check runs compile and pytest.

Partial:
- claim_matrix.csv exists with VERIFIED and PARTIAL rows.
- risk_lattice.md has no parser gate yet.
- audit_verdict.md has no value gate yet.

Not run here: CLI smoke, API smoke, schema check, circular import scan, dependency scan, benchmark.
