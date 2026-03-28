from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.common.data.dtos.users import UserCreateDTO
from user_pool.application.common.repositories import (
    TransactionManager,
    UserWriteRepository,
)
from user_pool.domain.services import UserService
from user_pool.domain.value_objects import UserID


@pytest.mark.asyncio
async def test_user_created_handler_success():
    request = UserCreateDTO(username="testusername", email="useremail@gmail.com", password="passworddalhd")
    user_id_value = UserID.unsafe(uuid4())

    mock_user = MagicMock()
    mock_user.id.value = user_id_value

    mock_repo = MagicMock(spec=UserWriteRepository)
    mock_repo.add = AsyncMock()

    mock_transaction = MagicMock(spec=TransactionManager)
    mock_transaction.commit = AsyncMock()

    mock_service = MagicMock(spec=UserService)
    mock_service.create_user.return_value = mock_user

    handler = UserCreatedHandler(
        repo=mock_repo,
        transaction_manager=mock_transaction,
        service=mock_service,
    )

    result = await handler.handle(request)

    mock_service.create_user.assert_called_once_with(
        username=request.username,
        email=request.email,
        raw_password=request.password
    )
    mock_repo.add.assert_called_once_with(user=mock_user)
    mock_transaction.commit.assert_called_once()

    assert result == user_id_value
