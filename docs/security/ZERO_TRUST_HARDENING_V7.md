# Intentia Amoris v7 — Zero Trust Hardening

## Purpose

v7 turns Intentia from a research prototype into a hardened product scaffold.

The system is built around four rules:

1. **Deny by default** — protected API endpoints require `X-Intentia-API-Key`.
2. **Consent before persistence** — media is not written before the consent gate passes.
3. **Evidence before claims** — hormones require measured labs; partner inner states require partner signal.
4. **Audit before trust** — important operations emit tamper-evident audit events.

## New modules

```text
src/intentia_amoris/security/auth.py
src/intentia_amoris/security/audit.py
src/intentia_amoris/security/crypto.py
src/intentia_amoris/security/middleware.py
src/intentia_amoris/security/rate_limit.py
src/intentia_amoris/security/redaction.py
src/intentia_amoris/security/validation.py
src/intentia_amoris/kernel/calibration.py
src/intentia_amoris/quality/security_audit.py
contracts/security/ZERO_TRUST_CONTROL_MAP.json
```

## API hardening

Protected endpoints now require:

```http
X-Intentia-API-Key: <one of INTENTIA_API_KEYS>
```

Production startup fails unless:

```text
INTENTIA_REQUIRE_API_AUTH=true
INTENTIA_API_KEYS is non-empty
INTENTIA_SECRET_KEY length >= 32
```

## Media hardening

Upload pipeline:

```text
receive metadata
  ↓
build pre-event
  ↓
ConsentGate.evaluate_event
  ↓
validate size extension path
  ↓
atomic write under INTENTIA_MEDIA_ROOT
  ↓
hash sha256
  ↓
event-store
```

## Claims calibration

Intentia blocks or downgrades claims:

```text
hormone + not measured → blocked
partner intent + unknown evidence → blocked
inferred claim → capped confidence
unknown evidence → low confidence + caveat
```

## Audit ledger

Audit logs are JSONL lines with:

```text
prev_hash
hash
created_at
event_type
actor
action
target
allowed
reason
metadata
```

If a line is edited or removed, verification fails.

## Security audit

```bash
aris-security-audit
pytest -q
```
