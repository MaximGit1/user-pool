from uuid import UUID

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends, Security
from starlette import status
from starlette.responses import Response

from user_pool.application.commands.all_users_unclocked import (
    AllUsersUnlockedHandler,
)
from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.commands.user_locked import (
    UserLocked,
    UserLockedHandler,
)
from user_pool.application.commands.user_unlocked import UserUnlockedHandler
from user_pool.application.common.data.dtos.users import (
    UserFullDTO,
    UserShortDTO,
)
from user_pool.application.common.services.user_context import ProtectedManager
from user_pool.application.queries.user_get_by_id import (
    RetrieveUserRequestHandler,
)
from user_pool.application.queries.users_list import RetrieveUserShortHandler
from user_pool.delivery.http.controllers.schemes.assigned_users import (
    ProjectScheme,
)
from user_pool.delivery.http.controllers.schemes.users import (
    UserCreateScheme,
    UsersListScheme,
)
from user_pool.delivery.http.http_response_schemes import (
    UNAUTHORIZED,
    BadRequest,
    InternalServerError,
    conflict,
    locked,
    not_found,
)
from user_pool.delivery.http.secure import ContextResolver, bearer_scheme

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def get_users(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[RetrieveUserShortHandler],
    filters: UsersListScheme = Depends(),
) -> list[UserShortDTO]:
    """Returns a list of users"""

    context.resolve_context(response, await protection())
    return await interactor.handle(filters.to_dto())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        **InternalServerError,
        **BadRequest,
        **conflict("User already exists"),
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def create_user(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[UserCreatedHandler],
    create_data: UserCreateScheme = Body(...),
) -> UUID:
    context.resolve_context(response, await protection())
    return await interactor.handle(create_data.to_dto())


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def get_user_by_id(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[RetrieveUserRequestHandler],
    user_id: UUID,
) -> UserFullDTO:
    context.resolve_context(response, await protection())
    return await interactor.handle(user_id)


@router.post(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
        **locked("User is already locked"),
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def acquire_lock(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[UserLockedHandler],
    user_id: UUID,
    lock_data: ProjectScheme = Body(...),
) -> None:
    context.resolve_context(response, await protection())
    await interactor.handle(
        UserLocked(
            dto=lock_data.to_dto(),
            user_id=user_id,
        )
    )


@router.delete(
    "/unlock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def release_all(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[AllUsersUnlockedHandler],
) -> None:
    context.resolve_context(response, await protection())
    await interactor.handle()


@router.delete(
    "/{user_id}/unlock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
        **UNAUTHORIZED,
    },
    dependencies=[Security(bearer_scheme)],
)
async def release_lock(
    response: Response,
    protection: FromDishka[ProtectedManager],
    context: FromDishka[ContextResolver],
    interactor: FromDishka[UserUnlockedHandler],
    user_id: UUID,
) -> None:
    context.resolve_context(response, await protection())
    await interactor.handle(user_id=user_id)
