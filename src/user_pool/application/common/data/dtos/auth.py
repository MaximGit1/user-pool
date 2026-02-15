from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True, slots=True)
class ClientCreateRequest:
    email: str
    password: str

@dataclass(frozen=True, slots=True)
class Client:
    id: UUID
    email: str

@dataclass(frozen=True, slots=True)
class LoginRequest:
    email: str
    password: str

@dataclass(frozen=True, slots=True)
class AuthTokens:
    access: str
    refresh: str

@dataclass(frozen=True, slots=True)
class AccessPayload:
    user_id: str
    expires_at: datetime
    issued_at: datetime

type RefreshToken = str
type AccessToken = str


@dataclass(slots=True, frozen=True)
class AuthContext:
    user: Client
    new_access: str | None = None
    new_refresh: str | None = None