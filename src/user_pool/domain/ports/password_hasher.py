from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from user_pool.domain.value_objects.raw_password import RawPassword


class PasswordHasher(Protocol):
    """Password interface"""

    def hash(self, raw_password: RawPassword) -> bytes: ...
