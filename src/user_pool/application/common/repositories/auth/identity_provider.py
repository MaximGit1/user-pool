from typing import Protocol

from user_pool.application.common.data.dtos.auth import AuthContext


class IdentityProvider(Protocol):
    """
    Gets the client from the current context
    """

    async def get_context(self) -> AuthContext: ...

