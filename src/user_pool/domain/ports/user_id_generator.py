from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from user_pool.domain.value_objects.user_id import UserID


class UserIDGenerator(Protocol):
    """Generates UserID VO"""

    def generate(self) -> UserID: ...
