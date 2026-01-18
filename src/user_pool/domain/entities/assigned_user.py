from dataclasses import dataclass
from datetime import datetime

from user_pool.domain.entities.base import BaseEntity
from user_pool.domain.value_objects.project import Project
from user_pool.domain.value_objects.user_id import UserID


@dataclass(slots=True, kw_only=True)
class AssignedUser(BaseEntity[UserID]):
    _project: Project
    _locked_time: datetime

    @property
    def project(self) -> Project:
        return self._project

    @property
    def locked_time(self) -> datetime:
        return self._locked_time
