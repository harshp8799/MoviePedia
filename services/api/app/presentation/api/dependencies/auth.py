"""Authentication & authorization dependencies. Deny-by-default (ADR-003).

- get_current_user: verifies the Bearer ID token and resolves the role from custom claims.
- require_role(*roles): guards a route; raises 403 unless the caller has one of the roles.

Role is read ONLY from the verified token's claims — never from the request body or headers.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.domain.repositories.ports import AuthPort
from app.infrastructure.firebase.auth_adapter import FirebaseAuthAdapter
from app.presentation.api.schemas.common import CurrentUser

# auto_error=False so we can return our own envelope instead of FastAPI's default 403.
_bearer = HTTPBearer(auto_error=False)


def get_auth_port() -> AuthPort:
    return FirebaseAuthAdapter()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
    auth_port: Annotated[AuthPort, Depends(get_auth_port)],
) -> CurrentUser:
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("Missing bearer token")

    decoded = await auth_port.verify_token(credentials.credentials)
    return CurrentUser(
        uid=decoded["uid"],
        email=decoded.get("email"),
        role=decoded.get("role", "user"),
    )


def require_role(*allowed_roles: str):
    """Return a dependency that allows only the given roles."""

    async def _guard(
        user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        if user.role not in allowed_roles:
            raise ForbiddenError(
                f"Requires one of roles: {', '.join(allowed_roles)}",
                details={"required": list(allowed_roles), "actual": user.role},
            )
        return user

    return _guard
