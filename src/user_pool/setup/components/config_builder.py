import os
import re
from datetime import timedelta
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml


class StartMode(StrEnum):
    Dev = "dev"
    Test = "test"


class ConfigBuilder:
    _DURATION_PATTERN = re.compile(r"^(?P<value>\d+)(?P<unit>[smhd])$")

    @classmethod
    def config_path(cls) -> Path:
        return Path(__file__).resolve().parents[4] / "configs" / "config"

    @classmethod
    def load_yaml(cls) -> dict[str, Any]:
        path = cls.config_path() / "config.yaml"

        if not path.exists():
            raise RuntimeError(f"Config file not found: {path}")

        with path.open() as f:
            raw = yaml.safe_load(f)

        base = raw.get("default", {})
        override = raw.get(cls._select_mode().value, {})
        return cls._deep_merge(base, override)

    @classmethod
    def _deep_merge(cls, base: dict, override: dict) -> dict:
        result = dict(base)
        for key, value in override.items():
            if isinstance(value, dict) and isinstance(result.get(key), dict):
                result[key] = cls._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @classmethod
    def _select_mode(cls) -> StartMode:
        value = os.getenv("ENV")
        match value:
            case StartMode.Test:
                return StartMode.Test
            case StartMode.Dev:
                return StartMode.Dev
            case _:
                err_msg = "Unknown environment 'ENV' "
                raise RuntimeError(err_msg)

    @classmethod
    def parse_duration(cls, value: str) -> int:
        match = cls._DURATION_PATTERN.match(value.strip())
        if not match:
            raise ValueError(f"Invalid duration format: {value}")

        amount = int(match.group("value"))
        unit = match.group("unit")

        delta = timedelta(seconds=0)

        match unit:
            case "s":
                delta = timedelta(seconds=amount)
            case "m":
                delta = timedelta(minutes=amount)
            case "h":
                delta = timedelta(hours=amount)
            case "d":
                delta = timedelta(days=amount)
            case _:
                raise ValueError(f"Unsupported duration unit: {unit}")

        return int(delta.total_seconds())
