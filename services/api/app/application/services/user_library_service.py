"""User-library use-cases: watchlist/favorites, recently-viewed history, watch progress.

Every operation is scoped to the caller's uid (owner-only). Denormalizes a small content
summary on write so library/history pages render without extra reads (no N+1)."""

from __future__ import annotations

from typing import Any

from app.core.exceptions import NotFoundError, ValidationError
from app.domain.repositories.ports import ContentRepository, UserLibraryRepository

_SUMMARY_FIELDS = ("type", "slug", "title", "releaseYear", "poster")
_LIST_TYPES = {"watchlist": "watchlist", "favorites": "favorite"}


def _summary_of(content: dict[str, Any]) -> dict[str, Any]:
    return {k: content.get(k) for k in _SUMMARY_FIELDS}


def _resolve_list_type(path_value: str) -> str:
    try:
        return _LIST_TYPES[path_value]
    except KeyError as exc:
        raise ValidationError(f"Unknown list: {path_value}") from exc


class UserLibraryService:
    def __init__(self, content: ContentRepository, library: UserLibraryRepository) -> None:
        self._content = content
        self._library = library

    async def _summary_or_404(self, content_id: str) -> dict[str, Any]:
        content = await self._content.get_by_id(content_id)
        if not content:
            raise NotFoundError("Content not found")
        return _summary_of(content)

    async def add_to_list(self, uid: str, list_path: str, content_id: str) -> dict[str, Any]:
        list_type = _resolve_list_type(list_path)
        summary = await self._summary_or_404(content_id)
        await self._library.add_item(uid, list_type, content_id, summary)
        return {"contentId": content_id, "listType": list_type, **summary}

    async def remove_from_list(self, uid: str, list_path: str, content_id: str) -> None:
        await self._library.remove_item(uid, _resolve_list_type(list_path), content_id)

    async def get_list(self, uid: str, list_path: str) -> dict[str, Any]:
        items = await self._library.list_items(uid, _resolve_list_type(list_path))
        return {"items": items}

    async def record_view(self, uid: str, content_id: str) -> dict[str, Any]:
        summary = await self._summary_or_404(content_id)
        await self._library.record_view(uid, content_id, summary)
        return {"contentId": content_id, **summary}

    async def get_history(self, uid: str) -> dict[str, Any]:
        return {"items": await self._library.list_history(uid)}

    async def set_progress(
        self, uid: str, content_id: str, position_sec: int, duration_sec: int
    ) -> dict[str, Any]:
        if duration_sec <= 0:
            raise ValidationError("durationSec must be positive")
        summary = await self._summary_or_404(content_id)
        position = max(0, min(position_sec, duration_sec))
        completed = position / duration_sec >= 0.95
        await self._library.upsert_progress(
            uid,
            content_id,
            {
                "positionSec": position,
                "durationSec": duration_sec,
                "completed": completed,
                **summary,
            },
        )
        return {"contentId": content_id, "positionSec": position, "completed": completed}

    async def get_continue_watching(self, uid: str) -> dict[str, Any]:
        return {"items": await self._library.list_progress(uid, incomplete_only=True)}
