from dataclasses import dataclass


@dataclass(frozen=True)
class UserFilter:
    username: str | None = None
    email: str | None = None
