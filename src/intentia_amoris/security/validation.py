from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

from intentia_amoris.config import get_settings

_SAFE_SLUG_RE = re.compile(r"[^a-zA-Z0-9._-]+")


class ValidationError(ValueError):
    pass


def safe_slug(value: str, fallback: str = "item") -> str:
    cleaned = _SAFE_SLUG_RE.sub("_", (value or "").strip())
    cleaned = cleaned.strip("._")
    return cleaned[:160] or fallback


def ensure_within_directory(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve()
    try:
        candidate_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValidationError("path traversal attempt blocked") from exc
    return candidate_resolved


def validate_event_content(content: str) -> str:
    settings = get_settings()
    if not content or not content.strip():
        raise ValidationError("event content cannot be empty")
    if len(content) > settings.max_content_chars:
        raise ValidationError(f"event content exceeds {settings.max_content_chars} characters")
    return content.strip()


def validate_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:
    settings = get_settings()
    if not metadata:
        return {}
    if len(metadata) > settings.max_metadata_keys:
        raise ValidationError(f"metadata exceeds {settings.max_metadata_keys} top-level keys")
    clean: dict[str, Any] = {}
    for key, value in metadata.items():
        k = safe_slug(str(key), "key")
        if isinstance(value, (str, int, float, bool)) or value is None:
            clean[k] = value
        elif isinstance(value, dict):
            clean[k] = {safe_slug(str(kk), "key"): vv for kk, vv in list(value.items())[:32]}
        elif isinstance(value, (list, tuple)):
            clean[k] = list(value)[:64]
        else:
            clean[k] = str(value)
    return clean


def validate_media_upload(data: bytes, filename: str) -> str:
    settings = get_settings()
    if not data:
        raise ValidationError("empty media upload")
    if len(data) > settings.max_media_bytes:
        raise ValidationError(f"media upload exceeds {settings.max_media_bytes} bytes")
    suffix = Path(filename or "upload.bin").suffix.lower()
    if suffix not in settings.parsed_media_extensions:
        raise ValidationError(f"media extension not allowed: {suffix or '<none>'}")
    return safe_slug(filename or "upload.bin", "upload.bin")


def atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "wb") as fh:
        fh.write(data)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)
