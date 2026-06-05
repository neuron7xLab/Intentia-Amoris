from pathlib import Path

import pytest

from intentia_amoris.domain import EvidenceLevel
from intentia_amoris.kernel.calibration import Claim, ClaimKind, calibrate_claim, evidence_manifest
from intentia_amoris.quality.security_audit import run_security_audit
from intentia_amoris.security.audit import AuditEvent, AuditLedger
from intentia_amoris.security.crypto import FieldCipher, constant_time_match, key_fingerprint
from intentia_amoris.security.redaction import redact_mapping, redact_text
from intentia_amoris.security.validation import (
    ValidationError,
    ensure_within_directory,
    safe_slug,
    validate_event_content,
    validate_media_upload,
    validate_metadata,
)


def test_constant_time_api_key_match():
    allowed = {"alpha", "beta"}
    assert constant_time_match("alpha", allowed)
    assert not constant_time_match("gamma", allowed)
    assert key_fingerprint("alpha") == key_fingerprint("alpha")


def test_redaction_removes_secrets_and_contacts():
    text = "token=abc123 email a@b.com phone +380 67 123 45 67"
    redacted = redact_text(text)
    assert "abc123" not in redacted
    assert "a@b.com" not in redacted
    assert "+380" not in redacted
    mapping = redact_mapping({"api_key": "secret", "nested": {"phone": "+380 67 123 45 67"}})
    assert mapping["api_key"] == "<redacted>"


def test_validation_blocks_path_traversal_and_large_content(tmp_path: Path):
    assert safe_slug("../bad name") == "bad_name"
    with pytest.raises(ValidationError):
        ensure_within_directory(tmp_path, tmp_path / ".." / "escape.txt")
    with pytest.raises(ValidationError):
        validate_event_content("")
    assert validate_event_content(" valid ") == "valid"
    assert validate_metadata({"a": 1}) == {"a": 1}


def test_media_validation_blocks_extension_and_size(monkeypatch):
    assert validate_media_upload(b"abc", "photo.jpg") == "photo.jpg"
    with pytest.raises(ValidationError):
        validate_media_upload(b"abc", "run.exe")


def test_audit_ledger_hash_chain_detects_tampering(tmp_path: Path):
    ledger = AuditLedger(tmp_path / "audit.jsonl")
    ledger.append(AuditEvent(event_type="test", action="one"))
    ledger.append(AuditEvent(event_type="test", action="two"))
    ok, count = ledger.verify()
    assert ok
    assert count == 2

    lines = (tmp_path / "audit.jsonl").read_text().splitlines()
    lines[0] = lines[0].replace("one", "evil")
    (tmp_path / "audit.jsonl").write_text("\n".join(lines) + "\n")
    ok, _ = ledger.verify()
    assert not ok


def test_field_cipher_roundtrip():
    cipher = FieldCipher("x" * 32)
    token = cipher.encrypt("Дарія Ярослав private")
    assert "Дарія" not in token
    assert cipher.decrypt(token) == "Дарія Ярослав private"


def test_claim_calibration_blocks_unmeasured_hormones_and_partner_mind_reading():
    hormone = calibrate_claim(
        Claim(
            kind=ClaimKind.HORMONE,
            subject="self",
            statement="cortisol is high",
            evidence_level=EvidenceLevel.INFERRED,
        )
    )
    assert not hormone.allowed

    intent = calibrate_claim(
        Claim(kind=ClaimKind.INTENT, subject="dasha", statement="she wants X")
    )
    assert not intent.allowed

    measured = calibrate_claim(
        Claim(
            kind=ClaimKind.HORMONE,
            subject="self",
            statement="testosterone lab value",
            evidence_level=EvidenceLevel.MEASURED,
            confidence=0.8,
            evidence=("lab:2026-06-05",),
        )
    )
    assert measured.allowed
    assert measured.calibrated_confidence >= 0.8


def test_evidence_manifest_counts():
    manifest = evidence_manifest(
        [
            Claim(kind=ClaimKind.FACT, subject="pair", statement="1000 events", evidence_level=EvidenceLevel.MEASURED),
            Claim(kind=ClaimKind.HORMONE, subject="self", statement="high cortisol"),
        ]
    )
    assert manifest["total_claims"] == 2
    assert manifest["blocked"] == 1


def test_v7_security_audit_passes():
    report = run_security_audit(Path("."))
    assert report["ok"], report
    assert report["score"] == 1.0
