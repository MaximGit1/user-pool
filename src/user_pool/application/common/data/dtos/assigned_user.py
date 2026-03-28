from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from user_pool.domain.value_objects.project import Project


@dataclass(frozen=True, slots=True)
class UserLockDTO:
    locked_time: datetime
    locked_by: Project

@dataclass(frozen=True, slots=True)
class UserLocked:
    dto: Project
    user_id: UUID
