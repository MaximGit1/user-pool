from typing import Protocol

from user_pool.application.common.data.dtos.auth import (
    AccessPayload,
    AccessToken,
)


class TokenManager(Protocol):
    """
    Check the access token signature
    Check exp
    Decide whether to update
    """

    def parse_access(self, token: AccessToken) -> AccessPayload: ...

    def should_refresh(self, payload: AccessPayload) -> bool: ...
