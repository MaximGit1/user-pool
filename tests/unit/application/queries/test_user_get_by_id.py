from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4

import pytest

from user_pool.application.common.data.dtos.users import UserFullDTO
from user_pool.application.common.exceptions.users import UserNotFoundError
from user_pool.application.common.repositories import (
    AssignedUserReadRepository,
    UserReadRepository,
)
from user_pool.application.queries.user_get_by_id import (
    RetrieveUserRequestHandler,
)
from user_pool.domain.value_objects import UserID
from user_pool.domain.value_objects.project import (
    Project,
    ProjectDomainEnum,
    ProjectEnvEnum,
)


@pytest.fixture
def user_id():
    return uuid4()


@pytest.mark.asyncio
async def test_retrieve_user_success(user_id: UUID) -> None:
    mock_user = MagicMock()
    mock_user.username.value = "custom_username"
    mock_user.email.value = "email_custom@example.com"
    mock_user.hashed_password = "secret_hash_some_pass"
    mock_user.created_at = datetime.now(UTC)

    user_repo = MagicMock(spec=UserReadRepository)
    user_repo.get_by_id = AsyncMock(return_value=mock_user)

    project_vo = Project(
        id=uuid4(), env=ProjectEnvEnum.Prod, domain=ProjectDomainEnum.Regular
    )

    mock_assignment = MagicMock()
    mock_assignment.locked_time = datetime.now(UTC)
    mock_assignment.project = project_vo

    assigned_repo = MagicMock(spec=AssignedUserReadRepository)
    assigned_repo.get_assignment = AsyncMock(return_value=mock_assignment)

    handler = RetrieveUserRequestHandler(user_repo, assigned_repo)
    result = await handler.handle(user_id)

    assert isinstance(result, UserFullDTO)
    assert result.user_id == user_id
    assert result.username == "custom_username"
    assert result.email == "email_custom@example.com"

    assert result.lock is not None
    assert result.lock.locked_by == project_vo
    assert result.lock.locked_by.env == ProjectEnvEnum.Prod

    user_repo.get_by_id.assert_called_once()
    args, _ = user_repo.get_by_id.call_args
    assert isinstance(args[0], UserID)


@pytest.mark.asyncio
async def test_retrieve_user_not_found(user_id: UUID) -> None:
    user_repo = MagicMock(spec=UserReadRepository)
    user_repo.get_by_id = AsyncMock(return_value=None)

    assigned_repo = MagicMock(spec=AssignedUserReadRepository)
    handler = RetrieveUserRequestHandler(user_repo, assigned_repo)

    with pytest.raises(UserNotFoundError, match="User not found"):
        await handler.handle(user_id)

    assigned_repo.get_assignment.assert_not_called()
