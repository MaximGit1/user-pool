import logging
import sys
from typing import final

import structlog

from user_pool.setup.config import LoggingConfig


@final
class StructlogConfig:
    def __init__(self, level: int = logging.INFO, *, json_format: bool = True):
        self._level = level
        self._json_format = json_format
        self.configure()

    _configured = False

    def configure(self):
        self._configure_structlog()
        self._configure_logging()
        self._override_handlers()

    def _configure_structlog(self) -> None:
        if getattr(self, "_structlog_configured", False):
            return

        def add_trace(_, __, event_dict):
            exc_info = event_dict.pop("exc_info", None)
            if exc_info:
                import traceback

                event_dict["trace"] = "".join(
                    traceback.format_exception(*exc_info)
                )
            return event_dict

        structlog.configure_once(
            processors=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                add_trace,
                structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )
        self._structlog_configured = True

    def _configure_logging(self) -> None:
        renderer = (
            structlog.processors.JSONRenderer()
            if self._json_format
            else structlog.dev.ConsoleRenderer()
        )
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt="iso"),
            ],
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                renderer,
            ],
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        root = logging.getLogger()
        root.handlers.clear()
        root.addHandler(handler)
        root.setLevel(self._level)

    def _override_handlers(self) -> None:
        if not self._json_format:
            return
        renderer = structlog.processors.JSONRenderer()
        formatter = structlog.stdlib.ProcessorFormatter(
            foreign_pre_chain=[
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
                structlog.processors.TimeStamper(fmt="iso"),
            ],
            processors=[
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                renderer,
            ],
        )
        for logger_name in (
            "uvicorn",
            "uvicorn.error",
            "uvicorn.access",
            "gunicorn",
            "gunicorn.error",
            "gunicorn.access",
        ):
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(self._level)
            logger.propagate = False


def init_logger(config: LoggingConfig) -> logging.Logger:
    StructlogConfig(level=config.level, json_format=config.json_format)

    return logging.getLogger("setup")
