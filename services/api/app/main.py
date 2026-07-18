"""FastAPI application factory. Wires config, logging, CORS, routers, error handling.

Modular monolith entrypoint. Feature routers are mounted under /api/v1 as modules land
(Phase 4+). For Phase 2 this boots with health/readiness only.
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger
from app.presentation.api.errors import register_exception_handlers
from app.presentation.api.middleware.request_context import RequestContextMiddleware
from app.presentation.api.routers import admin, health, users

API_V1_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(level=settings.log_level, fmt=settings.log_format)
    logger = get_logger("app.startup")

    app = FastAPI(
        title="Movie Pedia API",
        version="0.1.0",
        description="Movie Pedia backend — modular monolith, Clean Architecture.",
    )

    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)

    app.include_router(health.router, prefix=API_V1_PREFIX)
    app.include_router(users.router, prefix=API_V1_PREFIX)
    app.include_router(admin.router, prefix=API_V1_PREFIX)

    logger.info("app_started", extra={"env": settings.app_env, "prefix": API_V1_PREFIX})
    return app


app = create_app()
