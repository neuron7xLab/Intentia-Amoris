# Architecture v8 — Intentia Amoris

## Runtime topology

```text
            ┌────────────────────────────┐
            │ Telegram / API / Telemetry │
            └──────────────┬─────────────┘
                           ↓
┌────────────────────────────────────────────────┐
│ Zero Trust Boundary                            │
│ API key auth · rate limit · headers · schemas  │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Consent Kernel                                 │
│ privacy_scope · allowed action · revocation    │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Event-Sourced Memory                           │
│ raw events · derived chunks · media manifest   │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Cognitive Kernel                               │
│ embeddings · prototypes · scale homeostasis    │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Intentia Value Core                            │
│ protective integrity · compounding · abyss     │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Extrapolation                                  │
│ scenarios · probabilities · falsifiers         │
└──────────────────────┬─────────────────────────┘
                       ↓
┌────────────────────────────────────────────────┐
│ Aletheia ↔ Eunoia                              │
│ questions · advice · audit · dashboard         │
└────────────────────────────────────────────────┘
```

## Infrastructure

```text
FastAPI        API gateway
aiogram        Telegram runtime
SQLAlchemy     persistence
PostgreSQL     production store
pgvector       semantic retrieval target
SQLite         test/local fallback
Docker         portable runtime
GitHub Actions CI
```

## Production stance

- fail closed
- least privilege
- explicit secrets
- strict input schemas
- media validation
- consent-before-persistence
- audit everything meaningful
- no oracle claims
