"""Request schemas for user-library operations."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ContentRef(BaseModel):
    contentId: str = Field(min_length=1)


class ProgressUpdate(BaseModel):
    positionSec: int = Field(ge=0)
    durationSec: int = Field(gt=0)
