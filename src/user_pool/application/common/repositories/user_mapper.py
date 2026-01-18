from typing import Any, Protocol
from collections.abc import Sequence

from user_pool.domain.entities import User


class UserMapper(Protocol):
    def load_user(self, row: Sequence[Any]) -> User: ...

    def load_users(self, rows: Sequence[Any]) -> list[User]: ...

    def to_create_data(self, user: User) -> dict[str, Any]: ...
