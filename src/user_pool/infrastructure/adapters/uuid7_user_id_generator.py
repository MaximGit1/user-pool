from uuid import UUID

from uuid_utils import uuid7

from user_pool.domain.value_objects.user_id import UserID


class UUID7UserIDGenerator:
    def generate(self) -> UserID:
        return UserID.unsafe(UUID(uuid7().hex))
