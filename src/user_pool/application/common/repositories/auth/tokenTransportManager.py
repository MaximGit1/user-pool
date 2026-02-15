from typing import Protocol

from user_pool.application.common.data.dtos.auth import AccessToken, RefreshToken


class HttpTokenTransportManager(Protocol):
    def get_access(self) -> AccessToken | None: ...
    def get_refresh(self) -> RefreshToken | None: ...
