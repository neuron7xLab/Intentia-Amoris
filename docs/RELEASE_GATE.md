# Release Gate

## Required commands

```bash
bash scripts/verify_all.sh
```

## Expected output

```text
verify_all PASS
```

## Required artifacts

- repo_genome.json
- claim_matrix.csv
- verification_report.md
- artifacts/evidence_bundle/manifest.json

## Reproducibility

A clean checkout must install, compile, test, and parse JSON audit artifacts without manual steps.
