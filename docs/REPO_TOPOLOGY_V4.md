# Repository Topology v4

```text
data/private/raw/telegram_export/
  messages.html
  archive_name.zip

data/derived/telegram/
  messages.jsonl
  media_manifest.json
  summary.json
  dialogue_signals.json
  living_story_snapshot.*
  parousia_metrics.json
  parousia_dialogue_report.md

docs/
  FIRST_PRINCIPLES_V4.md
  VALUE_FUNCTIONS_V4.md
  OMEGA_ARCHITECTURE.md
  CLAIM_BOUNDARY_V4.md

src/intentia_amoris/kernel/
  first_principles.py
  value_functions_v4.py
  autopoiesis.py
  continuation.py

src/intentia_amoris/research/
  dialogue_miner.py

tests/
  test_value_functions_v4.py
  test_dialogue_miner.py
```

## Research shape

```text
claim → boundary → evidence → code → test → report → audit → revision
```

## Private boundary

Raw Telegram data is intentionally inside `data/private`.
Do not publish this directory unless both people explicitly approve.
