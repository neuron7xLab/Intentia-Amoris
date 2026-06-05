# Operations

## Local dev

```bash
cp .env.example .env
pip install -e ".[dev]"
pytest
uvicorn intentia_amoris.api:app --reload
```

## Docker

```bash
docker compose up --build
```

## Parse Telegram

```bash
aris-parse-telegram data/private/raw/telegram_export/messages.html \
  --archive data/private/raw/telegram_export/archive_name.zip \
  --out data/derived/telegram
```

## Import Telegram into DB

```bash
python scripts/import_telegram_to_db.py run data/derived/telegram/messages.jsonl
```

## Production deployment checklist

```text
set TELEGRAM_BOT_TOKEN
set DATABASE_URL
enable PostgreSQL backups
restrict CORS
restrict allowed Telegram IDs
enable HTTPS
encrypt raw exports
turn on object storage for media
schedule pg_dump
ship OpenTelemetry traces
```

## Private data warning

The sandbox zip includes raw Telegram export files because this build is for Yaroslav.  
Do not push raw archives to a public GitHub repository.
