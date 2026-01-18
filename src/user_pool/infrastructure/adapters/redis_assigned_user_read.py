from datetime import datetime
from uuid import UUID

from redis.asyncio import Redis

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.project import (
    Project,
    ProjectDomainEnum,
    ProjectEnvEnum,
)
from user_pool.domain.value_objects.user_id import UserID


class RedisAssignedUserReadRepository:
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def locked_user_ids(self, user_ids: list[UserID]) -> set[UserID]:
        if not user_ids:
            return set()

        async with self._client.pipeline(transaction=False) as pipe:
            for user_id in user_ids:
                await pipe.exists(self._get_key(user_id))

            results = await pipe.execute()

        return {user_ids[i] for i, exists in enumerate(results) if exists > 0}

    async def get_assignment(self, user_id: UserID) -> AssignedUser | None:
        data = await self._client.hgetall(self._get_key(user_id))
        if not data:
            return None

        return AssignedUser(
            _id=user_id,
            _project=Project(
                id=UUID(data["project_id"]),
                env=ProjectEnvEnum(data["project_env"]),
                domain=ProjectDomainEnum(data["project_domain"]),
            ),
            _locked_time=datetime.fromisoformat(data["locked_time"]),
        )

    async def exists(self, user_id: UserID) -> bool:
        return await self._client.exists(self._get_key(user_id)) > 0

    def _get_key(self, user_id: UserID) -> str:
        return f"assigned_user:{user_id.value}"
