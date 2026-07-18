"""Public catalog routes — no auth. Serves only published content (visibility enforced in the
repository/service). Cursor pagination for lists."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.application.services.public_catalog_service import PublicCatalogService
from app.domain.value_objects.enums import ContentType
from app.presentation.api.dependencies.public_catalog import get_public_catalog_service

router = APIRouter(tags=["catalog"])

Svc = Annotated[PublicCatalogService, Depends(get_public_catalog_service)]
Sort = Annotated[str, Query(pattern="^(popularity|recent|trending|release)$")]
Limit = Annotated[int, Query(ge=1, le=50)]


@router.get("/home")
async def home(svc: Svc) -> dict:
    return await svc.home()


@router.get("/genres")
async def genres(svc: Svc) -> dict:
    return await svc.list_genres()


@router.get("/movies")
async def list_movies(
    svc: Svc,
    genre: str | None = None,
    sort: Sort = "popularity",
    cursor: str | None = None,
    limit: Limit = 24,
) -> dict:
    return await svc.list_content(
        ContentType.MOVIE, genre=genre, sort=sort, cursor=cursor, limit=limit
    )


@router.get("/series")
async def list_series(
    svc: Svc,
    genre: str | None = None,
    sort: Sort = "popularity",
    cursor: str | None = None,
    limit: Limit = 24,
) -> dict:
    return await svc.list_content(
        ContentType.SERIES, genre=genre, sort=sort, cursor=cursor, limit=limit
    )


@router.get("/search")
async def search(
    svc: Svc,
    q: Annotated[str, Query(min_length=1, max_length=100)],
    type: Annotated[str | None, Query(pattern="^(movie|series)$")] = None,
) -> dict:
    return await svc.search(q, content_type=type)


@router.get("/movies/{slug}")
async def movie_detail(slug: str, svc: Svc) -> dict:
    return await svc.get_detail(slug)


@router.get("/series/{slug}")
async def series_detail(slug: str, svc: Svc) -> dict:
    return await svc.get_detail(slug)
