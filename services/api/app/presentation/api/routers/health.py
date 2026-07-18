"""Health & readiness endpoints. Liveness is dependency-free; readiness is expanded in Phase 4."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict:
    """Liveness — the process is up. No external dependencies checked."""
    settings = get_settings()
    return {"status": "ok", "env": settings.app_env, "service": "movie-pedia-api"}


@router.get("/ready")
async def ready() -> dict:
    """Readiness — placeholder. Phase 4 adds Firebase/Firestore connectivity checks."""
    return {"status": "ready", "checks": {"firebase": "not_wired_yet"}}
