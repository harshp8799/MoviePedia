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
    async def get_by_slug(self, slug: str) -> dict[str, Any] | None: ...

    @abstractmethod
    async def create(self, data: dict[str, Any]) -> str: ...


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
