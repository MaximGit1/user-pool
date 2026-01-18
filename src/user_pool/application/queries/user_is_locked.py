from dataclasses import dataclass
from logging import getLogger
from uuid import UUID

from bazario import Request
from bazario.asyncio import RequestHandler

from user_pool.domain.value_objects.user_id import UserID
from user_pool.application.common.repositories.assigned_user_read import (
    AssignedUserReadRepository,
)


log = getLogger(__name__)


@dataclass(frozen=True)
class RetrieveUserIsLockedRequest(Request[bool]):
    user_id: UUID


class RetrieveUserIsLockedRequestHandler(
    RequestHandler[RetrieveUserIsLockedRequest, bool]
):
    def __init__(
        self,
        assigned_user_repo: AssignedUserReadRepository,
    ) -> None:
        self._assigned_user_repo = assigned_user_repo

    async def handle(self, request: RetrieveUserIsLockedRequest) -> bool:
        user_id = request.user_id
        res = await self._assigned_user_repo.exists(UserID.unsafe(user_id))
        msg, ctx = "", {"user_id": user_id}
        log.info(msg, extra=ctx)

        return res
