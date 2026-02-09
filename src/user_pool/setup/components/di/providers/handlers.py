from dishka import Provider, Scope

from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.commands.user_locked import UserLockedHandler
from user_pool.application.commands.user_unlocked import UserUnlockedHandler
from user_pool.application.queries.health_checker import (
    RetrieveHealthRequestHandler,
)
from user_pool.application.queries.user_get_by_id import (
    RetrieveUserRequestHandler,
)
from user_pool.application.queries.users_list import RetrieveUserShortHandler
from user_pool.domain.services.user import UserService


def handler_query_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(RetrieveUserRequestHandler)
    provider.provide(RetrieveUserShortHandler)

    return provider


def handler_command_provider() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(UserCreatedHandler)
    provider.provide(UserLockedHandler)
    provider.provide(UserUnlockedHandler)
    provider.provide(RetrieveHealthRequestHandler)

    return provider


def domain_service_provider() -> Provider:
    provider = Provider()

    provider.provide(UserService, scope=Scope.APP)

    return provider


def get_handler_providers() -> list[Provider]:
    return [
        handler_query_provider(),
        handler_command_provider(),
        domain_service_provider(),
    ]
