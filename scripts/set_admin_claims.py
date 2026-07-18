#!/usr/bin/env python3
"""Grant a role (admin|editor|user) to a user via Firebase custom claims.

Roles are the authorization source of truth (ADR-003). Defaults to the emulator; to target a
real project set GOOGLE_APPLICATION_CREDENTIALS and FIREBASE_PROJECT_ID and unset the emulator host.

Usage:
    .venv/bin/python scripts/set_admin_claims.py <email-or-uid> <admin|editor|user>
"""

from __future__ import annotations

import os
import sys

ROLES = {"admin", "editor", "user"}

if len(sys.argv) != 3 or sys.argv[2] not in ROLES:
    print("Usage: set_admin_claims.py <email-or-uid> <admin|editor|user>")
    sys.exit(1)

target, role = sys.argv[1], sys.argv[2]

PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "movie-pedia-local")
if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ.setdefault("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")
    os.environ.setdefault("GCLOUD_PROJECT", PROJECT_ID)

import firebase_admin  # noqa: E402
from firebase_admin import auth, credentials  # noqa: E402

if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    firebase_admin.initialize_app(options={"projectId": PROJECT_ID})
else:
    import google.auth.credentials

    class _EmulatorCredentials(credentials.Base):
        def get_credential(self):
            return google.auth.credentials.AnonymousCredentials()

    firebase_admin.initialize_app(_EmulatorCredentials(), {"projectId": PROJECT_ID})

user = auth.get_user(target) if "@" not in target else auth.get_user_by_email(target)
auth.set_custom_user_claims(user.uid, {"role": role})
print(f"[claims] set role='{role}' on uid={user.uid} ({user.email}) project={PROJECT_ID}")
print("[claims] user must obtain a fresh ID token for the new claim to take effect.")
