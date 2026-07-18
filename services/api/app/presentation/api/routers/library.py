"""User-library routes (auth required). Everything is scoped to the caller's uid."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Path

from app.application.services.user_library_service import UserLibraryService
from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.dependencies.library import get_user_library_service
from app.presentation.api.schemas.common import CurrentUser
from app.presentation.api.schemas.library import ContentRef, ProgressUpdate

router = APIRouter(tags=["library"])

User = Annotated[CurrentUser, Depends(get_current_user)]
Svc = Annotated[UserLibraryService, Depends(get_user_library_service)]
ListPath = Annotated[str, Path(pattern="^(watchlist|favorites)$")]


# ---- watchlist / favorites ------------------------------------------------
@router.get("/library/{list_type}")
async def get_list(list_type: ListPath, user: User, svc: Svc) -> dict:
    return await svc.get_list(user.uid, list_type)


@router.post("/library/{list_type}", status_code=201)
async def add_item(list_type: ListPath, body: ContentRef, user: User, svc: Svc) -> dict:
    return await svc.add_to_list(user.uid, list_type, body.contentId)


@router.delete("/library/{list_type}/{content_id}")
async def remove_item(list_type: ListPath, content_id: str, user: User, svc: Svc) -> dict:
    await svc.remove_from_list(user.uid, list_type, content_id)
    return {"status": "removed", "contentId": content_id}


# ---- history --------------------------------------------------------------
@router.get("/history")
async def get_history(user: User, svc: Svc) -> dict:
    return await svc.get_history(user.uid)


@router.post("/history", status_code=201)
async def record_view(body: ContentRef, user: User, svc: Svc) -> dict:
    return await svc.record_view(user.uid, body.contentId)


# ---- progress / continue watching -----------------------------------------
@router.get("/progress")
async def continue_watching(user: User, svc: Svc) -> dict:
    return await svc.get_continue_watching(user.uid)


@router.put("/progress/{content_id}")
async def set_progress(content_id: str, body: ProgressUpdate, user: User, svc: Svc) -> dict:
    return await svc.set_progress(user.uid, content_id, body.positionSec, body.durationSec)
