import json
from pathlib import Path

from intentia_amoris.research.living_story import build_living_story, load_messages
from intentia_amoris.research.paradigm import PAROUSIA_LAYERS, render_paradigm


def test_living_story_snapshot():
    messages = load_messages(Path("data/derived/telegram/messages.jsonl"))
    signals = json.loads(Path("data/derived/telegram/dialogue_signals.json").read_text())
    snapshot = build_living_story(messages, signals)
    assert snapshot.event_count == 1000
    assert snapshot.actors["self"] == 544
    assert snapshot.actors["partner"] == 456
    assert snapshot.media["photo"] == 71


def test_parousia_paradigm_has_consent_and_eternity():
    text = render_paradigm()
    assert len(PAROUSIA_LAYERS) == 7
    assert "Consent Kernel" in text
    assert "Eternity Gate" in text
