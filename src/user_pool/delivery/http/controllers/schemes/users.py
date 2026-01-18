from dataclasses import dataclass

from pydantic import BaseModel, Field

from user_pool.application.common.data.dtos.users import UserCreateDTO
from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination, SortOrder


class UserCreateScheme(BaseModel):
    """Input Scheme for creating a new user"""

    username: str = Field(
        ...,
        min_length=5,
        max_length=20,
        description=(
            "Username (5–20 chars).\n"
            "- must NOT start with a digit\n"
            "- allowed characters: letters, digits, '_'\n"
        ),
        examples=["_any_user12", "test_user1"],
    )

    email: str = Field(
        ...,
        description=(
            "Email address.\n"
            "Format: local-part + '@' + domain.\n"
            "Valid characters in local part: letters, digits, '._%'+-'\n"
            "End with TLD ≥ 2 letters."
        ),
        examples=["user@example.com"],
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=36,
        description=(
            "Raw password before hashing.\n"
            "- must NOT start with a digit\n"
            "- allowed characters: lowercase letters, digits, '_!$%'\n"
            f"- length: {8}–{36}"
        ),
        examples=["qwerty_123", "password!12"],
    )

    def to_dto(self) -> UserCreateDTO:
        return UserCreateDTO(
            username=self.username,
            email=self.email,
            password=self.password,
        )


@dataclass(frozen=True)
class UsersListScheme:
    offset: int | None = None
    limit: int | None = None
    order: SortOrder | None = None

    username: str | None = None
    email: str | None = None

    def to_dto(self) -> tuple[Pagination, UserFilter]:
        return (
            Pagination(offset=self.offset, limit=self.limit, order=self.order),
            UserFilter(username=self.username, email=self.email),
        )
