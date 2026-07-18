"""Firestore adapter for the ContentRepository port (single `content` collection)."""

from __future__ import annotations

from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter

from app.domain.repositories.ports import ContentRepository
from app.domain.value_objects.enums import Visibility
from app.infrastructure.repositories.base import FirestoreRepository

_COLLECTION = "content"
_TS = firestore.SERVER_TIMESTAMP


class FirestoreContentRepository(FirestoreRepository, ContentRepository):
    def _col(self):
        return self._db.collection(_COLLECTION)

    async def get_by_id(self, content_id: str) -> dict[str, Any] | None:
        snap = self._col().document(content_id).get()
        return self._to_dict(snap) if snap.exists else None

    async def get_by_slug(self, slug: str) -> dict[str, Any] | None:
        query = self._col().where(filter=FieldFilter("slug", "==", slug)).limit(1)
        docs = list(query.stream())
        return self._to_dict(docs[0]) if docs else None

    async def create(self, data: dict[str, Any]) -> str:
        ref = self._col().document()
        ref.set({**data, "createdAt": _TS, "updatedAt": _TS, "publishedAt": None})
        return ref.id

    async def update(self, content_id: str, patch: dict[str, Any]) -> None:
        self._col().document(content_id).update({**patch, "updatedAt": _TS})

    async def set_visibility(self, content_id: str, visibility: str) -> None:
        patch: dict[str, Any] = {"visibility": visibility, "updatedAt": _TS}
        if visibility == Visibility.PUBLISHED.value:
            patch["publishedAt"] = _TS
        self._col().document(content_id).update(patch)

    async def list_published(
        self, *, content_type: str | None = None, limit: int = 24
    ) -> list[dict[str, Any]]:
        query = self._col().where(filter=FieldFilter("visibility", "==", "published"))
        if content_type:
            query = query.where(filter=FieldFilter("type", "==", content_type))
        return [self._to_dict(d) for d in query.limit(limit).stream()]

    async def list_all(
        self, *, content_type: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]:
        query = self._col()
        if content_type:
            query = query.where(filter=FieldFilter("type", "==", content_type))
        return [self._to_dict(d) for d in query.limit(limit).stream()]

    async def add_season(self, series_id: str, data: dict[str, Any]) -> str:
        ref = self._col().document(series_id).collection("seasons").document()
        ref.set({**data, "createdAt": _TS})
        return ref.id

    async def add_episode(self, series_id: str, season_id: str, data: dict[str, Any]) -> str:
        ref = (
            self._col()
            .document(series_id)
            .collection("seasons")
            .document(season_id)
            .collection("episodes")
            .document()
        )
        ref.set({**data, "createdAt": _TS})
        return ref.id
