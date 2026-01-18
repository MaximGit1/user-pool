from dataclasses import dataclass
from uuid import UUID

from user_pool.domain.value_objects.base import ValueObject


@dataclass(slots=True, frozen=True)
class UserID(ValueObject[UUID]):
    """ID for User domain entity"""

    def to_uuid(self) -> UUID:
        return self.value
