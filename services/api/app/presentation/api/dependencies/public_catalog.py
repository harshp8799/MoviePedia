"""DI for the public catalog read service (no auth required)."""

from __future__ import annotations

from app.application.services.public_catalog_service import PublicCatalogService
from app.infrastructure.repositories.content_repository import FirestoreContentRepository
from app.infrastructure.repositories.genre_repository import FirestoreGenreRepository


def get_public_catalog_service() -> PublicCatalogService:
    return PublicCatalogService(FirestoreContentRepository(), FirestoreGenreRepository())
