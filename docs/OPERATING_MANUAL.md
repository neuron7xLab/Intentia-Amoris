# Operating Manual

## Local

```bash
pip install -e ".[dev]"
INTENTIA_ENV=test pytest -q
intentia-value
intentia-product-audit
intentia-security-audit
```

## Production

```bash
cp .env.example .env
python - <<'PY'
import secrets
print("INTENTIA_API_KEYS=" + secrets.token_urlsafe(32))
print("INTENTIA_SECRET_KEY=" + secrets.token_urlsafe(48))
PY
docker compose up --build
```

## API key

```http
X-Intentia-API-Key: <secret>
# legacy compatible: X-ARIS-API-Key
```

Legacy name is preserved to avoid breaking clients.

## Data safety

Raw Telegram export lives under:

```text
data/private/raw/telegram_export/
```

Derived operational data lives under:

```text
data/derived/telegram/
```

Do not publish private data.
Create sanitized demos before public release.
