"""User routes. Phase 4: identity echo. Profile/library features land in later phases."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.presentation.api.dependencies.auth import get_current_user
from app.presentation.api.schemas.common import CurrentUser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=CurrentUser)
async def me(user: Annotated[CurrentUser, Depends(get_current_user)]) -> CurrentUser:
    """Return the authenticated caller resolved from their verified token."""
    return user
