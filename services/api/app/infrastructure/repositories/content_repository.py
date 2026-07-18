"""Firestore adapter for the ContentRepository port (single `content` collection)."""

from __future__ import annotations

from typing import Any

from google.cloud.firestore_v1 import FieldFilter

from app.domain.repositories.ports import ContentRepository
from app.infrastructure.repositories.base import FirestoreRepository

_COLLECTION = "content"


class FirestoreContentRepository(FirestoreRepository, ContentRepository):
    async def get_by_slug(self, slug: str) -> dict[str, Any] | None:
        query = (
            self._db.collection(_COLLECTION)
            .where(filter=FieldFilter("slug", "==", slug))
            .limit(1)
        )
        docs = list(query.stream())
        return self._to_dict(docs[0]) if docs else None

    async def create(self, data: dict[str, Any]) -> str:
        ref = self._db.collection(_COLLECTION).document()
        ref.set(data)
        return ref.id

    async def list_published(
        self, *, content_type: str | None = None, limit: int = 24
    ) -> list[dict[str, Any]]:
        query = self._db.collection(_COLLECTION).where(
            filter=FieldFilter("visibility", "==", "published")
        )
        if content_type:
            query = query.where(filter=FieldFilter("type", "==", content_type))
        query = query.limit(limit)
        return [self._to_dict(d) for d in query.stream()]
