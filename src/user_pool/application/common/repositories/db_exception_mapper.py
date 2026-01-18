from typing import Protocol

from user_pool.application.common.exceptions.base import ApplicationError


class DBExceptionMapper(Protocol):
    """Mapper for converting database exceptions to domain exceptions."""

    def map(self, exc: Exception) -> ApplicationError:
        """Converts a database exception to a domain exception."""


class ExceptionRule(Protocol):
    """Rule for transforming exceptions."""

    def try_map(self, exc: Exception) -> ApplicationError | None:
        """Tries to transform an exception. Returns None if unable to do so."""
