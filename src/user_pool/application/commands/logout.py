from logging import getLogger

from user_pool.application.common.data.dtos.net import CookieKey
from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
)
from user_pool.application.common.repositories.auth.tokenTransportManager import (
    HttpTokenTransportManager,
)
from user_pool.setup.config import TokenConfig

log = getLogger(__name__)


class LogoutHandler:
    def __init__(
        self,
        client: AuthSSOClient,
        token_transport: HttpTokenTransportManager,
        token_config: TokenConfig,
    ) -> None:
        self._client = client
        self._token_transport = token_transport
        self._cookie_refresh_name = token_config.refresh_cookie_key

    async def handle(self) -> CookieKey:
        refresh = self._token_transport.get_refresh()
        await self._client.logout(refresh)

        msg = "the user has been logout"
        log.info(msg)

        return self._cookie_refresh_name
