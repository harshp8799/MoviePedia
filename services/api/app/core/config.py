"""Application configuration. Loaded from environment / .env (never hardcode secrets)."""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../../.env"),  # service-local first, then repo root
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Comma-separated list of allowed CORS origins.
    api_cors_origins: str = "http://localhost:3000,http://localhost:8081"

    # Firebase / emulator
    firebase_admin_project_id: str = "movie-pedia-local"
    google_application_credentials: str = ""
    use_firebase_emulator: bool = True
    firestore_emulator_host: str = "localhost:8080"
    firebase_auth_emulator_host: str = "localhost:9099"
    firebase_storage_emulator_host: str = "localhost:9199"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"  # json | console

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.api_cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor (import this, not the class, everywhere)."""
    return Settings()
