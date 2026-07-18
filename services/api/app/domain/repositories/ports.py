"""Repository & service ports (interfaces). Infrastructure adapters implement these.

Domain and application layers depend ONLY on these abstractions — never on firebase_admin or any
concrete SDK (ADR-002). Concrete methods are added per feature in Phase 4+; this file establishes
the boundary and the naming.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ContentRepository(ABC):
    """Reads/writes the single `content` collection (movies + series)."""

    @abstractmethod
    async def get_by_id(self, content_id: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def get_by_slug(self, slug: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> str: ...

    @abstractmethod
    async def update(self, content_id: str, patch: dict[str, Any]) -> None: ...

    @abstractmethod
    async def set_visibility(self, content_id: str, visibility: str) -> None: ...

    @abstractmethod
    async def list_published(
        self, *, content_type: str | None = None, limit: int = 24
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def list_all(
        self, *, content_type: str | None = None, limit: int = 50
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def add_season(self, series_id: str, data: dict[str, Any]) -> str: ...

    @abstractmethod
    async def add_episode(self, series_id: str, season_id: str, data: dict[str, Any]) -> str: ...

    # ---- public reads (published only) -----------------------------------
    @abstractmethod
    async def get_published_by_slug(self, slug: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def query_published(
        self,
        *,
        content_type: str | None = None,
        genre: str | None = None,
        sort: str = "popularity",
        cursor: str | None = None,
        limit: int = 24,
    ) -> tuple[list[dict[str, Any]], str | None]: ...

    @abstractmethod
    async def search_published(
        self, token: str, *, content_type: str | None = None, limit: int = 24
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def similar_published(
        self, genres: list[str], *, exclude_id: str, limit: int = 12
    ) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def list_seasons(self, series_id: str) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def list_episodes(self, series_id: str, season_id: str) -> list[dict[str, Any]]: ...


class GenreRepository(ABC):
    """Reference-data collection `genres` keyed by slug."""

    @abstractmethod
    async def upsert(self, genre_id: str, data: dict[str, Any]) -> None: ...

    @abstractmethod
    async def list(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def delete(self, genre_id: str) -> None: ...


class UserLibraryRepository(ABC):
    """Per-user private data: watchlist/favorites, recently-viewed history, watch progress.

    All methods are scoped by `uid` (from the verified token) — a user can only ever touch
    their own data (owner-scoped by construction).
    """

    @abstractmethod
    async def add_item(self, uid: str, list_type: str, content_id: str, summary: dict) -> None: ...

    @abstractmethod
    async def remove_item(self, uid: str, list_type: str, content_id: str) -> None: ...

    @abstractmethod
    async def list_items(self, uid: str, list_type: str) -> list[dict[str, Any]]: ...

    @abstractmethod
    async def has_item(self, uid: str, list_type: str, content_id: str) -> bool: ...

    @abstractmethod
    async def upsert_progress(self, uid: str, content_id: str, data: dict) -> None: ...

    @abstractmethod
    async def list_progress(self, uid: str, *, incomplete_only: bool = True) -> list[dict]: ...

    @abstractmethod
    async def record_view(self, uid: str, content_id: str, summary: dict) -> None: ...

    @abstractmethod
    async def list_history(self, uid: str, *, limit: int = 50) -> list[dict[str, Any]]: ...


class SearchPort(ABC):
    """Search abstraction — Firestore-native now, swappable later (ADR-005)."""

    @abstractmethod
    async def search(self, query: str, *, filters: dict[str, Any], cursor: str | None): ...


class StoragePort(ABC):
    """Object storage — issues signed upload/playback URLs; never proxies bytes."""

    @abstractmethod
    async def signed_upload_url(self, path: str, content_type: str) -> str: ...

    @abstractmethod
    async def signed_playback_url(self, path: str, ttl_seconds: int) -> str: ...


class NotificationPort(ABC):
    """Push notifications (FCM)."""

    @abstractmethod
    async def send_to_token(self, token: str, title: str, body: str) -> None: ...


class AuthPort(ABC):
    """Identity verification + role claims (Firebase Auth Admin SDK)."""

    @abstractmethod
    async def verify_token(self, id_token: str) -> dict[str, Any]: ...

    @abstractmethod
    async def set_role(self, uid: str, role: str) -> None: ...


class AuditLogPort(ABC):
    """Append-only audit trail for admin mutations."""

    @abstractmethod
    async def record(self, *, actor_uid: str, action: str, entity_type: str, entity_id: str,
                     before: dict | None = None, after: dict | None = None) -> None: ...

    @abstractmethod
    async def list(self, *, limit: int = 50) -> list[dict[str, Any]]: ...
