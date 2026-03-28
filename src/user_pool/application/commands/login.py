from logging import getLogger

from user_pool.application.common.data.dtos.auth import (
    AccessToken,
    LoginRequest,
)
from user_pool.application.common.data.dtos.net import CookieData
from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
)
from user_pool.setup.config import TokenConfig

log = getLogger(__name__)


class LoginHandler:
    def __init__(
        self, client: AuthSSOClient, token_config: TokenConfig
    ) -> None:
        self._client = client
        self._refresh_cookie_key = token_config.refresh_cookie_key
        self._refresh_max_age = token_config.refresh_max_age

    async def handle(
        self, request: LoginRequest
    ) -> tuple[AccessToken, CookieData]:
        tokens = await self._client.login(request)

        msg, ctx = "the user has been login", {"email": request.email}
        log.info(msg, extra=ctx)

        return tokens.access, CookieData(
            key=self._refresh_cookie_key,
            value=tokens.refresh,
            max_age=self._refresh_max_age,
        )
