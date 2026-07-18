"""Admin catalog API tests using in-memory fakes (no live Firebase).

Covers RBAC (user denied, editor/admin allowed), the publish workflow state machine, audit
logging on mutations, and upload-URL validation.
"""

from typing import Any

import pytest
from app.application.services.catalog_service import CatalogService
from app.domain.repositories.ports import (
    AuditLogPort,
    ContentRepository,
    GenreRepository,
    StoragePort,
)
from app.main import app
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.dependencies.catalog import get_catalog_service
from app.presentation.api.schemas.common import CurrentUser
from fastapi.testclient import TestClient

client = TestClient(app)


# ---- in-memory fakes ------------------------------------------------------
class FakeContent(ContentRepository):
    def __init__(self) -> None:
        self.docs: dict[str, dict] = {}
        self._n = 0

    async def get_by_id(self, cid: str):
        return {**self.docs[cid], "id": cid} if cid in self.docs else None

    async def get_by_slug(self, slug: str):
        for cid, d in self.docs.items():
            if d.get("slug") == slug:
                return {**d, "id": cid}
        return None

    async def create(self, data: dict[str, Any]) -> str:
        self._n += 1
        cid = f"c{self._n}"
        self.docs[cid] = dict(data)
        return cid

    async def update(self, cid: str, patch: dict[str, Any]) -> None:
        self.docs[cid].update(patch)

    async def set_visibility(self, cid: str, visibility: str) -> None:
        self.docs[cid]["visibility"] = visibility

    async def list_published(self, *, content_type=None, limit=24):
        return [
            {**d, "id": k}
            for k, d in self.docs.items()
            if d.get("visibility") == "published"
            and (not content_type or d.get("type") == content_type)
        ]

    async def list_all(self, *, content_type=None, limit=50):
        return [
            {**d, "id": k}
            for k, d in self.docs.items()
            if not content_type or d.get("type") == content_type
        ]

    async def add_season(self, series_id: str, data: dict[str, Any]) -> str:
        self._n += 1
        return f"s{self._n}"

    async def add_episode(self, series_id: str, season_id: str, data: dict[str, Any]) -> str:
        self._n += 1
        return f"e{self._n}"


class FakeGenre(GenreRepository):
    def __init__(self) -> None:
        self.g: dict[str, dict] = {}

    async def upsert(self, gid: str, data: dict[str, Any]) -> None:
        self.g[gid] = data

    async def list(self):
        return list(self.g.values())

    async def delete(self, gid: str) -> None:
        self.g.pop(gid, None)


class FakeStorage(StoragePort):
    async def signed_upload_url(self, path: str, content_type: str) -> str:
        return f"http://upload.test/{path}"

    async def signed_playback_url(self, path: str, ttl_seconds: int) -> str:
        return f"http://play.test/{path}"


class FakeAudit(AuditLogPort):
    def __init__(self) -> None:
        self.records: list[dict] = []

    async def record(self, **kwargs) -> None:
        self.records.append(kwargs)


@pytest.fixture
def svc():
    return CatalogService(FakeContent(), FakeGenre(), FakeStorage(), FakeAudit())


@pytest.fixture(autouse=True)
def _wire(svc):
    app.dependency_overrides[get_catalog_service] = lambda: svc
    yield
    app.dependency_overrides.clear()


def _login(role: str):
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid="actor1", role=role)


# ---- RBAC -----------------------------------------------------------------
def test_normal_user_cannot_create_movie():
    _login("user")
    res = client.post("/api/v1/admin/movies", json={"title": "X"})
    assert res.status_code == 403


def test_editor_can_create_movie_as_draft(svc):
    _login("editor")
    res = client.post("/api/v1/admin/movies", json={"title": "Neon Horizon", "genres": ["sci-fi"]})
    assert res.status_code == 201
    body = res.json()
    assert body["visibility"] == "draft"
    assert body["slug"] == "neon-horizon"
    assert any(r["action"] == "movie.create" for r in svc._audit.records)


# ---- publish workflow -----------------------------------------------------
def test_publish_then_archive_flow(svc):
    _login("editor")
    cid = client.post("/api/v1/admin/movies", json={"title": "Flow"}).json()["id"]

    assert client.post(f"/api/v1/admin/content/{cid}/publish").status_code == 200
    # publishing again is a conflict (already published)
    assert client.post(f"/api/v1/admin/content/{cid}/publish").status_code == 409
    assert client.post(f"/api/v1/admin/content/{cid}/archive").status_code == 200


def test_publish_unknown_content_is_404():
    _login("editor")
    assert client.post("/api/v1/admin/content/nope/publish").status_code == 404


# ---- genre delete is admin-only ------------------------------------------
def test_genre_delete_requires_admin():
    _login("editor")
    client.post("/api/v1/admin/genres", json={"name": "Action"})
    assert client.delete("/api/v1/admin/genres/action").status_code == 403
    _login("admin")
    assert client.delete("/api/v1/admin/genres/action").status_code == 200


# ---- upload url validation -----------------------------------------------
def test_upload_url_accepts_valid_image(svc):
    _login("editor")
    res = client.post(
        "/api/v1/admin/media/upload-url",
        json={
            "kind": "poster",
            "contentId": "c1",
            "filename": "p.jpg",
            "contentType": "image/jpeg",
        },
    )
    assert res.status_code == 200
    assert res.json()["path"].startswith("public/poster/c1/")


def test_upload_url_rejects_wrong_content_type():
    _login("editor")
    res = client.post(
        "/api/v1/admin/media/upload-url",
        json={
            "kind": "poster",
            "contentId": "c1",
            "filename": "p.exe",
            "contentType": "application/x-msdownload",
        },
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "validation_error"
