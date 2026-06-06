# Verification Report

Verdict: PARTIAL

## Verified

- repo_genome.json is parsed by an existing pytest gate.
- CI executes make check.
- GNUmakefile maps check to compile plus pytest.

## Partial

- claim_matrix.csv exists and records VERIFIED and PARTIAL rows.
- risk_lattice.md exists but has no parser gate yet.
- audit_verdict.md exists but has no value gate yet.

## Not executed

- CLI smoke.
- API smoke.
- schema validation.
- circular import scan.
- dependency boundary scan.
- minimal