from intentia_amoris.telemetry.adapters import Metric, PhoneTelemetryPacket, classify_telemetry_risk


def test_phone_telemetry_packet_content():
    packet = PhoneTelemetryPacket(
        actor="self",
        source="manual",
        metrics=[Metric(name="steps", value=8000, unit="count")],
        mood_label="calm",
    )
    assert "steps=8000count" in packet.to_event_content()


def test_telemetry_risk_deterministic_gate():
    low = classify_telemetry_risk({"sleep_hours": 7.5, "hrv_ms": 55, "resting_hr": 60, "steps": 9000})
    high = classify_telemetry_risk({"sleep_hours": 4.5, "hrv_ms": 18, "resting_hr": 92, "steps": 1000})
    assert low["risk"] < high["risk"]
    assert high["label"] in {"watch", "high_load"}
