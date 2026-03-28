from unittest.mock import AsyncMock, MagicMock

import pytest

from user_pool.application.commands.logout import LogoutHandler
from user_pool.application.common.repositories.auth.sso_clients import (
    AuthSSOClient,
)
from user_pool.application.common.repositories.auth.tokenTransportManager import (
    HttpTokenTransportManager,
)
from user_pool.setup.config import TokenConfig


@pytest.mark.asyncio
async def test_logout_handler_success():
    refresh_token = "refresh_token_key"
    cookie_key = "refresh_token_key"

    config = TokenConfig(
        public_key=b"key",
        issuer="issuer",
        audience="aud",
        refresh_cookie_key=cookie_key,
        access_header_key="access",
        refresh_max_age=3600
    )

    mock_transport = MagicMock(spec=HttpTokenTransportManager)
    mock_transport.get_refresh.return_value = refresh_token

    mock_client = MagicMock(spec=AuthSSOClient)
    mock_client.logout = AsyncMock()

    handler = LogoutHandler(
        client=mock_client,
        token_transport=mock_transport,
        token_config=config
    )

    result = await handler.handle()

    mock_transport.get_refresh.assert_called_once()

    mock_client.logout.assert_called_once_with(refresh_token)

    assert result == cookie_key
