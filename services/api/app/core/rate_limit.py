"""In-memory sliding-window rate limiter.

Per-process (fine for a single Cloud Run/Render instance MVP); swap for a Redis-backed limiter
when horizontally scaled. Pure and injectable-clock for testing.
"""

from __future__ import annotations

import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, limit: int, window_seconds: float = 60.0) -> None:
        self.limit = limit
        self.window = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def allow(self, key: str, now: float | None = None) -> bool:
        now = time.monotonic() if now is None else now
        bucket = self._hits[key]
        cutoff = now - self.window
        # drop timestamps outside the window
        i = 0
        while i < len(bucket) and bucket[i] < cutoff:
            i += 1
        if i:
            del bucket[:i]
        if len(bucket) >= self.limit:
            return False
        bucket.append(now)
        return True
