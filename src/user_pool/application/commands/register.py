from logging import getLogger

from user_pool.application.common.data.dtos.auth import ClientCreateRequest
from user_pool.application.common.repositories.auth.sso_clients import (
    UserSSOClient,
)

log = getLogger(__name__)

class RegisterHandler:
    def __init__(
        self,
        client: UserSSOClient,
    ) -> None:
        self._client = client

    async def handle(self, request: ClientCreateRequest) -> None:
        await self._client.create(request)

        msg, ctx = "the user has been login", {"email": request.email}
        log.info(msg, extra=ctx)
