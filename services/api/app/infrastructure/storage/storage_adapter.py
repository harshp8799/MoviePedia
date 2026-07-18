"""Cloud Storage adapter for the StoragePort — mints signed upload/playback URLs (ADR-006).

Bytes never pass through the API. In production a v4 signed URL is generated (requires a service
account with a signing key). Against the emulator (no signing key) we return an emulator upload/
download URL so the local flow still works end-to-end.
"""

from __future__ import annotations

from datetime import timedelta

from firebase_admin import storage as fb_storage

from app.core.config import get_settings
from app.domain.repositories.ports import StoragePort


class FirebaseStorageAdapter(StoragePort):
    def __init__(self) -> None:
        settings = get_settings()
        self._settings = settings
        self._bucket_name = (
            settings.firebase_storage_bucket or f"{settings.firebase_admin_project_id}.appspot.com"
        )

    def _emulator_url(self, path: str) -> str:
        host = self._settings.firebase_storage_emulator_host
        from urllib.parse import quote

        return f"http://{host}/v0/b/{self._bucket_name}/o?name={quote(path, safe='')}"

    async def signed_upload_url(self, path: str, content_type: str) -> str:
        if self._settings.use_firebase_emulator:
            return self._emulator_url(path)
        blob = fb_storage.bucket(self._bucket_name).blob(path)
        return blob.generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=15),
            method="PUT",
            content_type=content_type,
        )

    async def signed_playback_url(self, path: str, ttl_seconds: int) -> str:
        if self._settings.use_firebase_emulator:
            return self._emulator_url(path)
        blob = fb_storage.bucket(self._bucket_name).blob(path)
        return blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=ttl_seconds),
            method="GET",
        )
