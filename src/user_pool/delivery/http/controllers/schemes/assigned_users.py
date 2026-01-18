from uuid import UUID

from pydantic import BaseModel

from user_pool.domain.value_objects.project import (
    Project,
    ProjectDomainEnum,
    ProjectEnvEnum,
)


class ProjectScheme(BaseModel):
    project_id: UUID
    project_env: ProjectEnvEnum
    project_domain: ProjectDomainEnum

    def to_dto(self) -> Project:
        return Project(
            id=self.project_id,
            env=self.project_env,
            domain=self.project_domain,
        )
