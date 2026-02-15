from dishka import Provider, Scope

from user_pool.application.commands.login import LoginHandler
from user_pool.application.commands.logout import LogoutHandler
from user_pool.application.commands.register import RegisterHandler
from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.commands.user_locked import UserLockedHandler
from user_pool.application.commands.user_unlocked import UserUnlockedHandler
from user_pool.application.common.services.user_context import ProtectedManager
from user_pool.application.queries.health_checker import (
    HealthRequestHandler,
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
    provider.provide(HealthRequestHandler)
    provider.provide(RegisterHandler)
    provider.provide(LoginHandler)
    provider.provide(LogoutHandler)

    return provider


def domain_service_provider() -> Provider:
    provider = Provider()

    provider.provide(UserService, scope=Scope.APP)

    return provider


def other_services_provider() -> Provider:
    provider = Provider()

    provider.provide(ProtectedManager, scope=Scope.REQUEST)

    return provider


def get_handlers_providers() -> list[Provider]:
    return [
        handler_query_provider(),
        handler_command_provider(),
        domain_service_provider(),
        other_services_provider(),
    ]
