"""Admin routes. Phase 4: RBAC probe proving deny-by-default authorization.

Real admin catalog mutations land in Phase 5 — every one will independently authorize here,
never relying on frontend route guards (ADR-003).
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.presentation.api.dependencies.auth import require_role
from app.presentation.api.schemas.common import CurrentUser

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/ping")
async def admin_ping(
    user: Annotated[CurrentUser, Depends(require_role("admin"))],
) -> dict:
    """Admin-only health probe. 403 for non-admins, 401 for unauthenticated."""
    return {"status": "ok", "role": user.role, "uid": user.uid}


@router.get("/editorial")
async def editorial_ping(
    user: Annotated[CurrentUser, Depends(require_role("admin", "editor"))],
) -> dict:
    """Accessible to editors and admins — demonstrates multi-role authorization."""
    return {"status": "ok", "role": user.role}
