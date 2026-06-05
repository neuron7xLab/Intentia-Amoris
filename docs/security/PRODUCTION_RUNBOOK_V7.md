# Intentia v7 Production Runbook

## Local secure start

```bash
cp .env.example .env
python - <<'PY'
import secrets
print(secrets.token_urlsafe(32))
PY
# put generated values into INTENTIA_API_KEYS and INTENTIA_SECRET_KEY
docker compose up --build
```

## Required environment

```text
INTENTIA_ENV=prod
INTENTIA_REQUIRE_API_AUTH=true
INTENTIA_API_KEYS=<rotatable comma-separated secrets>
INTENTIA_SECRET_KEY=<32+ chars>
INTENTIA_DATABASE_URL=postgresql+asyncpg://...
```

## Backup

1. `pg_dump` database daily.
2. Back up `data/media`.
3. Back up `data/audit`.
4. Store encrypted copies only.

## Emergency stop

Set:

```text
INTENTIA_REQUIRE_API_AUTH=true
INTENTIA_API_KEYS=<new key only>
```

Restart services and rotate old keys.

## Consent incident

If data was stored without correct consent:

1. freeze writes;
2. export audit window;
3. identify affected event/media ids;
4. delete or quarantine records;
5. document remediation;
6. require renewed consent.
