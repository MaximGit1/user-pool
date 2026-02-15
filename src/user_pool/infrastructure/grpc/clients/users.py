from uuid_utils import UUID

import grpc.aio

from user_pool.application.common.data.dtos.auth import ClientCreateRequest, Client
from user_pool.application.common.exceptions.auth import ClientAlreadyExistsError, InvalidArgument, InternalError, \
    ClientNotFoundError
from user_pool.setup.config import AuthGRPCClientConfig
from user_pool.infrastructure.grpc.gen.auth import users_pb2_grpc, users_pb2 as msg


class UsersGRPCClient:
    def __init__(self, config: AuthGRPCClientConfig, channel: grpc.aio.Channel) -> None:
        self._client = users_pb2_grpc.UsersStub(channel)
        self._meta = [(config.secret_key, config.secret_key_value)]
        self._timeout = config.timeout

    async def create(self, request: ClientCreateRequest) -> None:
        req = msg.RegisterRequest(email=request.email, password=request.password)
        try:
            await self._client.Create(req, timeout=self._timeout, metadata=self._meta)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                err_msg = f"User {request.email} already exists"
                raise ClientAlreadyExistsError(err_msg)
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                err_msg = "Invalid input data"
                raise InvalidArgument(err_msg)
            else:
                err_msg = f"gRPC system error: {e.code()} - {e.details()}"
                raise InternalError(err_msg)


    async def get_user_by_id(self, user_id: UUID) -> Client:
        req = msg.UserByIDRequest(user_id=str(user_id))

        try:
            user: msg.User = await self._client.GetUserByID(req, timeout=self._timeout, metadata=self._meta)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                err_msg = f"User with ID {user_id} not found."
                raise ClientNotFoundError(err_msg)
            elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                err_msg = f"Incorrect ID format passed: {e.details()}"
                raise InvalidArgument(err_msg)
            else:
                err_msg = f"gRPC system error: {e.code()} - {e.details()}"
                raise InternalError(err_msg)

        return Client(id=UUID(user.id), email=user.email)