from typing import Protocol

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID


class AssignedUserReadRepository(Protocol):
    async def locked_user_ids(self, user_ids: list[UserID]) -> set[UserID]: ...

    async def get_assignment(self, user_id: UserID) -> AssignedUser | None: ...

    async def exists(self, user_id: UserID) -> bool: ...
