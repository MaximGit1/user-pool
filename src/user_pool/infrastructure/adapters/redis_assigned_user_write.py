from redis.asyncio import Redis

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects.user_id import UserID


class RedisAssignedUserWriteRepository:
    def __init__(self, client: Redis) -> None:
        self._client = client
        self._assigned_users_index_key = "assigned_user:index"

    async def assign(
        self, assigned_user: AssignedUser, assignment_ttl: int
    ) -> None:
        key = self._get_key(assigned_user.id)

        async with self._client.pipeline(transaction=True) as pipe:
            await pipe.hset(
                key,
                mapping={
                    "project_id": str(assigned_user.project.id),
                    "project_env": assigned_user.project.env.value,
                    "project_domain": assigned_user.project.domain.value,
                    "locked_time": assigned_user.locked_time.isoformat(),
                },
            )
            await pipe.expire(key, assignment_ttl)
            await pipe.sadd(self._assigned_users_index_key, key)
            await pipe.execute()

    async def remove(self, user_id: UserID) -> None:
        key = self._get_key(user_id)

        async with self._client.pipeline(transaction=True) as pipe:
            await pipe.delete(key)
            await pipe.srem(self._assigned_users_index_key, key)
            await pipe.execute()

    async def remove_all(self) -> None:
        keys = await self._client.smembers(self._assigned_users_index_key)

        if not keys:
            return

        async with self._client.pipeline(transaction=False) as pipe:
            for key in keys:
                await pipe.exists(key)
            exists = await pipe.execute()

        real_keys = [k for k, e in zip(keys, exists) if e]

        async with self._client.pipeline(transaction=True) as pipe:
            if real_keys:
                await pipe.delete(*real_keys)

            await pipe.delete(self._assigned_users_index_key)
            await pipe.execute()

    def _get_key(self, user_id: UserID) -> str:
        return f"assigned_user:{user_id.value}"
