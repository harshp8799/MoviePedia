"""Firestore adapter for the GenreRepository port (`genres` collection, keyed by slug)."""

from __future__ import annotations

from typing import Any

from google.cloud import firestore

from app.domain.repositories.ports import GenreRepository
from app.infrastructure.repositories.base import FirestoreRepository

_COLLECTION = "genres"
_TS = firestore.SERVER_TIMESTAMP


class FirestoreGenreRepository(FirestoreRepository, GenreRepository):
    async def upsert(self, genre_id: str, data: dict[str, Any]) -> None:
        self._db.collection(_COLLECTION).document(genre_id).set(
            {**data, "updatedAt": _TS}, merge=True
        )

    async def list(self) -> list[dict[str, Any]]:
        return [self._to_dict(d) for d in self._db.collection(_COLLECTION).stream()]

    async def delete(self, genre_id: str) -> None:
        self._db.collection(_COLLECTION).document(genre_id).delete()
