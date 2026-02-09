from dishka import AsyncContainer, Provider, make_async_container

from user_pool.setup.components.di.providers.adapters import port_provider
from user_pool.setup.components.di.providers.cache import get_cache_providers
from user_pool.setup.components.di.providers.config import ConfigProvider
from user_pool.setup.components.di.providers.db import get_db_providers
from user_pool.setup.components.di.providers.handlers import (
    get_handler_providers,
)

from user_pool.setup.config import Config


def get_adapters_providers() -> list[Provider]:
    return [
        ConfigProvider(),
        *get_db_providers(),
        *get_cache_providers(),
        port_provider(),
    ]


def container_factory(config: Config) -> AsyncContainer:
    return make_async_container(
        *get_adapters_providers(),
        *get_handler_providers(),
        context={Config: config},
    )
