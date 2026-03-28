from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from user_pool.application.commands.user_unlocked import UserUnlockedHandler
from user_pool.application.common.repositories import (
    AssignedUserWriteRepository,
)


@pytest.mark.asyncio
async def test_user_unlocked_handler_success():
    user_id_uuid = uuid4()

    mock_repo = MagicMock(spec=AssignedUserWriteRepository)
    mock_repo.remove = AsyncMock()

    handler = UserUnlockedHandler(assigned_user_repo=mock_repo)
    await handler.handle(user_id_uuid)

    mock_repo.remove.assert_called_once()

    called_user_id = mock_repo.remove.call_args[0][0]
    assert called_user_id.value == user_id_uuid
