from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from user_pool.application.common.data.dtos.auth import AuthContext, Client
from user_pool.application.common.repositories.auth.identity_provider import (
    IdentityProvider,
)
from user_pool.application.common.services.user_context import ProtectedManager


@pytest.mark.asyncio
async def test_protected_manager_returns_context():
    client = Client(id=uuid4(), email="authemail@gmail.com")
    expected_context = AuthContext(
        user=client, new_access="access_", new_refresh="refresh_"
    )

    mock_identity = MagicMock(spec=IdentityProvider)
    mock_identity.get_context = AsyncMock(return_value=expected_context)

    manager = ProtectedManager(identity=mock_identity)
    result = await manager()

    assert result == expected_context
    assert result.user.email == "authemail@gmail.com"

    mock_identity.get_context.assert_called_once()
