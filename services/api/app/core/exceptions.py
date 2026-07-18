"""Domain-agnostic application exceptions. Mapped to HTTP responses in the presentation layer."""

from __future__ import annotations


class AppError(Exception):
    """Base application error with a stable machine code and HTTP status hint."""

    code = "app_error"
    status = 500

    def __init__(self, message: str, *, details: object | None = None):
        super().__init__(message)
        self.message = message
        self.details = details


class NotFoundError(AppError):
    code = "not_found"
    status = 404


class ValidationError(AppError):
    code = "validation_error"
    status = 422


class UnauthorizedError(AppError):
    code = "unauthorized"
    status = 401


class ForbiddenError(AppError):
    code = "forbidden"
    status = 403


class ConflictError(AppError):
    code = "conflict"
    status = 409
