from unittest.mock import AsyncMock, MagicMock

import pytest

from user_pool.application.commands.register import RegisterHandler
from user_pool.application.common.data.dtos.auth import ClientCreateRequest
from user_pool.application.common.repositories.auth.sso_clients import (
    UserSSOClient,
)


@pytest.mark.asyncio
async def test_register_handler_success():
    request = ClientCreateRequest(
        email="new_user@example.com",
        password="secure_password"
    )

    mock_client = MagicMock(spec=UserSSOClient)
    mock_client.create = AsyncMock()

    handler = RegisterHandler(client=mock_client)

    result = await handler.handle(request)

    mock_client.create.assert_called_once_with(request)

    assert result is None
