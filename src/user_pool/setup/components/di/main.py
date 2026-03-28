from dishka import AsyncContainer, Provider, make_async_container

from user_pool.setup.components.di.providers.adapters import (
    ports_provider,
    repositories_provider,
)
from user_pool.setup.components.di.providers.cache import get_cache_providers
from user_pool.setup.components.di.providers.config import ConfigProvider
from user_pool.setup.components.di.providers.db import get_db_providers
from user_pool.setup.components.di.providers.handlers import (
    get_handlers_providers,
)
from user_pool.setup.components.di.providers.net import get_net_providers
from user_pool.setup.config import Config


def get_adapters_providers() -> list[Provider]:
    return [
        ConfigProvider(),
        *get_db_providers(),
        *get_cache_providers(),
        ports_provider(),
        repositories_provider(),
    ]


def container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        *get_adapters_providers(),
        *get_handlers_providers(),
        *get_net_providers(),
        context={Config: config},
    )
