#!/usr/bin/env python3
"""Reset LOCAL development data by clearing the Firestore + Auth emulators.

SAFETY: only ever talks to the emulator REST endpoints. Refuses to run if a real credential
is configured. Never touches production.

Usage:
    .venv/bin/python scripts/reset_dev_data.py     # emulators must be running
"""

from __future__ import annotations

import os
import sys
import urllib.request

if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
    print("[reset] Refusing: GOOGLE_APPLICATION_CREDENTIALS is set (looks like a real target).")
    sys.exit(1)

PROJECT_ID = os.environ.get("FIREBASE_PROJECT_ID", "movie-pedia-local")
FS_HOST = os.environ.get("FIRESTORE_EMULATOR_HOST", "localhost:8080")
AUTH_HOST = os.environ.get("FIREBASE_AUTH_EMULATOR_HOST", "localhost:9099")


def delete(url: str, label: str) -> None:
    req = urllib.request.Request(url, method="DELETE")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[reset] cleared {label}: HTTP {resp.status}")
    except Exception as exc:  # noqa: BLE001
        print(f"[reset] {label} not cleared ({exc}). Is the emulator running?")


delete(
    f"http://{FS_HOST}/emulator/v1/projects/{PROJECT_ID}/databases/(default)/documents",
    "firestore",
)
delete(f"http://{AUTH_HOST}/emulator/v1/projects/{PROJECT_ID}/accounts", "auth")
print("[reset] done. Run scripts/seed.py to repopulate.")
