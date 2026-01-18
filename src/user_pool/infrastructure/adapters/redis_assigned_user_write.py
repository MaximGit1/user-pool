from redis.asyncio import Redis

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID


class RedisAssignedUserWriteRepository:
    def __init__(self, client: Redis) -> None:
        self._client = client

    async def assign(
        self, assigned_user: AssignedUser, assignment_ttl: int
    ) -> None:
        key = self._get_key(assigned_user.id)
        await self._client.hset(
            key,
            mapping={
                "project_id": str(assigned_user.project.id),
                "project_env": assigned_user.project.env.value,
                "project_domain": assigned_user.project.domain.value,
                "locked_time": assigned_user.locked_time.isoformat(),
            },
        )

        await self._client.expire(key, assignment_ttl)

    async def remove(self, user_id: UserID) -> None:
        await self._client.delete(self._get_key(user_id))

    def _get_key(self, user_id: UserID) -> str:
        return f"assigned_user:{user_id.value}"
