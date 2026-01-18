from dataclasses import dataclass
from logging import getLogger

from bazario import Notification
from bazario.asyncio import NotificationHandler

from user_pool.application.common.repositories.transaction_manager import (
    TransactionManager,
)
from user_pool.application.common.repositories.user_write import (
    UserWriteRepository,
)
from user_pool.domain.entities.user import User



log = getLogger(__name__)


@dataclass(frozen=True)
class UserCreated(Notification):
    user: User


class UserCreatedHandler(NotificationHandler[UserCreated]):
    def __init__(
        self,
        repo: UserWriteRepository,
        transaction_manager: TransactionManager,
    ) -> None:
        self._repo = repo
        self._transaction = transaction_manager

    async def handle(self, notification: UserCreated) -> None:
        user = notification.user

        await self._repo.add(user=user)
        await self._transaction.commit()

        msg, ctx = "user was saved", {"user_id": user.id.value}
        log.info(msg, extra=ctx)
