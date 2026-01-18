from bazario.asyncio import Dispatcher
from bazario.asyncio.resolvers.dishka import DishkaResolver
from dishka import Provider, Scope, WithParents

from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.commands.user_locked import UserLockedHandler
from user_pool.application.commands.user_unlocked import UserUnlockedHandler
from user_pool.application.queries.get_user_id import RetrieveNewUserIDHandler
from user_pool.application.queries.health_checker import (
    RetrieveHealthRequestHandler,
)
from user_pool.application.queries.user_get_by_id import (
    RetrieveUserRequestHandler,
)
from user_pool.application.queries.user_is_locked import (
    RetrieveUserIsLockedRequestHandler,
)
from user_pool.application.queries.users_list import RetrieveUserShortHandler
from user_pool.setup.components.orchestration import bazario_handlers_registry


def bazario_provide() -> Provider:
    provider = Provider(scope=Scope.REQUEST)

    provider.provide(bazario_handlers_registry)
    provider.provide(WithParents[Dispatcher])
    provider.provide(WithParents[DishkaResolver])

    provider.provide_all(
        RetrieveNewUserIDHandler,
        RetrieveUserRequestHandler,
        RetrieveUserIsLockedRequestHandler,
        RetrieveUserShortHandler,
        UserCreatedHandler,
        UserLockedHandler,
        UserUnlockedHandler,
        RetrieveHealthRequestHandler,
    )

    return provider
