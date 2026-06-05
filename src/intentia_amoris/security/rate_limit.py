from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Deque

from fastapi import HTTPException, Request, status

from intentia_amoris.config import get_settings


@dataclass(slots=True)
class MemoryRateLimiter:
    per_minute: int
    buckets: dict[str, Deque[float]]

    @classmethod
    def from_settings(cls) -> "MemoryRateLimiter":
        return cls(per_minute=get_settings().request_rate_limit_per_minute, buckets=defaultdict(deque))

    def check(self, key: str, now: float | None = None) -> bool:
        current = now or time.time()
        bucket = self.buckets[key]
        cutoff = current - 60
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        if len(bucket) >= self.per_minute:
            return False
        bucket.append(current)
        return True


limiter = MemoryRateLimiter.from_settings()


async def rate_limit_dependency(request: Request) -> None:
    client = request.client.host if request.client else "unknown"
    key = f"{client}:{request.url.path}"
    if not limiter.check(key):
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="rate limit exceeded")
