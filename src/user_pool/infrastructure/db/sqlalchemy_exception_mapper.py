from sqlalchemy.exc import SQLAlchemyError

from user_pool.application.common.exceptions.base import ApplicationError
from user_pool.application.common.exceptions.db import DataMapperError
from user_pool.application.common.repositories.db_exception_mapper import (
    ExceptionRule,
)


class SqlAlchemyExceptionMapper:
    """Mapper for converting SQLAlchemy exceptions."""

    def __init__(self, rules: list[ExceptionRule]) -> None:
        self._rules = rules

    def map(self, exc: Exception) -> ApplicationError:
        """Converts a SQLAlchemy exception to a domain exception."""

        for rule in self._rules:
            try:
                mapped = rule.try_map(exc)
                if mapped is not None:
                    raise mapped
            except Exception as rule_exc:
                raise rule_exc

        if isinstance(exc, SQLAlchemyError):
            err_msg = f"Database error: {exc}"
            raise DataMapperError(err_msg)
        err_msg = f"Unexpected error: {exc}"
        raise DataMapperError(err_msg)
