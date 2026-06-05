from __future__ import annotations

import re
from typing import Any

_TOKEN_RE = re.compile(r"(?i)(token|api[_-]?key|secret|password|authorization)\s*[:=]\s*([^\s,;]+)")
_EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
_PHONE_RE = re.compile(r"(?<!\d)(?:\+?\d[\d\s().-]{7,}\d)(?!\d)")
_LONG_HEX_RE = re.compile(r"\b[a-f0-9]{32,}\b", re.IGNORECASE)


def redact_text(text: str, max_chars: int = 1200) -> str:
    value = text or ""
    value = _TOKEN_RE.sub(lambda m: f"{m.group(1)}=<redacted>", value)
    value = _EMAIL_RE.sub("<email:redacted>", value)
    value = _PHONE_RE.sub("<phone:redacted>", value)
    value = _LONG_HEX_RE.sub("<hex:redacted>", value)
    if len(value) > max_chars:
        value = value[:max_chars] + "…<truncated>"
    return value


def redact_mapping(data: dict[str, Any] | None, max_depth: int = 3) -> dict[str, Any]:
    if not data:
        return {}

    def walk(obj: Any, depth: int) -> Any:
        if depth <= 0:
            return "<max-depth>"
        if isinstance(obj, str):
            return redact_text(obj)
        if isinstance(obj, (int, float, bool)) or obj is None:
            return obj
        if isinstance(obj, dict):
            result = {}
            for key, value in list(obj.items())[:64]:
                k = str(key)
                if any(word in k.lower() for word in ("token", "secret", "password", "api_key", "authorization")):
                    result[k] = "<redacted>"
                else:
                    result[k] = walk(value, depth - 1)
            return result
        if isinstance(obj, (list, tuple)):
            return [walk(x, depth - 1) for x in list(obj)[:64]]
        return redact_text(str(obj))

    return walk(data, max_depth)
