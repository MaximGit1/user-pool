from unittest.mock import AsyncMock

import pytest

from user_pool.application.commands.all_users_unclocked import (
    AllUsersUnlockedHandler,
)
from user_pool.application.common.repositories import (
    AssignedUserWriteRepository,
)


@pytest.mark.asyncio
async def test_all_users_unlocked_handler_calls_remove_all() -> None:
    repo = AsyncMock(spec=AssignedUserWriteRepository)
    handler = AllUsersUnlockedHandler(assigned_user_repo=repo)

    await handler.handle()

    repo.remove_all.assert_awaited_once()
