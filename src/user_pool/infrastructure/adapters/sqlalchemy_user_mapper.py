from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row

from user_pool.domain.entities import User
from user_pool.domain.value_objects import Email, UserID, Username


class SqlalchemyUserMapper:
    def load_user(self, row: Row[Any]) -> User:
        return User(
            _id=UserID.unsafe(row.id),
            _username=Username.unsafe(row.username),
            _hashed_password=row.password,
            _email=Email.unsafe(row.email),
            _created_at=row.created_at,
        )

    def load_users(self, rows: Sequence[Row[Any]]) -> list[User]:
        return [self.load_user(row) for row in rows]

    def to_create_data(self, user: User) -> dict[str, Any]:
        return {
            "id": user.id.value,
            "username": user.username.value,
            "email": user.email.value,
            "password": user.hashed_password,
            "created_at": user.created_at,
        }
