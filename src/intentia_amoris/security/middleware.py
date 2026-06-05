from __future__ import annotations

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response

from intentia_amoris.security.audit import AuditEvent, AuditLedger


async def security_headers_middleware(request: Request, call_next: Callable) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Cache-Control"] = "no-store"

    if request.url.path not in {"/health", "/ready"}:
        AuditLedger().append(
            AuditEvent(
                event_type="http.request",
                action=f"{request.method} {request.url.path}",
                request_id=request_id,
                allowed=response.status_code < 400,
                metadata={"status_code": response.status_code, "elapsed_ms": elapsed_ms},
            )
        )

    return response
