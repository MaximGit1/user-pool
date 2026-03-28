from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from user_pool.application.common.data.dtos.assigned_user import (
    UserLockDTO,
)
from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination


@dataclass(frozen=True, slots=True)
class UserShortDTO:
    user_id: UUID
    is_locked: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class UserFullDTO:
    user_id: UUID
    username: str
    email: str
    hashed_password: bytes
    created_at: datetime

    lock: UserLockDTO | None


@dataclass(frozen=True, slots=True)
class UserCreateDTO:
    username: str
    email: str
    password: str

@dataclass(frozen=True, slots=True)
class RetrieveUsersListRequest:
    pagination: Pagination
    filters: UserFilter
