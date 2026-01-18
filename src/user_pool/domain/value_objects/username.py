from dataclasses import dataclass
from string import ascii_lowercase, digits
from typing import ClassVar, Final

from user_pool.domain.exceptions.user import (
    UsernameRangeError,
    UsernameValueError,
)
from user_pool.domain.value_objects.base import ValueObject


@dataclass(slots=True, frozen=True)
class Username(ValueObject[str]):
    """Represents a username chosen by the user.

    Domain validation rules:
    - must be between USERNAME_MIN_LEN and USERNAME_MAX_LEN characters
    - first character cannot be a digit
    - allowed characters: ASCII letters, digits, '_'
    - validation is case-insensitive (username is normalized to lowercase)
    """

    __USERNAME_MIN_LEN: ClassVar[Final[int]] = 5
    __USERNAME_MAX_LEN: ClassVar[Final[int]] = 20
    __USERNAME_ALLOWED_CHARS: ClassVar[Final[set[str]]] = set(
        ascii_lowercase + digits + "_"
    )

    @classmethod
    def _validate(cls, value: str) -> None:
        name_len = len(value)
        if not (cls.__USERNAME_MIN_LEN <= name_len <= cls.__USERNAME_MAX_LEN):
            raise UsernameRangeError

        if value[0] in digits:
            raise UsernameValueError

        for char in value.lower():
            if char not in cls.__USERNAME_ALLOWED_CHARS:
                raise UsernameValueError
