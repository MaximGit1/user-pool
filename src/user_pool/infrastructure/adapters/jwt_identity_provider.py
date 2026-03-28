from uuid import UUID

from user_pool.application.common.data.dtos.auth import AuthContext
from user_pool.application.common.exceptions.auth import UnauthenticatedError
from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
    UserSSOClient,
)
from user_pool.application.common.repositories.auth.tokenManager import (
    TokenManager,
)
from user_pool.application.common.repositories.auth.tokenTransportManager import (
    HttpTokenTransportManager,
)


class JWTIdentityProvider:
    def __init__(
        self,
        parser: TokenManager,
        transport: HttpTokenTransportManager,
        auth_client: AuthSSOClient,
        users_client: UserSSOClient,
    ) -> None:
        self._parser = parser
        self._transport = transport
        self._auth_client = auth_client
        self._users_client = users_client

    async def get_context(self) -> AuthContext:
        access = self._transport.get_access()
        if access is None:
            err_msg = "couldn't get an current access token"
            raise UnauthenticatedError(err_msg)

        access_payload = self._parser.parse_access(access)

        if self._parser.should_refresh(access_payload):
            refresh = self._transport.get_refresh()
            if refresh is None:
                err_msg = "couldn't get an current refresh token"
                raise UnauthenticatedError(err_msg)

            new_tokens = await self._auth_client.refresh(refresh)
            access_payload = self._parser.parse_access(new_tokens.access)
            user = await self._users_client.get_user_by_id(
                UUID(access_payload.user_id)
            )

            return AuthContext(
                user=user,
                new_access=new_tokens.access,
                new_refresh=new_tokens.refresh,
            )

        user = await self._users_client.get_user_by_id(
            UUID(access_payload.user_id)
        )

        return AuthContext(user=user)
