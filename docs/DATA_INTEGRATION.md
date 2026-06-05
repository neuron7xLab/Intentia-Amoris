# Data Integration

This repository includes a private Telegram export transformed into Intentia event memory.

## Source files

```text
data/private/raw/telegram_export/messages.html
data/private/raw/telegram_export/archive_name.zip
```

## Derived files

```text
data/derived/telegram/messages.jsonl
data/derived/telegram/summary.json
data/derived/telegram/dialogue_signals.json
data/derived/telegram/media_manifest.json
data/derived/telegram/living_story_snapshot.md
```

## Current import summary

```json
{
  "message_count": 1000,
  "text_message_count": 882,
  "media_message_count": 117,
  "reply_message_count": 61,
  "link_message_count": 1,
  "sender_counts": {
    "Дарія 🍓 Вікторівна 👸": 456,
    "Yaroslav": 544
  },
  "actor_counts": {
    "partner": 456,
    "self": 544
  },
  "media_counts": {
    "photo": 71,
    "video": 29,
    "call": 3,
    "voice": 14
  },
  "reaction_counts": {
    "❤": 107,
    "🔥": 17,
    "🥰": 3,
    "🤯": 1,
    "🤣": 2,
    "😈": 1,
    "👍": 1
  },
  "first_timestamp": "28.05.2026 19:04:07 GMT+02:00",
  "last_timestamp": "02.06.2026 19:51:39 GMT+02:00",
  "days": [
    "1 June 2026",
    "2 June 2026",
    "28 May 2026",
    "29 May 2026",
    "30 May 2026",
    "31 May 2026"
  ]
}
```

## Media

Every photo/video/voice reference that exists inside the uploaded Telegram archive is represented in:

```text
data/derived/telegram/media_manifest.json
```

Each entry includes:

```text
message_id
timestamp
actor
kind
href
sha256
size
```

This lets the system treat media as evidence-bearing artifacts without exposing them in prompts by default.

## Interpretation rule

The Telegram export is evidence of messages, timing, media, reactions and replies.

It is **not** direct evidence of hidden thoughts, hormones, consent outside the recorded context, or future decisions.

Intentia stores three classes of data:

```text
observed    exact event from the export
inferred    cautious signal extracted from patterns
unknown     anything not directly available
```
