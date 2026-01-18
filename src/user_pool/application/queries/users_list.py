from dataclasses import dataclass
from logging import getLogger

from bazario import Request
from bazario.asyncio import RequestHandler

from user_pool.application.common.data.dtos.users import UserShortDTO
from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination
from user_pool.application.common.repositories.assigned_user_read import (
    AssignedUserReadRepository,
)
from user_pool.application.common.repositories.user_read import (
    UserReadRepository,
)


log = getLogger(__name__)


@dataclass(frozen=True)
class RetrieveUsersListRequest(Request[list[UserShortDTO]]):
    pagination: Pagination
    filters: UserFilter


class RetrieveUserShortHandler(
    RequestHandler[RetrieveUsersListRequest, list[UserShortDTO]]
):
    def __init__(
        self,
        user_repo: UserReadRepository,
        assigned_user_repo: AssignedUserReadRepository,
    ) -> None:
        self._user_repo = user_repo
        self._assigned_user_repo = assigned_user_repo

    async def handle(
        self, request: RetrieveUsersListRequest
    ) -> list[UserShortDTO]:
        users = await self._user_repo.list(
            filters=request.filters, pagination=request.pagination
        )
        locked_ids = await self._assigned_user_repo.locked_user_ids(
            [user.id for user in users]
        )

        return [
            UserShortDTO(
                user_id=user.id.value,
                is_locked=user.id in locked_ids,
                created_at=user.created_at,
            )
            for user in users
        ]
