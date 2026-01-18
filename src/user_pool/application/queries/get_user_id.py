from dataclasses import dataclass
from logging import getLogger
from uuid import UUID

from bazario import Request
from bazario.asyncio import Publisher, RequestHandler

from user_pool.application.commands.user_created import UserCreated
from user_pool.domain.services.user import UserService
from user_pool.application.common.data.dtos.users import UserCreateDTO



log = getLogger(__name__)


@dataclass(frozen=True)
class RetrieveNewUserIDRequest(Request[UUID]):
    dto: UserCreateDTO


class RetrieveNewUserIDHandler(RequestHandler[RetrieveNewUserIDRequest, UUID]):
    def __init__(self, service: UserService, publisher: Publisher) -> None:
        self._service = service
        self._publisher = publisher

    async def handle(self, request: RetrieveNewUserIDRequest) -> UUID:
        dto = request.dto

        user = self._service.create_user(
            username=dto.username,
            email=dto.email,
            raw_password=dto.password,
        )

        await self._publisher.publish(UserCreated(user))

        msg = "user was created (draft)"
        log.info(msg)

        return user.id.value
