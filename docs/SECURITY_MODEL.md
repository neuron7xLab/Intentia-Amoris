# Security Model

## Baseline

Intentia aligns its internal control map with:

```text
NIST SP 800-207 Zero Trust Architecture
OWASP ASVS
OWASP API Security Top 10
OWASP SCVS
```

## Implemented controls

```text
deny-by-default API auth
rate limiting
runtime secret validation
security headers
strict Pydantic schemas
media extension and size validation
safe path handling
redaction utilities
tamper-evident audit ledger
non-root Docker runtime
CI tests
minimal SBOM
```

## Threats

```text
private archive leakage
unauthorized API access
media path traversal
prompt/inference overreach
partner-state hallucination
archive weaponization
supply-chain drift
```

## Production requirements

```text
INTENTIA_ENV=prod
INTENTIA_REQUIRE_API_AUTH=true
INTENTIA_API_KEYS=<secret>
INTENTIA_SECRET_KEY=<secret length >= 32>
TLS termination in front of API
encrypted backups
external security audit before public SaaS
```
