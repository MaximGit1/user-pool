from datetime import UTC, datetime
from uuid import uuid4

from user_pool.domain.entities.assigned_user import AssignedUser
from user_pool.domain.value_objects import UserID
from user_pool.domain.value_objects.project import (
    Project,
    ProjectDomainEnum,
    ProjectEnvEnum,
)


def test_properties() -> None:
    user_project = Project(
        id=uuid4(),
        env=ProjectEnvEnum.Prod,
        domain=ProjectDomainEnum.Canary,
    )

    locked_time = datetime.now(UTC)

    user = AssignedUser(
        _id=UserID.unsafe(uuid4()),
        _locked_time=locked_time,
        _project=user_project,
    )

    assert user.project == user_project
    assert user.locked_time == locked_time
