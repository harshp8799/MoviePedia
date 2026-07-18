"""User-library API tests — owner scoping, watchlist/history/progress, auth. In-memory fakes."""

import pytest
from app.application.services.user_library_service import UserLibraryService
from app.main import app
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.dependencies.library import get_user_library_service
from app.presentation.api.schemas.common import CurrentUser
from fastapi.testclient import TestClient

client = TestClient(app)

_CONTENT = {
    "c1": {
        "type": "movie",
        "slug": "m1",
        "title": "Movie One",
        "releaseYear": 2020,
        "poster": None,
    },
}


class FakeContent:
    async def get_by_id(self, cid):
        return _CONTENT.get(cid)


class FakeLibrary:
    def __init__(self):
        self.items = {}
        self.progress = {}
        self.history = {}

    async def add_item(self, uid, lt, cid, summary):
        self.items[(uid, lt, cid)] = {"contentId": cid, "listType": lt, **summary}

    async def remove_item(self, uid, lt, cid):
        self.items.pop((uid, lt, cid), None)

    async def list_items(self, uid, lt):
        return [v for (u, m, c), v in self.items.items() if u == uid and m == lt]

    async def has_item(self, uid, lt, cid):
        return (uid, lt, cid) in self.items

    async def upsert_progress(self, uid, cid, data):
        self.progress[(uid, cid)] = {"contentId": cid, **data}

    async def list_progress(self, uid, *, incomplete_only=True):
        return [
            v
            for (u, c), v in self.progress.items()
            if u == uid and (not incomplete_only or not v.get("completed"))
        ]

    async def record_view(self, uid, cid, summary):
        self.history[(uid, cid)] = {"contentId": cid, **summary}

    async def list_history(self, uid, *, limit=50):
        return [v for (u, c), v in self.history.items() if u == uid][:limit]


@pytest.fixture
def svc():
    return UserLibraryService(FakeContent(), FakeLibrary())


@pytest.fixture(autouse=True)
def _wire(svc):
    app.dependency_overrides[get_user_library_service] = lambda: svc
    yield
    app.dependency_overrides.clear()


def _login(uid, role="user"):
    app.dependency_overrides[get_current_user] = lambda: CurrentUser(uid=uid, role=role)


def test_library_requires_auth():
    assert client.get("/api/v1/library/watchlist").status_code == 401


def test_add_list_and_remove_watchlist():
    _login("userA")
    assert client.post("/api/v1/library/watchlist", json={"contentId": "c1"}).status_code == 201
    listed = client.get("/api/v1/library/watchlist").json()
    assert [i["contentId"] for i in listed["items"]] == ["c1"]
    assert client.delete("/api/v1/library/watchlist/c1").status_code == 200
    assert client.get("/api/v1/library/watchlist").json()["items"] == []


def test_add_unknown_content_is_404():
    _login("userA")
    assert client.post("/api/v1/library/watchlist", json={"contentId": "nope"}).status_code == 404


def test_users_have_separate_libraries():
    _login("userA")
    client.post("/api/v1/library/watchlist", json={"contentId": "c1"})
    _login("userB")
    assert client.get("/api/v1/library/watchlist").json()["items"] == []


def test_invalid_list_type_rejected():
    _login("userA")
    assert client.get("/api/v1/library/badtype").status_code == 422


def test_progress_and_continue_watching():
    _login("userA")
    # 30% watched -> not completed -> shows in continue-watching
    r = client.put("/api/v1/progress/c1", json={"positionSec": 30, "durationSec": 100})
    assert r.status_code == 200 and r.json()["completed"] is False
    cw = client.get("/api/v1/progress").json()
    assert [i["contentId"] for i in cw["items"]] == ["c1"]
    # 99% watched -> completed -> drops out of continue-watching
    client.put("/api/v1/progress/c1", json={"positionSec": 99, "durationSec": 100})
    assert client.get("/api/v1/progress").json()["items"] == []


def test_history_records_view():
    _login("userA")
    assert client.post("/api/v1/history", json={"contentId": "c1"}).status_code == 201
    assert [i["contentId"] for i in client.get("/api/v1/history").json()["items"]] == ["c1"]
