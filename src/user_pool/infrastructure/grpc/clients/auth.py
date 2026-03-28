import grpc.aio

from user_pool.application.common.data.dtos.auth import (
    AuthTokens,
    LoginRequest,
    RefreshToken,
)
from user_pool.application.common.exceptions.auth import (
    ClientNotFoundError,
    InternalError,
    InvalidArgument,
    UnauthenticatedError,
)
from user_pool.infrastructure.grpc.gen.auth import auth_pb2 as msg
from user_pool.infrastructure.grpc.gen.auth import auth_pb2_grpc
from user_pool.setup.config import AuthGRPCClientConfig


class AuthGRPCClient:
    def __init__(self, config: AuthGRPCClientConfig, channel: grpc.aio.Channel) -> None:
        self._client = auth_pb2_grpc.AuthStub(channel)
        self._meta = [(config.secret_key, config.secret_key_value)]
        self._timeout = config.timeout

    async def login(self, request: LoginRequest) -> AuthTokens:
        req = msg.LoginRequest(email=request.email, password=request.password)

        try:
            tokens: msg.AuthTokens = await self._client.Login(req, timeout=self._timeout, metadata=self._meta)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                err_msg = f"Unauthenticated: {e.details()}"
                raise UnauthenticatedError(err_msg)
            if e.code() == grpc.StatusCode.NOT_FOUND:
                raise ClientNotFoundError()
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                err_msg = "Invalid input data"
                raise InvalidArgument(err_msg)
            err_msg = f"gRPC system error: {e.code()} - {e.details()}"
            raise InternalError(err_msg)

        return AuthTokens(access=tokens.access_token, refresh=tokens.refresh_token)

    async def refresh(self, refresh: RefreshToken) -> AuthTokens:
        req = msg.RefreshRequest(refresh_token=refresh)

        try:
            tokens: msg.AuthTokens = await self._client.Refresh(req, timeout=self._timeout, metadata=self._meta)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                err_msg = f"Refresh error: Refresh token is invalid or expired. {e.details()}"
                raise UnauthenticatedError(err_msg)
            err_msg = f"gRPC system error: {e.code()} - {e.details()}"
            raise InternalError(err_msg)

        return AuthTokens(access=tokens.access_token, refresh=tokens.refresh_token)


    async def logout(self, refresh_token: str) -> None:
        req = msg.LogoutRequest(refresh_token=refresh_token)

        try:
            await self._client.Logout(req, timeout=self._timeout, metadata=self._meta)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                err_msg = f"The token is no longer valid. {e.details()}"
                raise UnauthenticatedError(err_msg)
            err_msg = f"gRPC system error: {e.code()} - {e.details()}"
            raise InternalError(err_msg)
