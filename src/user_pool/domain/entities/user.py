from dataclasses import dataclass
from datetime import datetime

from user_pool.domain.entities.base import BaseEntity
from user_pool.domain.value_objects.email import Email
from user_pool.domain.value_objects.user_id import UserID
from user_pool.domain.value_objects.username import Username


@dataclass(slots=True, kw_only=True)
class User(BaseEntity[UserID]):
    _username: Username
    _email: Email
    _hashed_password: bytes
    _created_at: datetime

    @property
    def username(self) -> Username:
        return self._username

    @property
    def email(self) -> Email:
        return self._email

    @property
    def hashed_password(self) -> bytes:
        return self._hashed_password

    @property
    def created_at(self) -> datetime:
        return self._created_at
