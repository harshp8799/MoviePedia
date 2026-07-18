"""Public catalog read use-cases — home rails, listings, detail, search, similar.

Returns only public-safe fields (internal fields like searchTokens/createdBy/timestamps are
stripped before leaving the API — no Firebase internals exposed, per the API design)."""

from __future__ import annotations

from typing import Any

from app.core.exceptions import NotFoundError
from app.domain.repositories.ports import ContentRepository, GenreRepository
from app.domain.value_objects.enums import ContentType

_SUMMARY_FIELDS = ("id", "type", "slug", "title", "releaseYear", "genres", "poster")
_FULL_EXTRA = (
    "originalTitle",
    "shortDescription",
    "fullDescription",
    "releaseDate",
    "durationMinutes",
    "ageRating",
    "languages",
    "countries",
    "backdrop",
    "trailer",
)
_CHILD_DROP = ("createdAt", "updatedAt")


def _summary(doc: dict[str, Any]) -> dict[str, Any]:
    return {k: doc.get(k) for k in _SUMMARY_FIELDS}


def _detail(doc: dict[str, Any]) -> dict[str, Any]:
    out = _summary(doc)
    out.update({k: doc.get(k) for k in _FULL_EXTRA})
    return out


def _child(doc: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in doc.items() if k not in _CHILD_DROP}


class PublicCatalogService:
    def __init__(self, content: ContentRepository, genres: GenreRepository) -> None:
        self._content = content
        self._genres = genres

    async def home(self) -> dict[str, Any]:
        sections = []
        for key, title, sort in (
            ("trending", "Trending", "trending"),
            ("popular", "Popular", "popularity"),
            ("recent", "Recently Added", "recent"),
        ):
            items, _ = await self._content.query_published(sort=sort, limit=12)
            sections.append({"key": key, "title": title, "items": [_summary(i) for i in items]})
        return {"sections": sections}

    async def list_content(
        self,
        content_type: ContentType,
        *,
        genre: str | None = None,
        sort: str = "popularity",
        cursor: str | None = None,
        limit: int = 24,
    ) -> dict[str, Any]:
        items, next_cursor = await self._content.query_published(
            content_type=content_type.value, genre=genre, sort=sort, cursor=cursor, limit=limit
        )
        return {"items": [_summary(i) for i in items], "nextCursor": next_cursor}

    async def get_detail(self, slug: str) -> dict[str, Any]:
        doc = await self._content.get_published_by_slug(slug)
        if not doc:
            raise NotFoundError("Content not found")
        detail = _detail(doc)

        if doc.get("type") == ContentType.SERIES.value:
            seasons = await self._content.list_seasons(doc["id"])
            for season in seasons:
                episodes = await self._content.list_episodes(doc["id"], season["id"])
                season["episodes"] = [_child(e) for e in episodes]
            detail["seasons"] = [_child(s) for s in seasons]

        similar = await self._content.similar_published(
            doc.get("genres", []), exclude_id=doc["id"], limit=12
        )
        detail["similar"] = [_summary(i) for i in similar]
        return detail

    async def search(self, query: str, *, content_type: str | None = None) -> dict[str, Any]:
        token = (query or "").strip().lower().split(" ")[0] if query else ""
        if not token:
            return {"items": []}
        items = await self._content.search_published(token, content_type=content_type)
        return {"items": [_summary(i) for i in items]}

    async def list_genres(self) -> dict[str, Any]:
        genres = await self._genres.list()
        return {"items": [{"id": g.get("id"), "name": g.get("name")} for g in genres]}
