from starlette.requests import Request

from user_pool.application.common.data.dtos.auth import (
    AccessToken,
    RefreshToken,
)
from user_pool.setup.config import TokenConfig


class HttpCookieHeaderTokenTransportManager:
    def __init__(self, config: TokenConfig, request: Request) -> None:
        self._request = request

        self._refresh_cookie_key = config.refresh_cookie_key
        self._access_header_key = config.access_header_key

    def get_access(self) -> AccessToken | None:
        auth_header = self._request.headers.get("Authorization")
        if not auth_header:
            return None

        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            return token if token else None

        return None

    def get_refresh(self) -> RefreshToken | None:
        token = self._request.cookies.get(self._refresh_cookie_key)
        return token
