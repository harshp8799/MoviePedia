"""Firebase implementation of the AuthPort (token verification + role claims).

The only place firebase auth token logic lives. Application/domain code depends on AuthPort,
never on firebase_admin (ADR-002).
"""

from __future__ import annotations

from typing import Any

from app.core.exceptions import UnauthorizedError
from app.domain.repositories.ports import AuthPort
from app.infrastructure.firebase.admin import get_auth


class FirebaseAuthAdapter(AuthPort):
    async def verify_token(self, id_token: str) -> dict[str, Any]:
        auth = get_auth()
        try:
            # check_revoked rejects tokens for disabled/revoked sessions.
            return auth.verify_id_token(id_token, check_revoked=True)
        except auth.ExpiredIdTokenError as exc:
            raise UnauthorizedError("Token has expired") from exc
        except auth.RevokedIdTokenError as exc:
            raise UnauthorizedError("Token has been revoked") from exc
        except Exception as exc:  # invalid signature, malformed, wrong audience, etc.
            raise UnauthorizedError("Invalid authentication token") from exc

    async def set_role(self, uid: str, role: str) -> None:
        auth = get_auth()
        auth.set_custom_user_claims(uid, {"role": role})
