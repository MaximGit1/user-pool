from dataclasses import dataclass
from string import ascii_lowercase, digits
from typing import ClassVar, Final

from user_pool.domain.exceptions.user import (
    PasswordRangeError,
    PasswordValueError,
)
from user_pool.domain.value_objects.base import ValueObject


@dataclass(slots=True, frozen=True)
class RawPassword(ValueObject[str]):
    """Represents an unencrypted (raw) password before hashing.

    Validation rules:
    - length must be between PASSWORD_MIN_LEN and PASSWORD_MAX_LEN
    - first character cannot be a digit
    """

    __PASSWORD_MIN_LEN: ClassVar[Final[int]] = 8
    __PASSWORD_MAX_LEN: ClassVar[Final[int]] = 36
    __PASSWORD_ALLOWED_CHARS: ClassVar[Final[str]] = (
        ascii_lowercase + digits + "_!$%"
    )

    @classmethod
    def _validate(cls, value: str) -> None:
        pass_len = len(value)
        if (
            pass_len < cls.__PASSWORD_MIN_LEN
            or pass_len > cls.__PASSWORD_MAX_LEN
        ):
            raise PasswordRangeError

        if value[0] in digits:
            raise PasswordValueError

        allowed = set(cls.__PASSWORD_ALLOWED_CHARS)

        for char in value.lower():
            if char not in allowed:
                raise PasswordValueError
