from __future__ import annotations

import hashlib
from pathlib import Path

from intentia_amoris.config import get_settings
from intentia_amoris.security.validation import (
    atomic_write_bytes,
    ensure_within_directory,
    safe_slug,
    validate_media_upload,
)


async def store_media_bytes(data: bytes, filename: str, actor: str, kind: str) -> tuple[str, str]:
    settings = get_settings()
    safe_filename = validate_media_upload(data, filename)
    safe_actor = safe_slug(actor, "unknown")
    safe_kind = safe_slug(kind, "media")
    sha = hashlib.sha256(data).hexdigest()

    folder = ensure_within_directory(settings.media_root, settings.media_root / safe_actor / safe_kind)
    path = folder / f"{sha[:16]}_{safe_filename}"
    final_path = ensure_within_directory(settings.media_root, path)
    atomic_write_bytes(final_path, data)
    return str(final_path), sha


def build_media_description_stub(kind: str, caption: str, metadata: dict | None = None) -> str:
    """
    Placeholder for a VLM adapter.

    Production invariant:
    - factual description first;
    - emotional interpretation explicitly marked inferred;
    - no identity/consent/intent inference from pixels alone.
    """
    meta = metadata or {}
    parts = [f"media_kind={safe_slug(kind, 'media')}"]
    if caption:
        parts.append(f"caption={caption[:500]}")
    if meta:
        parts.append(f"metadata_keys={sorted(meta.keys())[:12]}")
    parts.append("vlm_status=not_configured")
    parts.append("evidence_level=inferred")
    return "; ".join(parts)
