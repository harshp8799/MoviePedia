"""Request schemas for admin catalog management. Pydantic enforces validation at the edge."""

from __future__ import annotations

from pydantic import BaseModel, Field


class GenreCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)


class ContentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    originalTitle: str | None = None
    shortDescription: str | None = Field(default=None, max_length=500)
    fullDescription: str | None = None
    releaseDate: str | None = None
    releaseYear: int | None = Field(default=None, ge=1888, le=2100)
    durationMinutes: int | None = Field(default=None, ge=0, le=1000)
    ageRating: str | None = None
    genres: list[str] = Field(default_factory=list, max_length=10)
    languages: list[str] = Field(default_factory=list, max_length=20)
    countries: list[str] = Field(default_factory=list, max_length=20)


class ContentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    shortDescription: str | None = Field(default=None, max_length=500)
    fullDescription: str | None = None
    releaseDate: str | None = None
    releaseYear: int | None = Field(default=None, ge=1888, le=2100)
    durationMinutes: int | None = Field(default=None, ge=0, le=1000)
    ageRating: str | None = None
    genres: list[str] | None = Field(default=None, max_length=10)
    featured: bool | None = None


class SeasonCreate(BaseModel):
    seasonNumber: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=120)
    episodeCount: int | None = Field(default=None, ge=0)


class EpisodeCreate(BaseModel):
    episodeNumber: int = Field(ge=0)
    title: str = Field(min_length=1, max_length=200)
    durationMinutes: int | None = Field(default=None, ge=0, le=600)
    mediaAssetId: str | None = None
    visibility: str = "draft"


class UploadUrlRequest(BaseModel):
    kind: str = Field(pattern="^(poster|backdrop|trailer|video)$")
    contentId: str = Field(min_length=1)
    filename: str = Field(min_length=1, max_length=200)
    contentType: str = Field(min_length=1)
