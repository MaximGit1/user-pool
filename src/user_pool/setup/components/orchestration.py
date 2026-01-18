from bazario.asyncio import Registry

from user_pool.application.commands.user_created import (
    UserCreated,
    UserCreatedHandler,
)
from user_pool.application.commands.user_locked import (
    UserLocked,
    UserLockedHandler,
)
from user_pool.application.commands.user_unlocked import (
    UserUnlocked,
    UserUnlockedHandler,
)
from user_pool.application.queries.get_user_id import (
    RetrieveNewUserIDHandler,
    RetrieveNewUserIDRequest,
)
from user_pool.application.queries.health_checker import (
    RetrieveHealthRequest,
    RetrieveHealthRequestHandler,
)
from user_pool.application.queries.user_get_by_id import (
    RetrieveUserRequest,
    RetrieveUserRequestHandler,
)
from user_pool.application.queries.user_is_locked import (
    RetrieveUserIsLockedRequest,
    RetrieveUserIsLockedRequestHandler,
)
from user_pool.application.queries.users_list import (
    RetrieveUserShortHandler,
    RetrieveUsersListRequest,
)


def bazario_handlers_registry() -> Registry:
    registry = Registry()

    registry.add_request_handler(
        RetrieveNewUserIDRequest, RetrieveNewUserIDHandler
    )
    registry.add_request_handler(
        RetrieveUserRequest, RetrieveUserRequestHandler
    )
    registry.add_request_handler(
        RetrieveUserIsLockedRequest, RetrieveUserIsLockedRequestHandler
    )
    registry.add_request_handler(
        RetrieveUsersListRequest, RetrieveUserShortHandler
    )
    registry.add_request_handler(
        RetrieveHealthRequest, RetrieveHealthRequestHandler
    )

    registry.add_notification_handlers(UserCreated, UserCreatedHandler)
    registry.add_notification_handlers(UserLocked, UserLockedHandler)
    registry.add_notification_handlers(UserUnlocked, UserUnlockedHandler)

    return registry
