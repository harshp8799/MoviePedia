"""Pure domain rules for catalog content. No framework/Firebase imports (ADR-002).

Covers slug generation, search-token derivation, the publish-workflow state machine, and
assembly of a content document body (timestamps are added by the repository layer).
"""

from __future__ import annotations

import re
from typing import Any

from app.core.exceptions import ConflictError, ValidationError
from app.domain.value_objects.enums import ContentType, Visibility

_SLUG_MAX = 80
_TOKEN_PREFIX_MAX = 8

# Allowed visibility transitions (publish workflow state machine).
_TRANSITIONS: dict[Visibility, set[Visibility]] = {
    Visibility.DRAFT: {Visibility.PUBLISHED, Visibility.ARCHIVED},
    Visibility.PUBLISHED: {Visibility.ARCHIVED, Visibility.DRAFT},
    Visibility.ARCHIVED: {Visibility.DRAFT, Visibility.PUBLISHED},
}


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:_SLUG_MAX]
    if not slug:
        raise ValidationError("Title does not produce a valid slug")
    return slug


def build_search_tokens(title: str, keywords: list[str] | None = None) -> list[str]:
    words = re.sub(r"[^a-z0-9\s]", " ", f"{title} {' '.join(keywords or [])}".lower()).split()
    tokens: set[str] = set()
    for word in words:
        for i in range(1, min(len(word), _TOKEN_PREFIX_MAX) + 1):
            tokens.add(word[:i])
    return sorted(tokens)


def validate_transition(current: str, target: str) -> None:
    """Raise ConflictError if moving from `current` visibility to `target` is not allowed."""
    try:
        cur, tgt = Visibility(current), Visibility(target)
    except ValueError as exc:
        raise ValidationError(f"Unknown visibility value: {exc}") from exc
    if cur == tgt:
        raise ConflictError(f"Content is already '{target}'")
    if tgt not in _TRANSITIONS[cur]:
        raise ConflictError(f"Cannot transition from '{current}' to '{target}'")


def assemble_content_doc(
    content_type: ContentType, payload: dict[str, Any], actor_uid: str
) -> dict[str, Any]:
    """Build a new content document body from a validated create payload.

    Server timestamps (createdAt/updatedAt/publishedAt) are set by the repository.
    """
    title = payload["title"]
    doc = {
        "type": content_type.value,
        "slug": payload.get("slug") or slugify(title),
        "title": title,
        "originalTitle": payload.get("originalTitle") or title,
        "shortDescription": payload.get("shortDescription", ""),
        "fullDescription": payload.get("fullDescription", ""),
        "releaseDate": payload.get("releaseDate"),
        "releaseYear": payload.get("releaseYear"),
        "durationMinutes": payload.get("durationMinutes"),
        "ageRating": payload.get("ageRating"),
        "genres": payload.get("genres", []),
        "languages": payload.get("languages", []),
        "countries": payload.get("countries", []),
        "poster": payload.get("poster"),
        "backdrop": payload.get("backdrop"),
        "trailer": payload.get("trailer"),
        "visibility": Visibility.DRAFT.value,  # everything starts as a draft
        "featured": False,
        "trendingScore": 0.0,
        "popularity": 0,
        "searchTokens": build_search_tokens(title, payload.get("genres", [])),
        "schemaVersion": 1,
        "createdBy": actor_uid,
        "updatedBy": actor_uid,
    }
    return doc
