from uuid import UUID
from logging import getLogger

from user_pool.application.common.data.dtos.assigned_user import UserLockDTO
from user_pool.application.common.data.dtos.users import UserFullDTO
from user_pool.application.common.exceptions.users import UserNotFoundError
from user_pool.domain.value_objects.user_id import UserID
from user_pool.application.common.repositories.assigned_user_read import (
    AssignedUserReadRepository,
)
from user_pool.application.common.repositories.user_read import (
    UserReadRepository,
)



log = getLogger(__name__)


class RetrieveUserRequestHandler:
    def __init__(
        self,
        user_repo: UserReadRepository,
        assigned_user_repo: AssignedUserReadRepository,
    ) -> None:
        self._user_repo = user_repo
        self._assigned_user_repo = assigned_user_repo

    async def handle(self, user_id: UUID) -> UserFullDTO:
        user_id_vo = UserID.unsafe(user_id)

        user = await self._user_repo.get_by_id(user_id_vo)
        if user is None:
            err_msg, ctx = "User not found", {"user_id": user_id}

            log.error(err_msg, extra=ctx)
            raise UserNotFoundError(err_msg)

        assigned_user = await self._assigned_user_repo.get_assignment(
            user_id_vo
        )

        lock_data = (
            None
            if assigned_user is None
            else UserLockDTO(
                locked_time=assigned_user.locked_time,
                locked_by=assigned_user.project,
            )
        )

        return UserFullDTO(
            user_id=user_id,
            username=user.username.value,
            email=user.email.value,
            hashed_password=user.hashed_password,
            created_at=user.created_at,
            lock=lock_data,
        )
