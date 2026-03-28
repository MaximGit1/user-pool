from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Security
from starlette import status
from starlette.responses import Response

from user_pool.application.commands.login import LoginHandler
from user_pool.application.commands.logout import LogoutHandler
from user_pool.application.commands.register import RegisterHandler
from user_pool.application.common.data.dtos.auth import (
    AccessToken,
    LoginRequest,
)
from user_pool.delivery.http.controllers.schemes.auth import RegisterSchema
from user_pool.delivery.http.http_response_schemes import (
    UNAUTHORIZED,
    BadRequest,
    InternalServerError,
    conflict,
)
from user_pool.delivery.http.response_data_editor import (
    delete_cookie,
    set_cookie,
)
from user_pool.delivery.http.secure import bearer_scheme

router = APIRouter(
    prefix="/auth", tags=["Auth system"], route_class=DishkaRoute
)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    responses={
        **BadRequest,
        **conflict("User already exists"),
        **InternalServerError,
    },
)
async def register(
    data: RegisterSchema, interactor: FromDishka[RegisterHandler]
) -> None:
    await interactor.handle(data.to_dto())


@router.post(
    "/login",
    responses={
        **BadRequest,
        **UNAUTHORIZED,
        **InternalServerError,
    },
)
async def login(
    interactor: FromDishka[LoginHandler],
    request: LoginRequest,
    response: Response,
) -> AccessToken:
    access_token, cookie_data = await interactor.handle(request)
    set_cookie(response, cookie_data)

    return access_token


@router.delete(
    "/logout",
    dependencies=[Security(bearer_scheme)],
    responses={
        **UNAUTHORIZED,
        **InternalServerError,
    },
)
async def logout(
    interactor: FromDishka[LogoutHandler], response: Response
) -> None:
    refresh_cookie_key = await interactor.handle()
    delete_cookie(response, refresh_cookie_key)
