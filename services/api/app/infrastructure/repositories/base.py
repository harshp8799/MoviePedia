"""Base for Firestore-backed repositories. Centralizes client access + doc->dict mapping.

Note: the Firebase Admin Firestore client is synchronous; these async methods call it directly.
That's fine at current scale (fast round-trips); wrap in a threadpool later if it ever matters.
"""

from __future__ import annotations

from typing import Any

from google.cloud.firestore_v1 import DocumentSnapshot

from app.infrastructure.firebase.admin import get_firestore


class FirestoreRepository:
    def __init__(self) -> None:
        self._db = get_firestore()

    @staticmethod
    def _to_dict(snap: DocumentSnapshot) -> dict[str, Any]:
        data = snap.to_dict() or {}
        data["id"] = snap.id
        return data
