from typing import Protocol
from uuid import UUID

from user_pool.application.common.data.dtos.auth import (
    AuthTokens,
    Client,
    ClientCreateRequest,
    LoginRequest,
    RefreshToken,
)


class UserSSOClient(Protocol):
    async def create(self, request: ClientCreateRequest) -> None: ...

    async def get_user_by_id(self, user_id: UUID) -> Client: ...


class AuthSSOClient(Protocol):
    async def login(self, request: LoginRequest) -> AuthTokens: ...

    async def refresh(self, refresh: RefreshToken) -> AuthTokens: ...

    async def logout(self, refresh: RefreshToken) -> None: ...
