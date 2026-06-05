from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from intentia_amoris.config import get_settings
from intentia_amoris.security.crypto import stable_sha256
from intentia_amoris.security.redaction import redact_mapping, redact_text
from intentia_amoris.security.validation import atomic_write_bytes


@dataclass(slots=True)
class AuditEvent:
    event_type: str
    actor: str = "system"
    action: str = ""
    target: str = ""
    request_id: str = ""
    allowed: bool = True
    reason: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class AuditLedger:
    """
    Append-only JSONL audit ledger with a tamper-evident hash chain.

    It is not a blockchain. It is a local integrity mechanism: if any line is edited or
    deleted, verification fails from that line onward.
    """

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or get_settings().audit_log_path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _last_hash(self) -> str:
        if not self.path.exists():
            return "0" * 64
        last = ""
        with open(self.path, "rb") as fh:
            for line in fh:
                if line.strip():
                    last = line.decode("utf-8")
        if not last:
            return "0" * 64
        try:
            return json.loads(last)["hash"]
        except Exception:
            return "<corrupt>"

    def append(self, event: AuditEvent) -> dict[str, Any]:
        payload = {
            "created_at": event.created_at,
            "event_type": redact_text(event.event_type, 128),
            "actor": redact_text(event.actor, 128),
            "action": redact_text(event.action, 128),
            "target": redact_text(event.target, 256),
            "request_id": redact_text(event.request_id, 128),
            "allowed": bool(event.allowed),
            "reason": redact_text(event.reason, 500),
            "metadata": redact_mapping(event.metadata),
            "prev_hash": self._last_hash(),
        }
        payload["hash"] = stable_sha256(canonical_json(payload))
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(canonical_json(payload) + "\n")
        return payload

    def verify(self) -> tuple[bool, int]:
        previous = "0" * 64
        count = 0
        if not self.path.exists():
            return True, 0
        with open(self.path, encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                count += 1
                payload = json.loads(line)
                observed_hash = payload.pop("hash")
                if payload.get("prev_hash") != previous:
                    return False, count
                expected = stable_sha256(canonical_json(payload))
                if observed_hash != expected:
                    return False, count
                previous = observed_hash
        return True, count

    def snapshot(self, output_path: Path) -> dict[str, Any]:
        ok, count = self.verify()
        data = {"ok": ok, "events": count, "ledger": str(self.path)}
        atomic_write_bytes(output_path, (canonical_json(data) + "\n").encode("utf-8"))
        return data
