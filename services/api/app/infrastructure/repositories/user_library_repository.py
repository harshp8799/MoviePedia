"""Firestore adapter for UserLibraryRepository — per-user subcollections, owner-scoped.

Layout (see docs/FIRESTORE.md):
  user_libraries/{uid}/items/{listType__contentId}
  watch_progress/{uid}/items/{contentId}
  viewing_history/{uid}/items/{contentId}   (one entry per title, updated on re-view)
"""

from __future__ import annotations

from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1 import FieldFilter, Query

from app.domain.repositories.ports import UserLibraryRepository
from app.infrastructure.repositories.base import FirestoreRepository

_TS = firestore.SERVER_TIMESTAMP


class FirestoreUserLibraryRepository(FirestoreRepository, UserLibraryRepository):
    def _items(self, uid: str):
        return self._db.collection("user_libraries").document(uid).collection("items")

    def _progress(self, uid: str):
        return self._db.collection("watch_progress").document(uid).collection("items")

    def _history(self, uid: str):
        return self._db.collection("viewing_history").document(uid).collection("items")

    async def add_item(self, uid: str, list_type: str, content_id: str, summary: dict) -> None:
        doc_id = f"{list_type}__{content_id}"
        self._items(uid).document(doc_id).set(
            {"contentId": content_id, "listType": list_type, "addedAt": _TS, **summary}
        )

    async def remove_item(self, uid: str, list_type: str, content_id: str) -> None:
        self._items(uid).document(f"{list_type}__{content_id}").delete()

    async def list_items(self, uid: str, list_type: str) -> list[dict[str, Any]]:
        query = self._items(uid).where(filter=FieldFilter("listType", "==", list_type))
        return [self._to_dict(d) for d in query.stream()]

    async def has_item(self, uid: str, list_type: str, content_id: str) -> bool:
        return self._items(uid).document(f"{list_type}__{content_id}").get().exists

    async def upsert_progress(self, uid: str, content_id: str, data: dict) -> None:
        self._progress(uid).document(content_id).set(
            {"contentId": content_id, **data, "updatedAt": _TS}, merge=True
        )

    async def list_progress(self, uid: str, *, incomplete_only: bool = True) -> list[dict]:
        query = self._progress(uid)
        if incomplete_only:
            query = query.where(filter=FieldFilter("completed", "==", False))
        query = query.order_by("updatedAt", direction=Query.DESCENDING).limit(30)
        return [self._to_dict(d) for d in query.stream()]

    async def record_view(self, uid: str, content_id: str, summary: dict) -> None:
        self._history(uid).document(content_id).set(
            {"contentId": content_id, "viewedAt": _TS, **summary}
        )

    async def list_history(self, uid: str, *, limit: int = 50) -> list[dict[str, Any]]:
        query = self._history(uid).order_by("viewedAt", direction=Query.DESCENDING).limit(limit)
        return [self._to_dict(d) for d in query.stream()]
