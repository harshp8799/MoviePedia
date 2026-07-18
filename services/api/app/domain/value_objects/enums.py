"""Domain enums — the vocabulary. Mirror of packages/shared-config (kept in lockstep)."""

from __future__ import annotations

from enum import Enum


class ContentType(str, Enum):
    MOVIE = "movie"
    SERIES = "series"


class Visibility(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    USER = "user"
