from pathlib import Path

from intentia_amoris.importers.telegram_html import (
    parse_telegram_html,
    summarize_messages,
    extract_dialogue_signals,
)


def test_real_telegram_export_parse_count():
    path = Path("data/private/raw/telegram_export/messages.html")
    messages = parse_telegram_html(path)
    summary = summarize_messages(messages)
    assert summary["message_count"] == 1000
    assert summary["actor_counts"]["self"] == 544
    assert summary["actor_counts"]["partner"] == 456


def test_dialogue_signal_extraction_is_auditable():
    path = Path("data/private/raw/telegram_export/messages.html")
    messages = parse_telegram_html(path)
    signals = extract_dialogue_signals(messages)
    assert "interpretation_rule" in signals
    assert signals["signal_counts"]["desire"] > 0
    assert signals["signal_counts"]["boundary"] > 0
