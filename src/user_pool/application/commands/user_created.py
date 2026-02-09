from logging import getLogger
from uuid import UUID

from user_pool.application.common.data.dtos.users import UserCreateDTO
from user_pool.application.common.repositories.transaction_manager import (
    TransactionManager,
)
from user_pool.application.common.repositories.user_write import (
    UserWriteRepository,
)
from user_pool.domain.entities.user import User
from user_pool.domain.services import UserService

log = getLogger(__name__)


class UserCreatedHandler:
    def __init__(
        self,
        repo: UserWriteRepository,
        transaction_manager: TransactionManager,
        service: UserService,
    ) -> None:
        self._repo = repo
        self._transaction = transaction_manager
        self._service = service

    async def handle(self, request: UserCreateDTO) -> UUID:
        user = self._create_user(request)

        await self._repo.add(user=user)
        await self._transaction.commit()

        msg, ctx = "user was saved", {"user_id": user.id.value}
        log.info(msg, extra=ctx)

        return user.id.value

    def _create_user(self, request: UserCreateDTO) -> User:
        user = self._service.create_user(
            username=request.username,
            email=request.email,
            raw_password=request.password,
        )

        msg = "user was created (draft)"
        log.info(msg)

        return user