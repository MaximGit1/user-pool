import logging

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status
from starlette.requests import Request

from user_pool.application.common.exceptions.auth import (
    ClientAlreadyExistsError,
    ClientNotFoundError,
    InternalError,
    InvalidArgument,
    InvalidTokenError,
    UnauthenticatedError,
)
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

logger = logging.getLogger(__name__)



class AppError(Exception):
    def __init__(self, original_exc: Exception, status_code: int, public_message: str) -> None:
        self.original_exc = original_exc
        self.status_code = status_code
        self.public_message = public_message
        super().__init__(str(original_exc))



type HttpStatus = int
type ErrPublicMessage = str

ERROR_STATUS_MAPPING: dict[type[Exception], tuple[HttpStatus, ErrPublicMessage]] = {
    # Domain errors
    UsernameValueError: (status.HTTP_400_BAD_REQUEST, "Invalid username"),
    UsernameRangeError: (status.HTTP_400_BAD_REQUEST, "Invalid username"),
    EmailValueError: (status.HTTP_400_BAD_REQUEST, "Invalid email"),
    PasswordValueError: (status.HTTP_400_BAD_REQUEST, "Invalid password"),
    PasswordRangeError: (status.HTTP_400_BAD_REQUEST, "Invalid password"),

    # Application errors
    UsernameAlreadyExistsError: (status.HTTP_409_CONFLICT, "Username already exists"),
    UserAlreadyLockedError: (status.HTTP_423_LOCKED, "User is already locked"),
    UserNotFoundError:(status.HTTP_404_NOT_FOUND, "User not found"),
    DataMapperError: (status.HTTP_501_NOT_IMPLEMENTED, "Data mapper error"),
    ServiceError: (status.HTTP_503_SERVICE_UNAVAILABLE, "Service unavailable"),
    ClientAlreadyExistsError: (status.HTTP_409_CONFLICT, "Client already exists"),
    ClientNotFoundError:  (status.HTTP_404_NOT_FOUND, "Client not found"),
    InvalidArgument: (status.HTTP_400_BAD_REQUEST, "Invalid argument"),
    UnauthenticatedError: (status.HTTP_401_UNAUTHORIZED, "Unauthorized"),
    InvalidTokenError: (status.HTTP_401_UNAUTHORIZED, "UNAUTHORIZED"),
    InternalError: (status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"),
    # General (default)
    DomainError: (status.HTTP_400_BAD_REQUEST, "Bad Request"),
    ApplicationError: (status.HTTP_400_BAD_REQUEST, "Bad Request"),
}


def wrap_domain_error(exc: Exception) -> AppError:
    if type(exc) in ERROR_STATUS_MAPPING:
        status_code, public_message = ERROR_STATUS_MAPPING[type(exc)]

        return AppError(original_exc=exc, status_code=status_code, public_message=public_message)


    return AppError(
        original_exc=exc,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        public_message="Internal server error",
    )

async def app_error_handler(request: Request, exc: AppError) -> ORJSONResponse:
    if exc.status_code >= 500:
        logger.error(
            "Server error",
            exc_info=exc.original_exc,
        )
    else:
        logger.warning(
            f"{type(exc.original_exc).__name__}: {exc.original_exc}"
        )

    return ORJSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.public_message},
    )


async def fallback_handler(_: Request, __: Exception) -> ORJSONResponse:
    logger.exception("Unhandled exception")

    return ORJSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

def init_exception_handlers(app_: FastAPI) -> None:
    """Configures exception handlers for the FastAPI application"""

    async def handler(request: Request, exc: Exception):
        wrapped = wrap_domain_error(exc)
        return await app_error_handler(request, wrapped)


    app_.add_exception_handler(ApplicationError, handler)
    app_.add_exception_handler(ApplicationError, handler)
    app_.add_exception_handler(Exception, fallback_handler)
