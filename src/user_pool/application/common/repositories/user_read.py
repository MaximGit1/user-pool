from typing import Protocol

from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination
from user_pool.domain.entities.user import User
from user_pool.domain.value_objects.user_id import UserID


class UserReadRepository(Protocol):
    async def get_by_id(self, user_id: UserID) -> User | None: ...

    async def list(
        self, filters: UserFilter, pagination: Pagination
    ) -> list[User]: ...
