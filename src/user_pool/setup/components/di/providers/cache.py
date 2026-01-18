from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from user_pool.application.common.repositories.checkers import (
    CacheConnectionChecker,
)
from user_pool.infrastructure.adapters.redis_cache_connection_checker import (
    RedisCacheConnectionChecker,
)
from user_pool.setup.config import CacheConfig


class CacheProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_redis(
        self,
        config: CacheConfig,
    ) -> AsyncIterator[Redis]:
        client = Redis.from_url(
            config.uri,
            decode_responses=True,
        )
        yield client

        await client.close()


def cache_health_check() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        RedisCacheConnectionChecker, provides=CacheConnectionChecker
    )

    return provider


def get_cache_providers() -> list[Provider]:
    return [
        cache_health_check(),
        CacheProvider(),
    ]
