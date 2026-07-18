"""DI for the user-library service."""

from __future__ import annotations

from app.application.services.user_library_service import UserLibraryService
from app.infrastructure.repositories.content_repository import FirestoreContentRepository
from app.infrastructure.repositories.user_library_repository import FirestoreUserLibraryRepository


def get_user_library_service() -> UserLibraryService:
    return UserLibraryService(FirestoreContentRepository(), FirestoreUserLibraryRepository())
