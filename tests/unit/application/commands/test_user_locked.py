from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from user_pool.application.commands.user_locked import UserLockedHandler
from user_pool.application.common.data.dtos.assigned_user import UserLocked
from user_pool.application.common.exceptions.users import (
    UserAlreadyLockedError,
)
from user_pool.application.common.repositories import (
    AssignedUserReadRepository,
    AssignedUserWriteRepository,
)
from user_pool.setup.config import CacheConfig


@pytest.mark.asyncio
async def test_user_locked_handler_success():
    # 1. Данные
    user_id_uuid = uuid4()
    notification = UserLocked(dto=MagicMock(), user_id=user_id_uuid)

    config = CacheConfig(assignment_ttl=3600, host="host", port=888, password="pass", client="mock_client")

    mock_read = MagicMock(spec=AssignedUserReadRepository)
    mock_read.exists = AsyncMock(return_value=False)

    mock_write = MagicMock(spec=AssignedUserWriteRepository)
    mock_write.assign = AsyncMock()

    handler = UserLockedHandler(config, mock_write, mock_read)
    await handler.handle(notification)

    mock_read.exists.assert_called_once()
    mock_write.assign.assert_called_once()
    args, kwargs = mock_write.assign.call_args
    assert kwargs["assignment_ttl"] == 3600
    assert kwargs["assigned_user"].id.value == user_id_uuid


@pytest.mark.asyncio
async def test_user_locked_handler_already_locked():
    user_id_uuid = uuid4()
    notification = UserLocked(dto=MagicMock(), user_id=user_id_uuid)
    config = CacheConfig(assignment_ttl=3600, host="host", port=888, password="pass", client="mock_client")

    mock_read = MagicMock(spec=AssignedUserReadRepository)
    mock_read.exists = AsyncMock(return_value=True)

    mock_write = MagicMock(spec=AssignedUserWriteRepository)

    handler = UserLockedHandler(config, mock_write, mock_read)


    with pytest.raises(UserAlreadyLockedError, match="user already locked"):
        await handler.handle(notification)

    mock_write.assign.assert_not_called()
