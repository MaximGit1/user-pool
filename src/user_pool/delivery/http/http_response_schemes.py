from typing import Any

from pydantic import BaseModel, create_model
from starlette import status


class ErrorResponse(BaseModel):
    code: int
    message: str


type ErrScheme = dict[str, Any]
type HttpResponses = dict[int, ErrScheme]


def create_http_response(
    class_name: str, code: int, message: str
) -> HttpResponses:
    return {
        code: {
            "model": create_model(class_name, __base__=ErrorResponse),
            "description": message,
            "content": {
                "application/json": {
                    "example": {"code": code, "message": message}
                }
            },
        }
    }



InternalServerError = create_http_response(
    class_name="InternalServerError",
    code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    message="Internal server error",
)

SERVICE_UNAVAILABLE = create_http_response(
    class_name="ServiceUnavailable",
    code=status.HTTP_503_SERVICE_UNAVAILABLE,
    message="Service is temporarily unavailable",
)

BadRequest = create_http_response(
    class_name="BadRequest",
    code=status.HTTP_400_BAD_REQUEST,
    message="Bad request",
)


def not_found(msg: str) -> HttpResponses:
    return create_http_response(
        class_name="NotFound",
        code=status.HTTP_404_NOT_FOUND,
        message=msg,
    )


def locked(msg: str) -> HttpResponses:
    return create_http_response(
        class_name="Locked",
        code=status.HTTP_423_LOCKED,
        message=msg,
    )


def conflict(msg: str) -> HttpResponses:
    return create_http_response(
        class_name="Conflict",
        code=status.HTTP_409_CONFLICT,
        message=msg,
    )
