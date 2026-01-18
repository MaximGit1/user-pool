import logging
import os
from typing import Any, NamedTuple, Self

from user_pool.setup.components.config_builder import ConfigBuilder


class Config(NamedTuple):
    asgi: ASGIConfig
    logging: LoggingConfig
    db: DBConfig
    cache: CacheConfig


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


def create_config() -> Config:
    yaml_cfg = ConfigBuilder.load_yaml()

    return Config(
        asgi=ASGIConfig(**yaml_cfg["asgi"]),
        logging=LoggingConfig.from_sources(yaml_cfg["logging"]),
        db=DBConfig.from_sources(yaml_cfg["db"]),
        cache=CacheConfig.from_sources(yaml_cfg["cache"]),
    )


def _get_env(key: str) -> str:
    value = os.getenv(key)

    if not value:
        err_msg = f"could not find environment variable '{key}'"
        raise RuntimeError(err_msg)

    return value
