# Technical Debt Register v7

## Resolved in v7

- API had no auth gate → added API-key zero-trust dependency.
- Media could be stored before consent result → consent gate moved before persistence.
- Runtime did not fail closed → production runtime safety check added.
- Audit trail was not tamper-evident → hash-chain JSONL ledger added.
- Input schemas allowed extra fields → strict Pydantic schemas.
- Telegram role binding was volatile memory → persisted `telegram_identities` table.
- Media path construction was weak → safe slug, root confinement, atomic writes.
- Hormone/partner-state claims were implicit → claim calibration kernel.

## Still intentionally open

- External KMS is not included.
- Full pgvector ANN index is schema-ready but not benchmarked here.
- Mobile HealthKit/Google Fit native clients are not included.
- Penetration test by an external auditor is still required before public hosting.
- SBOM generation is documented but not executed inside this sandbox.
