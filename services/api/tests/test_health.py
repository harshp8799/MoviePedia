"""Smoke test — the app boots and health/readiness respond. Phase 2 validation."""

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_ok():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    body = res.json()
    assert body["status"] == "ok"
    assert body["service"] == "movie-pedia-api"


def test_ready_ok():
    res = client.get("/api/v1/ready")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"
