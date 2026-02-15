import logging
import os
from pathlib import Path
from typing import Any, NamedTuple, Self

from user_pool.setup.components.config_builder import ConfigBuilder


class Config(NamedTuple):
    asgi: ASGIConfig
    logging: LoggingConfig
    db: DBConfig
    cache: CacheConfig
    tokens: TokenConfig
    auth_grpc_client: AuthGRPCClientConfig

class ASGIConfig(NamedTuple):
    host: str
    port: int
    debug: bool


class LoggingConfig(NamedTuple):
    level: int
    json_format: bool

    @classmethod
    def from_sources(cls, yaml_cfg: dict[str, Any]) -> Self:
        level_name = yaml_cfg["level"]
        try:
            level = logging._nameToLevel[level_name]
        except KeyError as exc:
            raise RuntimeError(f"Invalid logging level: {level_name}") from exc

        return cls(
            level=level,
            json_format=yaml_cfg["json_format"],
        )


class DBConfig(NamedTuple):
    user: str
    password: str
    host: str
    port: int
    db_name: str
    debug: bool

    @property
    def uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"  # asyncpg
            f"@{self.host}:{self.port}/{self.db_name}"
        )

    @classmethod
    def from_sources(cls, yaml_cfg: dict[str, Any]) -> Self:
        return cls(
            user=_get_env("DB_USER"),
            password=_get_env("DB_PASSWORD"),
            host=_get_env("DB_HOST"),
            port=int(_get_env("DB_PORT")),
            db_name=_get_env("DB_NAME"),
            debug=yaml_cfg["debug"],
        )


class CacheConfig(NamedTuple):
    assignment_ttl: int
    host: str
    port: int
    password: str
    client: str

    @property
    def uri(self) -> str:
        auth = f":{self.password}@" if self.password else ""
        return f"{self.client}://{auth}{self.host}:{self.port}"

    @classmethod
    def from_sources(cls, yaml_cfg: dict[str, Any]) -> Self:
        return cls(
            assignment_ttl=yaml_cfg["assignment_ttl"],
            host=_get_env("REDIS_HOST"),
            port=int(_get_env("REDIS_PORT")),
            password=_get_env("REDIS_PASSWORD"),
            client=yaml_cfg["client"],
        )


class TokenConfig(NamedTuple):
    public_key: bytes
    issuer: str
    audience: str
    refresh_cookie_key: str
    access_header_key: str
    refresh_max_age: int

    @classmethod
    def from_sources(cls, yaml_cfg: dict[str, Any]) -> "TokenConfig":
        path = Path(__file__).resolve().parents[3] / yaml_cfg["public_key_path"]

        if not path.exists():
            raise RuntimeError(f"JWT public key not found: {path}")

        return cls(
            public_key=path.read_bytes(),
            issuer=yaml_cfg["issuer"],
            audience=yaml_cfg["audience"],
            refresh_cookie_key=yaml_cfg["refresh_cookie_key"],
            access_header_key=yaml_cfg["access_header_key"],
            refresh_max_age=ConfigBuilder.parse_duration(yaml_cfg["refresh_cookie_max_age"]),
        )


class AuthGRPCClientConfig(NamedTuple):
    host: str
    port: int
    secret_key: str
    secret_key_value: str
    timeout: int

    @classmethod
    def from_sources(cls) -> Self:
        return cls(
            host=_get_env("AUTH_GRPC_CLIENT_HOST"),
            port=int(_get_env("AUTH_GRPC_CLIENT_PORT")),
            secret_key=_get_env("AUTH_GRPC_CLIENT_SECRET_KEY"),
            secret_key_value=_get_env("AUTH_GRPC_CLIENT_SECRET_KEY_VALUE"),
            timeout=int(_get_env("AUTH_GRPC_CLIENT_TIMEOUT"))
        )


def create_config() -> Config:
    yaml_cfg = ConfigBuilder.load_yaml()

    return Config(
        asgi=ASGIConfig(**yaml_cfg["asgi"]),
        logging=LoggingConfig.from_sources(yaml_cfg["logging"]),
        db=DBConfig.from_sources(yaml_cfg["db"]),
        cache=CacheConfig.from_sources(yaml_cfg["cache"]),
        tokens=TokenConfig.from_sources(yaml_cfg["auth"]),
        auth_grpc_client=AuthGRPCClientConfig.from_sources()
    )


def _get_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        err_msg = f"could not find environment variable '{key}'"
        raise RuntimeError(err_msg)

    return value
