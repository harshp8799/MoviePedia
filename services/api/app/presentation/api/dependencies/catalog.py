"""DI wiring for the catalog service — constructs it from the Firestore adapters.

Tests override get_catalog_service() with a fake using in-memory repositories.
"""

from __future__ import annotations

from app.application.services.catalog_service import CatalogService
from app.infrastructure.repositories.audit_log_repository import FirestoreAuditLogAdapter
from app.infrastructure.repositories.content_repository import FirestoreContentRepository
from app.infrastructure.repositories.genre_repository import FirestoreGenreRepository
from app.infrastructure.storage.storage_adapter import FirebaseStorageAdapter


def get_catalog_service() -> CatalogService:
    return CatalogService(
        content=FirestoreContentRepository(),
        genres=FirestoreGenreRepository(),
        storage=FirebaseStorageAdapter(),
        audit=FirestoreAuditLogAdapter(),
    )
