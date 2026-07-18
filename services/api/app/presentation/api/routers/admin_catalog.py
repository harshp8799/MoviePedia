"""Admin catalog management routes. Every mutation is authorized here (ADR-003) and audited.

Roles: editors and admins manage the catalog; destructive genre deletion is admin-only.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.services.catalog_service import CatalogService
from app.domain.value_objects.enums import ContentType, Visibility
from app.presentation.api.dependencies.auth import require_role
from app.presentation.api.dependencies.catalog import get_catalog_service
from app.presentation.api.schemas.catalog import (
    ContentCreate,
    ContentUpdate,
    EpisodeCreate,
    GenreCreate,
    SeasonCreate,
    UploadUrlRequest,
)
from app.presentation.api.schemas.common import CurrentUser

router = APIRouter(prefix="/admin", tags=["admin-catalog"])

Editor = Annotated[CurrentUser, Depends(require_role("admin", "editor"))]
Admin = Annotated[CurrentUser, Depends(require_role("admin"))]
Service = Annotated[CatalogService, Depends(get_catalog_service)]


# ---- genres ---------------------------------------------------------------
@router.post("/genres", status_code=201)
async def create_genre(body: GenreCreate, user: Editor, svc: Service) -> dict:
    return await svc.create_genre(user.uid, body.name)


@router.get("/genres")
async def list_genres(user: Editor, svc: Service) -> dict:
    return {"items": await svc.list_genres()}


@router.delete("/genres/{genre_id}")
async def delete_genre(genre_id: str, user: Admin, svc: Service) -> dict:
    await svc.delete_genre(user.uid, genre_id)
    return {"status": "deleted", "id": genre_id}


# ---- movies & series ------------------------------------------------------
@router.post("/movies", status_code=201)
async def create_movie(body: ContentCreate, user: Editor, svc: Service) -> dict:
    return await svc.create_content(user.uid, ContentType.MOVIE, body.model_dump())


@router.post("/series", status_code=201)
async def create_series(body: ContentCreate, user: Editor, svc: Service) -> dict:
    return await svc.create_content(user.uid, ContentType.SERIES, body.model_dump())


@router.patch("/content/{content_id}")
async def update_content(content_id: str, body: ContentUpdate, user: Editor, svc: Service) -> dict:
    return await svc.update_content(user.uid, content_id, body.model_dump(exclude_unset=True))


@router.post("/content/{content_id}/publish")
async def publish_content(content_id: str, user: Editor, svc: Service) -> dict:
    return await svc.change_visibility(user.uid, content_id, Visibility.PUBLISHED)


@router.post("/content/{content_id}/archive")
async def archive_content(content_id: str, user: Editor, svc: Service) -> dict:
    return await svc.change_visibility(user.uid, content_id, Visibility.ARCHIVED)


@router.post("/content/{content_id}/unpublish")
async def unpublish_content(content_id: str, user: Editor, svc: Service) -> dict:
    return await svc.change_visibility(user.uid, content_id, Visibility.DRAFT)


@router.get("/catalog")
async def list_catalog(
    user: Editor,
    svc: Service,
    type: Annotated[str | None, Query()] = None,
) -> dict:
    return {"items": await svc.list_catalog(content_type=type)}


@router.get("/audit-logs")
async def list_audit_logs(
    user: Admin,
    svc: Service,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
) -> dict:
    return {"items": await svc.list_audit_logs(limit)}


# ---- seasons & episodes ---------------------------------------------------
@router.post("/series/{series_id}/seasons", status_code=201)
async def add_season(series_id: str, body: SeasonCreate, user: Editor, svc: Service) -> dict:
    return await svc.add_season(user.uid, series_id, body.model_dump())


@router.post("/series/{series_id}/seasons/{season_id}/episodes", status_code=201)
async def add_episode(
    series_id: str, season_id: str, body: EpisodeCreate, user: Editor, svc: Service
) -> dict:
    return await svc.add_episode(user.uid, series_id, season_id, body.model_dump())


# ---- media uploads --------------------------------------------------------
@router.post("/media/upload-url")
async def request_upload_url(body: UploadUrlRequest, user: Editor, svc: Service) -> dict:
    return await svc.request_upload_url(
        user.uid, body.kind, body.contentId, body.filename, body.contentType
    )
