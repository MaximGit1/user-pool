from functools import partial

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from user_pool.application.common.exceptions.auth import ClientAlreadyExistsError, ClientNotFoundError, InvalidArgument, \
    UnauthenticatedError, InvalidTokenError, InternalError
from user_pool.application.common.exceptions.base import ApplicationError
from user_pool.application.common.exceptions.db import DataMapperError
from user_pool.application.common.exceptions.services import ServiceError
from user_pool.application.common.exceptions.users import (
    UserAlreadyLockedError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)
from user_pool.domain.exceptions.base import DomainError
from user_pool.domain.exceptions.user import (
    EmailValueError,
    PasswordRangeError,
    PasswordValueError,
    UsernameRangeError,
    UsernameValueError,
)

logger = structlog.getLogger(__name__)

ERROR_STATUS_MAPPING: dict[type[Exception], int] = {
    # Domain errors
    UsernameValueError: status.HTTP_400_BAD_REQUEST,
    UsernameRangeError: status.HTTP_400_BAD_REQUEST,
    EmailValueError: status.HTTP_400_BAD_REQUEST,
    PasswordValueError: status.HTTP_400_BAD_REQUEST,
    PasswordRangeError: status.HTTP_400_BAD_REQUEST,
    # Application errors
    UsernameAlreadyExistsError: status.HTTP_409_CONFLICT,
    UserAlreadyLockedError: status.HTTP_423_LOCKED,
    UserNotFoundError: status.HTTP_404_NOT_FOUND,
    DataMapperError: status.HTTP_501_NOT_IMPLEMENTED,
    ServiceError: status.HTTP_503_SERVICE_UNAVAILABLE,
    ClientAlreadyExistsError: status.HTTP_409_CONFLICT,
    ClientNotFoundError: status.HTTP_404_NOT_FOUND,
    InvalidArgument: status.HTTP_400_BAD_REQUEST,
    UnauthenticatedError: status.HTTP_401_UNAUTHORIZED,
    InvalidTokenError: status.HTTP_401_UNAUTHORIZED,
    InternalError: status.HTTP_500_INTERNAL_SERVER_ERROR,
    # General (default)
    DomainError: status.HTTP_400_BAD_REQUEST,
    ApplicationError: status.HTTP_400_BAD_REQUEST,
}


async def generic_error_handler(
    _: Request, exc: Exception, status_code: int
) -> ORJSONResponse:
    """A common handler for domain and application errors."""
    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(
            "Server error",
            error=f"{exc.__class__.__name__}: {exc}",
            exc_info=(type(exc), exc, exc.__traceback__),
        )
    else:
        warn_msg =  "Client error"
        logger.warning(
            warn_msg,
            error=f"{exc.__class__.__name__}: {exc}",
            exc_info=(type(exc), exc, exc.__traceback__),
        )

    return ORJSONResponse(content={
            "code": status_code,
            "message": str(exc),
        },
        status_code=status_code,
    )


async def validation_error_handler(
    _: Request, exc: RequestValidationError
) -> ORJSONResponse:
    """Handler for validation errors."""
    logger.warning("Validation error", error=str(exc))
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append(f"{field}: {error['msg']}")
    return ORJSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"code": status.HTTP_422_UNPROCESSABLE_ENTITY, "message": "Validation failed"},
    )


async def http_error_handler(_: Request, exc: HTTPException) -> ORJSONResponse:
    """Handler for HTTPException."""

    msg = f"HTTP {exc.status_code}"
    if exc.status_code >= 500:
        logger.error(msg, error=str(exc))
    else:
        logger.warning(msg, error=str(exc))

    return ORJSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=exc.headers,
    )


async def fallback_error_handler(
    request: Request, exc: Exception
) -> ORJSONResponse:
    """Fallback for all uncaught exceptions."""
    msg = "Unhandled exception",
    logger.critical(
        msg,
        error=f"{exc.__class__.__name__}: {exc}",
        path=request.url.path,
        method=request.method,
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return ORJSONResponse(
        content={"detail": "Internal server error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def init_exception_handlers(app_: FastAPI) -> None:
    """Configures exception handlers for the FastAPI application.

    Registration order:
    1. Specific exceptions
    2. Base classes
    3. HTTP and validation errors
    4. General fallback (last!)
    """

    for exc_type, http_status in ERROR_STATUS_MAPPING.items():
        app_.add_exception_handler(
            exc_type, partial(generic_error_handler, status_code=http_status)
        )

    app_.add_exception_handler(HTTPException, http_error_handler)
    app_.add_exception_handler(
        RequestValidationError, validation_error_handler
    )

    app_.exception_handler(Exception)(fallback_error_handler)
