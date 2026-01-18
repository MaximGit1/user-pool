from typing import Protocol

from user_pool.domain.entities.user import User


class UserWriteRepository(Protocol):
    async def add(self, user: User) -> None: ...
