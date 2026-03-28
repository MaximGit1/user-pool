from datetime import UTC, datetime

import jwt

from user_pool.application.common.data.dtos.auth import (
    AccessPayload,
    AccessToken,
)
from user_pool.application.common.exceptions.auth import InvalidTokenError
from user_pool.setup.config import TokenConfig


class JWTTokenManager:
    def __init__(self, config: TokenConfig) -> None:
        self._issuer = config.issuer
        self._audience = config.audience
        self._key = config.public_key

    def parse_access(self, token: AccessToken) -> AccessPayload:
        """Check signature, expiration, and return payload"""

        try:
            payload = jwt.decode(
                token,
                self._key,
                algorithms=["RS256"],
                issuer=self._issuer,
                audience=self._audience,
            )
        except jwt.ExpiredSignatureError as exc:
            err_msg = "Access token expired"
            raise InvalidTokenError(err_msg) from exc
        except jwt.InvalidTokenError as exc:
            err_msg = "Invalid access token"
            raise InvalidTokenError(err_msg) from exc

        return AccessPayload(
            user_id=payload["sub"],
            issued_at=datetime.fromtimestamp(payload["iat"], tz=UTC),
            expires_at=datetime.fromtimestamp(payload["exp"], tz=UTC),
        )

    def should_refresh(self, payload: AccessPayload) -> bool:
        """Returns True if the token has expired or is 80% of its lifespan"""

        now = datetime.now(UTC)
        if now >= payload.expires_at:
            return True

        lifetime = payload.expires_at - payload.issued_at
        elapsed = now - payload.issued_at

        if elapsed / lifetime >= 0.8:
            return True

        return False
