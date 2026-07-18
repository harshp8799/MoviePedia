"""Health & readiness endpoints. Liveness is dependency-free; readiness checks Firestore."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.logging import get_logger

router = APIRouter(tags=["health"])
logger = get_logger("api.health")


@router.get("/health")
async def health() -> dict:
    """Liveness — the process is up. No external dependencies checked."""
    settings = get_settings()
    return {"status": "ok", "env": settings.app_env, "service": "movie-pedia-api"}


@router.get("/ready")
async def ready() -> dict:
    """Readiness — verifies Firestore connectivity via the Admin SDK."""
    firebase_ok = False
    detail = "ok"
    try:
        from app.infrastructure.firebase.admin import get_firestore

        # A lightweight round-trip: list up to 1 collection reference (no full read).
        client = get_firestore()
        next(iter(client.collections()), None)
        firebase_ok = True
    except Exception as exc:  # noqa: BLE001 — readiness must never raise
        detail = f"unavailable: {type(exc).__name__}"
        logger.warning("readiness_firebase_unavailable", extra={"error": str(exc)})

    status = "ready" if firebase_ok else "degraded"
    return {"status": status, "checks": {"firebase": detail}}
