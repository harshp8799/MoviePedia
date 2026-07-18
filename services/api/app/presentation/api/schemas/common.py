"""Shared response schemas: error envelope + cursor pagination. Mirrors the JS Zod schemas."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    """Consistent error envelope for every non-2xx response."""

    error: ErrorBody


class Page(BaseModel, Generic[T]):
    """Cursor-paginated list envelope for Firestore-backed reads."""

    items: list[T]
    nextCursor: str | None = None


class CurrentUser(BaseModel):
    """Authenticated principal resolved from a verified Firebase ID token."""

    uid: str
    email: str | None = None
    role: str = "user"
