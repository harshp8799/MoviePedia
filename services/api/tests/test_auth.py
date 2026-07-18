"""Authentication & authorization tests (Phase 4). Deny-by-default is the contract.

RBAC is tested by overriding get_current_user (no live Firebase needed). Token rejection is
tested against the real dependency: missing/malformed tokens must be refused with 401.
"""

import pytest
from app.main import app
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.schemas.common import CurrentUser
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture(autouse=True)
def _clear_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


def _as(role: str):
    return lambda: CurrentUser(uid="u1", email="u1@test", role=role)


# ---- token rejection (real dependency) ------------------------------------
def test_me_requires_a_token():
    res = client.get("/api/v1/users/me")
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "unauthorized"


def test_malformed_token_is_rejected():
    res = client.get("/api/v1/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "unauthorized"


def test_admin_route_requires_a_token():
    res = client.get("/api/v1/admin/ping")
    assert res.status_code == 401


# ---- role-based authorization (overridden principal) ----------------------
def test_me_ok_when_authenticated():
    app.dependency_overrides[get_current_user] = _as("user")
    res = client.get("/api/v1/users/me")
    assert res.status_code == 200
    assert res.json()["uid"] == "u1"


def test_normal_user_cannot_access_admin_route():
    app.dependency_overrides[get_current_user] = _as("user")
    res = client.get("/api/v1/admin/ping")
    assert res.status_code == 403
    body = res.json()
    assert body["error"]["code"] == "forbidden"
    assert body["error"]["details"]["actual"] == "user"


def test_editor_cannot_access_admin_only_route():
    app.dependency_overrides[get_current_user] = _as("editor")
    assert client.get("/api/v1/admin/ping").status_code == 403


def test_admin_can_access_admin_route():
    app.dependency_overrides[get_current_user] = _as("admin")
    res = client.get("/api/v1/admin/ping")
    assert res.status_code == 200
    assert res.json()["role"] == "admin"


def test_editor_and_admin_can_access_editorial_route():
    for role in ("editor", "admin"):
        app.dependency_overrides[get_current_user] = _as(role)
        assert client.get("/api/v1/admin/editorial").status_code == 200


def test_normal_user_cannot_access_editorial_route():
    app.dependency_overrides[get_current_user] = _as("user")
    assert client.get("/api/v1/admin/editorial").status_code == 403
