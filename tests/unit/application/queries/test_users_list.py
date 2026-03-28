from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from user_pool.application.common.data.dtos.users import (
    RetrieveUsersListRequest,
)
from user_pool.application.common.data.filters.users import UserFilter
from user_pool.application.common.data.pagination import Pagination
from user_pool.application.common.repositories import (
    AssignedUserReadRepository,
    UserReadRepository,
)
from user_pool.application.queries.users_list import RetrieveUserShortHandler
from user_pool.domain.entities import User
from user_pool.domain.value_objects import UserID


@pytest.mark.asyncio
async def test_retrieve_user_short_list_success():
    user_id_1 = UserID.unsafe(uuid4())
    user_id_2 =  UserID.unsafe(uuid4())
    now = datetime.now(UTC)

    user_1 = MagicMock(spec=User)
    user_1.id = user_id_1
    user_1.created_at = now

    user_2 = MagicMock(spec=User)
    user_2.id = user_id_2
    user_2.created_at = now

    user_repo = MagicMock(spec=UserReadRepository)
    user_repo.list = AsyncMock(return_value=[user_1, user_2])

    assigned_repo = MagicMock(spec=AssignedUserReadRepository)
    assigned_repo.locked_user_ids = AsyncMock(return_value={user_id_1})

    request = MagicMock(spec=RetrieveUsersListRequest)
    request.filters = UserFilter(username="test")
    request.pagination = Pagination(limit=10)

    handler = RetrieveUserShortHandler(user_repo, assigned_repo)
    result = await handler.handle(request)

    assert len(result) == 2

    assert result[0].user_id == user_id_1.value
    assert result[0].is_locked is True

    assert result[1].user_id == user_id_2.value
    assert result[1].is_locked is False

    assigned_repo.locked_user_ids.assert_called_once_with([user_id_1, user_id_2])

    user_repo.list.assert_called_once_with(
        filters=request.filters,
        pagination=request.pagination
    )
