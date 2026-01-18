from dataclasses import dataclass
from datetime import datetime

from user_pool.domain.value_objects.project import Project



@dataclass(frozen=True, slots=True)
class UserLockDTO:
    locked_time: datetime
    locked_by: Project
