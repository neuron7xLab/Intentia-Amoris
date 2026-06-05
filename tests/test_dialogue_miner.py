from intentia_amoris.research.dialogue_miner import analyze


def test_dialogue_miner_counts_events():
    events = [
        {
            "actor": "self",
            "text": "я хочу ніжно і згодою",
            "media": [],
            "reactions": ["❤"],
            "timestamp_raw": "28.05.2026 19:04:07 GMT+02:00",
        },
        {
            "actor": "partner",
            "text": "согласна",
            "media": [{"kind": "photo"}],
            "reactions": [],
            "timestamp_raw": "28.05.2026 19:05:07 GMT+02:00",
        },
    ]
    metrics = analyze(events)
    assert metrics.total_events == 2
    assert metrics.actors["self"] == 1
    assert metrics.media_events == 1
    assert metrics.reactions["❤"] == 1
    assert metrics.feature_counts["eros"] >= 1
    assert metrics.feature_counts["boundary"] >= 1
