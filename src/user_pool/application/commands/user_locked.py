from dataclasses import dataclass
from datetime import UTC, datetime
from logging import getLogger
from uuid import UUID

from bazario import Notification
from bazario.asyncio import NotificationHandler

from user_pool.application.common.exceptions.users import (
    UserAlreadyLockedError,
)
from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID
from user_pool.application.common.repositories.assugned_user_write import (
    AssignedUserWriteRepository,
)
from user_pool.domain.value_objects.project import Project
from user_pool.setup.config import CacheConfig


log = getLogger(__name__)


@dataclass(frozen=True)
class UserLocked(Notification):
    dto: Project
    user_id: UUID
    user_is_locked: bool


class UserLockedHandler(NotificationHandler[UserLocked]):
    def __init__(
        self,
        config: CacheConfig,
        assigned_user_repo: AssignedUserWriteRepository,
    ) -> None:
        self._repo = assigned_user_repo
        self._ttl = config.assignment_ttl

    async def handle(self, notification: UserLocked) -> None:
        if notification.user_is_locked:
            err_msg, ctx = (
                "user already locked",
                {"user_id": notification.user_id},
            )

            log.error(err_msg, extra=ctx)
            raise UserAlreadyLockedError(err_msg)

        dto = notification.dto

        tll = self._ttl
        await self._repo.assign(
            assigned_user=AssignedUser(
                _id=UserID.unsafe(notification.user_id),
                _project=dto,
                _locked_time=datetime.now(UTC),
            ),
            assignment_ttl=tll,
        )
        msg, ctx = (
            "assigned data was saved",
            {"user_id": notification.user_id, "tll": tll},
        )
        log.info(msg, extra=ctx)
