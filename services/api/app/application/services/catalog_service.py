"""Catalog application service — use-cases for genres, content, seasons/episodes, publish
workflow, and media upload URLs. Depends only on ports (ADR-002); writes an audit log on every
mutation (ADR-003 / observability)."""

from __future__ import annotations

from typing import Any

from app.core.exceptions import NotFoundError, ValidationError
from app.domain.repositories.ports import (
    AuditLogPort,
    ContentRepository,
    GenreRepository,
    StoragePort,
)
from app.domain.services import content_rules
from app.domain.value_objects.enums import ContentType, Visibility

# Upload validation (mirrors packages/shared-config UPLOAD_LIMITS).
_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
_VIDEO_TYPES = {"video/mp4", "video/webm"}
_KIND_TYPES = {
    "poster": _IMAGE_TYPES,
    "backdrop": _IMAGE_TYPES,
    "trailer": _VIDEO_TYPES,
    "video": _VIDEO_TYPES,
}


class CatalogService:
    def __init__(
        self,
        content: ContentRepository,
        genres: GenreRepository,
        storage: StoragePort,
        audit: AuditLogPort,
    ) -> None:
        self._content = content
        self._genres = genres
        self._storage = storage
        self._audit = audit

    # ---- genres -----------------------------------------------------------
    async def create_genre(self, actor: str, name: str) -> dict[str, Any]:
        genre_id = content_rules.slugify(name)
        await self._genres.upsert(genre_id, {"id": genre_id, "name": name})
        await self._audit.record(
            actor_uid=actor, action="genre.upsert", entity_type="genre", entity_id=genre_id
        )
        return {"id": genre_id, "name": name}

    async def list_genres(self) -> list[dict[str, Any]]:
        return await self._genres.list()

    async def delete_genre(self, actor: str, genre_id: str) -> None:
        await self._genres.delete(genre_id)
        await self._audit.record(
            actor_uid=actor, action="genre.delete", entity_type="genre", entity_id=genre_id
        )

    # ---- content (movies & series) ---------------------------------------
    async def create_content(
        self, actor: str, content_type: ContentType, payload: dict[str, Any]
    ) -> dict[str, Any]:
        doc = content_rules.assemble_content_doc(content_type, payload, actor)
        content_id = await self._content.create(doc)
        await self._audit.record(
            actor_uid=actor,
            action=f"{content_type.value}.create",
            entity_type="content",
            entity_id=content_id,
            after={"slug": doc["slug"], "title": doc["title"]},
        )
        return {"id": content_id, **doc}

    async def update_content(
        self, actor: str, content_id: str, patch: dict[str, Any]
    ) -> dict[str, Any]:
        existing = await self._content.get_by_id(content_id)
        if not existing:
            raise NotFoundError("Content not found")

        clean = {k: v for k, v in patch.items() if v is not None}
        clean["updatedBy"] = actor
        if "title" in clean:
            genres = clean.get("genres", existing.get("genres", []))
            clean["searchTokens"] = content_rules.build_search_tokens(clean["title"], genres)
        await self._content.update(content_id, clean)
        await self._audit.record(
            actor_uid=actor,
            action="content.update",
            entity_type="content",
            entity_id=content_id,
            after={"fields": sorted(clean.keys())},
        )
        return {"id": content_id, **existing, **clean}

    async def change_visibility(
        self, actor: str, content_id: str, target: Visibility
    ) -> dict[str, Any]:
        existing = await self._content.get_by_id(content_id)
        if not existing:
            raise NotFoundError("Content not found")
        current = existing.get("visibility", Visibility.DRAFT.value)
        content_rules.validate_transition(current, target.value)
        await self._content.set_visibility(content_id, target.value)
        await self._audit.record(
            actor_uid=actor,
            action=f"content.{target.value}",
            entity_type="content",
            entity_id=content_id,
            before={"visibility": current},
            after={"visibility": target.value},
        )
        return {"id": content_id, "visibility": target.value}

    async def list_catalog(self, content_type: str | None = None) -> list[dict[str, Any]]:
        return await self._content.list_all(content_type=content_type)

    async def list_audit_logs(self, limit: int = 50) -> list[dict[str, Any]]:
        return await self._audit.list(limit=limit)

    # ---- seasons & episodes ----------------------------------------------
    async def _require_series(self, series_id: str) -> dict[str, Any]:
        series = await self._content.get_by_id(series_id)
        if not series:
            raise NotFoundError("Series not found")
        if series.get("type") != ContentType.SERIES.value:
            raise ValidationError("Target content is not a series")
        return series

    async def add_season(
        self, actor: str, series_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        await self._require_series(series_id)
        season_id = await self._content.add_season(series_id, payload)
        await self._audit.record(
            actor_uid=actor, action="season.create", entity_type="season", entity_id=season_id
        )
        return {"id": season_id, "seriesId": series_id, **payload}

    async def add_episode(
        self, actor: str, series_id: str, season_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        await self._require_series(series_id)
        episode_id = await self._content.add_episode(series_id, season_id, payload)
        await self._audit.record(
            actor_uid=actor, action="episode.create", entity_type="episode", entity_id=episode_id
        )
        return {"id": episode_id, "seasonId": season_id, **payload}

    # ---- media uploads ----------------------------------------------------
    async def request_upload_url(
        self, actor: str, kind: str, content_id: str, filename: str, content_type: str
    ) -> dict[str, Any]:
        allowed = _KIND_TYPES.get(kind)
        if allowed is None:
            raise ValidationError(f"Unsupported upload kind: {kind}")
        if content_type not in allowed:
            raise ValidationError(f"Content-type '{content_type}' not allowed for {kind}")

        safe_name = content_rules.slugify(filename.rsplit(".", 1)[0]) or "asset"
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
        path = f"public/{kind}/{content_id}/{safe_name}.{ext}"
        url = await self._storage.signed_upload_url(path, content_type)
        await self._audit.record(
            actor_uid=actor, action="media.upload_url", entity_type="media", entity_id=path
        )
        return {"uploadUrl": url, "path": path}
