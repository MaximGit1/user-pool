from user_pool.application.common.data.dtos.auth import AuthContext
from user_pool.application.common.repositories.auth.identity_provider import (
    IdentityProvider,
)


class ProtectedManager:
    """Protects handlers from unauthorized users"""

    def __init__(self, identity: IdentityProvider) -> None:
        self._identity = identity

    async def __call__(self) -> AuthContext:
        return await self._identity.get_context()
