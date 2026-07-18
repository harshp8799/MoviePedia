"""Firestore adapter for the ContentRepository port (single `content` collection)."""

from __future__ import annotations

from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter, Query

from app.domain.repositories.ports import ContentRepository
from app.domain.value_objects.enums import Visibility
from app.infrastructure.repositories.base import FirestoreRepository

_COLLECTION = "content"
_TS = firestore.SERVER_TIMESTAMP
_SORT_FIELDS = {
    "popularity": "popularity",
    "recent": "publishedAt",
    "trending": "trendingScore",
    "release": "releaseYear",
}


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

    # ---- public reads (published only) -----------------------------------
    async def get_published_by_slug(self, slug: str) -> dict[str, Any] | None:
        doc = await self.get_by_slug(slug)
        return doc if doc and doc.get("visibility") == Visibility.PUBLISHED.value else None

    async def query_published(
        self,
        *,
        content_type: str | None = None,
        genre: str | None = None,
        sort: str = "popularity",
        cursor: str | None = None,
        limit: int = 24,
    ) -> tuple[list[dict[str, Any]], str | None]:
        field = _SORT_FIELDS.get(sort, "popularity")
        query = self._col().where(filter=FieldFilter("visibility", "==", "published"))
        if content_type:
            query = query.where(filter=FieldFilter("type", "==", content_type))
        if genre:
            query = query.where(filter=FieldFilter("genres", "array_contains", genre))
        query = query.order_by(field, direction=Query.DESCENDING).order_by("__name__")
        if cursor:
            snap = self._col().document(cursor).get()
            if snap.exists:
                query = query.start_after(snap)
        docs = list(query.limit(limit + 1).stream())
        next_cursor = docs[limit - 1].id if len(docs) > limit else None
        return [self._to_dict(d) for d in docs[:limit]], next_cursor

    async def search_published(
        self, token: str, *, content_type: str | None = None, limit: int = 24
    ) -> list[dict[str, Any]]:
        query = self._col().where(
            filter=FieldFilter("searchTokens", "array_contains", token.lower())
        )
        query = query.where(filter=FieldFilter("visibility", "==", "published"))
        if content_type:
            query = query.where(filter=FieldFilter("type", "==", content_type))
        return [self._to_dict(d) for d in query.limit(limit).stream()]

    async def similar_published(
        self, genres: list[str], *, exclude_id: str, limit: int = 12
    ) -> list[dict[str, Any]]:
        if not genres:
            return []
        query = (
            self._col()
            .where(filter=FieldFilter("genres", "array_contains_any", genres[:10]))
            .where(filter=FieldFilter("visibility", "==", "published"))
            .limit(limit + 1)
        )
        items = [self._to_dict(d) for d in query.stream() if d.id != exclude_id]
        return items[:limit]

    async def list_seasons(self, series_id: str) -> list[dict[str, Any]]:
        query = self._col().document(series_id).collection("seasons").order_by("seasonNumber")
        return [self._to_dict(d) for d in query.stream()]

    async def list_episodes(self, series_id: str, season_id: str) -> list[dict[str, Any]]:
        query = (
            self._col()
            .document(series_id)
            .collection("seasons")
            .document(season_id)
            .collection("episodes")
            .order_by("episodeNumber")
        )
        return [self._to_dict(d) for d in query.stream()]
