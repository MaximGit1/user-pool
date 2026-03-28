from logging import getLogger
from uuid import UUID

from user_pool.application.common.repositories.assugned_user_write import (
    AssignedUserWriteRepository,
)
from user_pool.domain.value_objects.user_id import UserID

log = getLogger(__name__)


class UserUnlockedHandler:
    def __init__(
        self,
        assigned_user_repo: AssignedUserWriteRepository,
    ) -> None:
        self._repo = assigned_user_repo

    async def handle(self, user_id: UUID) -> None:
        await self._repo.remove(UserID.unsafe(user_id))

        msg, ctx = (
            "assigned data was removed before the expiration of the term",
            {"user_id": user_id},
        )
        log.info(msg, extra=ctx)
