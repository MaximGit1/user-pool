from logging import getLogger

from user_pool.application.common.repositories.assugned_user_write import (
    AssignedUserWriteRepository,
)

log = getLogger(__name__)


class AllUsersUnlockedHandler:
    def __init__(
        self,
        assigned_user_repo: AssignedUserWriteRepository,
    ) -> None:
        self._repo = assigned_user_repo

    async def handle(self) -> None:
        await self._repo.remove_all()

        msg = "All assigned data was deleted before the expiration of the agreement"
        log.info(msg)
