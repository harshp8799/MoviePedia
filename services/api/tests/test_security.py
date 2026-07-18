"""Hardening tests: rate limiter logic, security headers, and 429 on burst."""

from app.core.rate_limit import RateLimiter
from app.main import app
from app.presentation.api.middleware.security import (
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
)
from fastapi import FastAPI
from fastapi.testclient import TestClient

client = TestClient(app)


def test_rate_limiter_allows_up_to_limit_then_blocks():
    limiter = RateLimiter(limit=3, window_seconds=60)
    assert [limiter.allow("ip", now=0) for _ in range(3)] == [True, True, True]
    assert limiter.allow("ip", now=0) is False


def test_rate_limiter_window_slides():
    limiter = RateLimiter(limit=1, window_seconds=10)
    assert limiter.allow("ip", now=0) is True
    assert limiter.allow("ip", now=5) is False  # still inside window
    assert limiter.allow("ip", now=11) is True  # window passed


def test_rate_limiter_is_per_key():
    limiter = RateLimiter(limit=1, window_seconds=60)
    assert limiter.allow("a", now=0) is True
    assert limiter.allow("b", now=0) is True  # different key, independent bucket


def test_security_headers_present():
    res = client.get("/api/v1/health")
    assert res.headers["x-content-type-options"] == "nosniff"
    assert res.headers["x-frame-options"] == "DENY"
    assert res.headers["referrer-policy"] == "no-referrer"


def test_rate_limit_middleware_returns_429_on_burst():
    isolated = FastAPI()
    isolated.add_middleware(SecurityHeadersMiddleware)
    isolated.add_middleware(RateLimitMiddleware, limiter=RateLimiter(limit=2, window_seconds=60))

    @isolated.get("/ping")
    async def ping():
        return {"ok": True}

    c = TestClient(isolated)
    assert c.get("/ping").status_code == 200
    assert c.get("/ping").status_code == 200
    res = c.get("/ping")
    assert res.status_code == 429
    assert res.json()["error"]["code"] == "rate_limited"
