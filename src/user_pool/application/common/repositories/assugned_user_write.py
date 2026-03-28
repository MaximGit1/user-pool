from typing import Protocol

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID


class AssignedUserWriteRepository(Protocol):
    async def assign(
        self, assigned_user: AssignedUser, assignment_ttl: int
    ) -> None: ...

    async def remove(self, user_id: UserID) -> None: ...

    async def remove_all(self) -> None: ...
