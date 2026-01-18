from dataclasses import dataclass
from logging import getLogger
from uuid import UUID

from bazario import Notification
from bazario.asyncio import NotificationHandler

from user_pool.domain.value_objects.user_id import UserID
from user_pool.application.common.repositories.assugned_user_write import (
    AssignedUserWriteRepository,
)


log = getLogger(__name__)


@dataclass(frozen=True)
class UserUnlocked(Notification):
    user_id: UUID


class UserUnlockedHandler(NotificationHandler[UserUnlocked]):
    def __init__(
        self,
        assigned_user_repo: AssignedUserWriteRepository,
    ) -> None:
        self._repo = assigned_user_repo

    async def handle(self, notification: UserUnlocked) -> None:
        user_id = notification.user_id

        await self._repo.remove(UserID.unsafe(user_id))

        msg, ctx = (
            "assigned data was removed before the expiration of the term",
            {"user_id": user_id},
        )
        log.info(msg, extra=ctx)
