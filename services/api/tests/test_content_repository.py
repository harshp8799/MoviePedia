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
