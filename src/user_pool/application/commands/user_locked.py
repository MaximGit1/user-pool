from datetime import UTC, datetime
from logging import getLogger
from uuid import UUID

from user_pool.application.common.data.dtos.assigned_user import UserLocked
from user_pool.application.common.exceptions.users import (
    UserAlreadyLockedError,
)
from user_pool.application.common.repositories import (
    AssignedUserReadRepository,
)
from user_pool.application.common.repositories.assugned_user_write import (
    AssignedUserWriteRepository,
)
from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID
from user_pool.setup.config import CacheConfig

log = getLogger(__name__)


class UserLockedHandler:
    def __init__(
        self,
        config: CacheConfig,
        assigned_user_repo_write: AssignedUserWriteRepository,
        assigned_user_repo_read: AssignedUserReadRepository,
    ) -> None:
        self._repo_write = assigned_user_repo_write
        self._repo_read = assigned_user_repo_read
        self._ttl = config.assignment_ttl

    async def handle(self, notification: UserLocked) -> None:
        if await self._is_locked(notification.user_id):
            err_msg, ctx = (
                "user already locked",
                {"user_id": notification.user_id},
            )

            log.error(err_msg, extra=ctx)
            raise UserAlreadyLockedError(err_msg)

        dto = notification.dto

        tll = self._ttl
        await self._repo_write.assign(
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

    async def _is_locked(self, user_id: UUID) -> bool:
        res = await self._repo_read.exists(UserID.unsafe(user_id))
        msg, ctx = "", {"user_id": user_id}
        log.info(msg, extra=ctx)

        return res
