from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header, HTTPException, Request, status

from intentia_amoris.config import get_settings
from intentia_amoris.security.audit import AuditEvent, AuditLedger
from intentia_amoris.security.crypto import constant_time_match, key_fingerprint


@dataclass(frozen=True, slots=True)
class Principal:
    subject: str
    scopes: tuple[str, ...] = ("read", "write")


async def require_api_key(
    request: Request,
    x_intentia_api_key: str | None = Header(default=None, alias="X-Intentia-API-Key"),
    x_aris_api_key: str | None = Header(default=None, alias="X-ARIS-API-Key"),
) -> Principal:
    settings = get_settings()
    if not settings.require_api_auth:
        if settings.env in {"staging", "prod"}:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="API auth cannot be disabled in staging/prod",
            )
        if not settings.allow_insecure_dev:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="insecure dev auth requires INTENTIA_ALLOW_INSECURE_DEV=true",
            )
        return Principal(subject="local-dev", scopes=("read", "write", "admin"))

    allowed = settings.parsed_api_keys
    supplied_key = x_intentia_api_key or x_aris_api_key or ""
    if not constant_time_match(supplied_key, allowed):
        AuditLedger().append(
            AuditEvent(
                event_type="auth.denied",
                actor="anonymous",
                action=f"{request.method} {request.url.path}",
                target="api",
                allowed=False,
                reason="invalid or missing API key",
                metadata={"client": request.client.host if request.client else "unknown"},
            )
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return Principal(subject=f"api-key:{key_fingerprint(supplied_key)}")


def require_scope(principal: Principal, scope: str) -> None:
    if scope not in principal.scopes and "admin" not in principal.scopes:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"missing scope: {scope}")
