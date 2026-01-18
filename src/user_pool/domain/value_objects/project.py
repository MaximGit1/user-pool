from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID


class ProjectDomainEnum(StrEnum):
    Canary = "canary"
    Regular = "regular"


class ProjectEnvEnum(StrEnum):
    Prod = "prod"
    Preprod = "preprod"
    Stage = "stage"


@dataclass(slots=True, kw_only=True, frozen=True)
class Project:
    id: UUID
    env: ProjectEnvEnum
    domain: ProjectDomainEnum
