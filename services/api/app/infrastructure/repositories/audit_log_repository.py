"""Firestore adapter for the AuditLogPort (`audit_logs`, append-only, server-only)."""

from __future__ import annotations

from typing import Any

from google.cloud import firestore
from google.cloud.firestore_v1 import Query

from app.domain.repositories.ports import AuditLogPort
from app.infrastructure.repositories.base import FirestoreRepository

_COLLECTION = "audit_logs"
_TS = firestore.SERVER_TIMESTAMP


class FirestoreAuditLogAdapter(FirestoreRepository, AuditLogPort):
    async def record(
        self,
        *,
        actor_uid: str,
        action: str,
        entity_type: str,
        entity_id: str,
        before: dict | None = None,
        after: dict | None = None,
    ) -> None:
        self._db.collection(_COLLECTION).document().set(
            {
                "actorUid": actor_uid,
                "action": action,
                "entityType": entity_type,
                "entityId": entity_id,
                "before": before,
                "after": after,
                "at": _TS,
            }
        )

    async def list(self, *, limit: int = 50) -> list[dict[str, Any]]:
        query = (
            self._db.collection(_COLLECTION)
            .order_by("at", direction=Query.DESCENDING)
            .limit(limit)
        )
        return [self._to_dict(d) for d in query.stream()]
