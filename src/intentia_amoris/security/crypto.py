from __future__ import annotations

import base64
import hashlib
import hmac
from dataclasses import dataclass

try:
    from cryptography.fernet import Fernet, InvalidToken
except Exception:  # pragma: no cover - cryptography is a declared production dependency
    Fernet = None  # type: ignore[assignment]
    InvalidToken = Exception  # type: ignore[assignment]


def stable_sha256(data: bytes | str) -> str:
    raw = data.encode("utf-8") if isinstance(data, str) else data
    return hashlib.sha256(raw).hexdigest()


def key_fingerprint(secret: str) -> str:
    return stable_sha256(secret)[:16]


def constant_time_match(candidate: str, allowed: set[str]) -> bool:
    if not candidate or not allowed:
        return False
    return any(hmac.compare_digest(candidate, item) for item in allowed)


def derive_fernet_key(secret: str) -> bytes:
    if len(secret) < 32:
        raise ValueError("secret must be at least 32 characters")
    digest = hashlib.sha256(secret.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)


@dataclass(frozen=True, slots=True)
class FieldCipher:
    """
    Deterministic interface for encrypting sensitive blobs at the application boundary.

    This is envelope-ready: the project can later replace the single Fernet key with KMS.
    """

    secret: str

    def encrypt(self, text: str) -> str:
        if Fernet is None:
            raise RuntimeError("cryptography is not installed")
        f = Fernet(derive_fernet_key(self.secret))
        return f.encrypt(text.encode("utf-8")).decode("utf-8")

    def decrypt(self, token: str) -> str:
        if Fernet is None:
            raise RuntimeError("cryptography is not installed")
        try:
            f = Fernet(derive_fernet_key(self.secret))
            return f.decrypt(token.encode("utf-8")).decode("utf-8")
        except InvalidToken as exc:
            raise ValueError("invalid encrypted payload") from exc
