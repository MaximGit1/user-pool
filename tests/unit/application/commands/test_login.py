from unittest.mock import AsyncMock, MagicMock

import pytest

from user_pool.application.commands.login import LoginHandler
from user_pool.application.common.data.dtos.auth import (
    AuthTokens,
    LoginRequest,
)
from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
)
from user_pool.setup.config import TokenConfig


@pytest.mark.asyncio
async def test_login_handler_success() -> None:
    request = LoginRequest(email="test@example.com", password="password123")
    config = TokenConfig(
        public_key=b"key",
        issuer="issuer",
        audience="aud",
        refresh_cookie_key="refresh_token",
        access_header_key="access",
        refresh_max_age=3600,
    )

    tokens = AuthTokens(access="access_123", refresh="refresh_456")

    mock_client = MagicMock(spec=AuthSSOClient)
    mock_client.login = AsyncMock(return_value=tokens)

    handler = LoginHandler(client=mock_client, token_config=config)
    access, cookie = await handler.handle(request)

    assert access == "access_123"
    assert cookie.value == "refresh_456"
    assert cookie.key == "refresh_token"
    assert cookie.max_age == 3600

    mock_client.login.assert_called_once_with(request)
