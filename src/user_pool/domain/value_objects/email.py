import re
from dataclasses import dataclass
from typing import ClassVar, Final

from user_pool.domain.exceptions.user import EmailValueError
from user_pool.domain.value_objects.base import ValueObject


@dataclass(slots=True, frozen=True)
class Email(ValueObject[str]):
    """Represents a user's email address.

    Accepted format:
    - local part: letters, digits, '.', '_', '%', '+', '-'
    - '@'
    - domain: letters, digits, '.', '-'
    - TLD: at least 3 letters
    """

    __EMAIL_REGEX: ClassVar[Final[re.Pattern]] = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
    )

    @classmethod
    def _validate(cls, value: str) -> None:
        if not cls.__EMAIL_REGEX.match(value):
            raise EmailValueError
