"""Firestore ContentRepository adapter — emulator-gated integration smoke test.

Skips automatically unless the Firestore emulator is reachable. Run it with:
    firebase emulators:exec --only firestore "cd services/api && ../../.venv/bin/pytest -q"
"""

import asyncio
import os
import socket

import pytest


def _emulator_up() -> bool:
    host = os.environ.get("FIRESTORE_EMULATOR_HOST", "")
    if not host:
        return False
    h, _, p = host.partition(":")
    try:
        socket.create_connection((h or "localhost", int(p or "8080")), timeout=0.5).close()
        return True
    except OSError:
        return False


pytestmark = pytest.mark.skipif(not _emulator_up(), reason="Firestore emulator not running")


def test_create_get_and_list_published():
    from app.infrastructure.repositories.content_repository import FirestoreContentRepository

    repo = FirestoreContentRepository()

    async def scenario():
        cid = await repo.create(
            {
                "type": "movie",
                "slug": "phase4-smoke",
                "title": "Phase 4 Smoke",
                "visibility": "published",
            }
        )
        got = await repo.get_by_slug("phase4-smoke")
        published = await repo.list_published(content_type="movie", limit=50)
        return cid, got, published

    cid, got, published = asyncio.run(scenario())

    assert cid
    assert got is not None and got["slug"] == "phase4-smoke"
    assert any(item["slug"] == "phase4-smoke" for item in published)


def test_catalog_service_publish_flow_end_to_end():
    from app.domain.value_objects.enums import ContentType, Visibility
    from app.presentation.api.dependencies.catalog import get_catalog_service

    svc = get_catalog_service()

    async def scenario():
        created = await svc.create_content(
            "actor1", ContentType.MOVIE, {"title": "E2E Publish Test", "genres": ["drama"]}
        )
        cid = created["id"]
        published = await svc.change_visibility("actor1", cid, Visibility.PUBLISHED)
        listed = await svc.list_catalog(content_type="movie")
        return cid, published, listed

    cid, published, listed = asyncio.run(scenario())
    assert published["visibility"] == "published"
    assert any(item["id"] == cid for item in listed)


def test_public_catalog_reads_published_only():
    from app.application.services.public_catalog_service import PublicCatalogService
    from app.domain.value_objects.enums import ContentType, Visibility
    from app.infrastructure.repositories.content_repository import FirestoreContentRepository
    from app.infrastructure.repositories.genre_repository import FirestoreGenreRepository

    content = FirestoreContentRepository()
    svc = PublicCatalogService(content, FirestoreGenreRepository())

    async def scenario():
        pub = await content.create(
            {
                "type": "movie",
                "slug": "pub-movie-6",
                "title": "Pub Movie",
                "visibility": "published",
                "genres": ["drama"],
                "searchTokens": ["pub"],
                "popularity": 10,
            }
        )
        await content.set_visibility(pub, Visibility.PUBLISHED.value)
        await content.create(
            {"type": "movie", "slug": "draft-movie-6", "title": "Draft", "visibility": "draft"}
        )
        listed = await svc.list_content(ContentType.MOVIE, limit=50)
        detail = await svc.get_detail("pub-movie-6")
        return listed, detail

    listed, detail = asyncio.run(scenario())
    slugs = [i["slug"] for i in listed["items"]]
    assert "pub-movie-6" in slugs
    assert "draft-movie-6" not in slugs
    assert detail["slug"] == "pub-movie-6"
    assert "searchTokens" not in detail


def test_user_library_flow_end_to_end():
    from app.application.services.user_library_service import UserLibraryService
    from app.infrastructure.repositories.content_repository import FirestoreContentRepository
    from app.infrastructure.repositories.user_library_repository import (
        FirestoreUserLibraryRepository,
    )

    content = FirestoreContentRepository()
    svc = UserLibraryService(content, FirestoreUserLibraryRepository())

    async def scenario():
        cid = await content.create(
            {"type": "movie", "slug": "lib-e2e", "title": "Lib E2E", "visibility": "published"}
        )
        await svc.add_to_list("userX", "watchlist", cid)
        watchlist = await svc.get_list("userX", "watchlist")
        await svc.set_progress("userX", cid, 10, 100)
        continue_watching = await svc.get_continue_watching("userX")
        await svc.remove_from_list("userX", "watchlist", cid)
        after = await svc.get_list("userX", "watchlist")
        return cid, watchlist, continue_watching, after

    cid, watchlist, continue_watching, after = asyncio.run(scenario())
    assert any(i["contentId"] == cid for i in watchlist["items"])
    assert any(i["contentId"] == cid for i in continue_watching["items"])
    assert after["items"] == []
