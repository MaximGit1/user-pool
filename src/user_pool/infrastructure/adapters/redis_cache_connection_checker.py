from logging import getLogger

from redis.asyncio import Redis, RedisError

log = getLogger(__name__)


def __init__(self, redis_client: Redis) -> None:
    self._redis = redis_client


class RedisCacheConnectionChecker:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def check(self) -> bool:
        try:
            response = await self._redis.ping()

            if response is True or response == b"PONG" or response == "PONG":
                return True
            return False
        except RedisError as e:
            log.error(f"Redis connection check failed: {e}")
            return False
        except Exception as e:
            err_msg = f"Unexpected error during Redis check: {e}"
            log.critical(err_msg)
            return False
