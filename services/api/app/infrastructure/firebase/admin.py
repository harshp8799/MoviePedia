"""Firebase Admin SDK initialization (infrastructure layer only).

The rest of the app never imports firebase_admin directly — it depends on ports (ADR-002).
This module is the single place the concrete SDK is wired. When USE_FIREBASE_EMULATOR is on,
the Admin SDK targets the local emulators and needs no service-account credentials.
"""

from __future__ import annotations

import os
from functools import lru_cache

import firebase_admin
import google.auth.credentials
from firebase_admin import auth as fb_auth
from firebase_admin import credentials, firestore

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger("infra.firebase")


class _EmulatorCredentials(credentials.Base):
    """Anonymous credential so the Admin SDK never resolves ADC against the emulator."""

    def get_credential(self):
        return google.auth.credentials.AnonymousCredentials()


@lru_cache
def get_app() -> firebase_admin.App:
    """Initialize (once) and return the Firebase Admin app."""
    settings = get_settings()

    if settings.use_firebase_emulator:
        # Point the Admin SDK at the emulators; no real credentials required.
        os.environ.setdefault("FIRESTORE_EMULATOR_HOST", settings.firestore_emulator_host)
        os.environ.setdefault("FIREBASE_AUTH_EMULATOR_HOST", settings.firebase_auth_emulator_host)
        os.environ.setdefault("GCLOUD_PROJECT", settings.firebase_admin_project_id)
        cred = _EmulatorCredentials()
    elif settings.google_application_credentials:
        cred = credentials.Certificate(settings.google_application_credentials)
    else:
        cred = None  # falls back to Application Default Credentials in real environments

    try:
        return firebase_admin.get_app()
    except ValueError:
        options = {"projectId": settings.firebase_admin_project_id}
        app = firebase_admin.initialize_app(cred, options)
        logger.info(
            "firebase_admin_initialized",
            extra={
                "emulator": settings.use_firebase_emulator,
                "project": settings.firebase_admin_project_id,
            },
        )
        return app


def get_firestore():
    """Firestore client bound to the initialized Admin app."""
    return firestore.client(get_app())


def get_auth():
    """Firebase Auth admin module (token verification, custom claims)."""
    get_app()
    return fb_auth
