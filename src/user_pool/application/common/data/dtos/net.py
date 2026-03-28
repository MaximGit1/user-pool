from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CookieData:
    key: str
    value: str
    max_age: int
    httponly: bool = True
    secure: bool = True
    same_site: str = "lax"


@dataclass(frozen=True, slots=True)
class HeaderData:
    key: str
    value: str


type CookieKey = str
