from uuid import UUID


from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends
from starlette import status

from user_pool.application.commands.user_created import UserCreatedHandler
from user_pool.application.commands.user_locked import UserLocked, UserLockedHandler
from user_pool.application.commands.user_unlocked import  UserUnlockedHandler
from user_pool.application.common.data.dtos.users import (
    UserFullDTO,
    UserShortDTO,
)

from user_pool.application.queries.user_get_by_id import RetrieveUserRequestHandler
from user_pool.application.queries.users_list import RetrieveUserShortHandler
from user_pool.delivery.http.controllers.schemes.assigned_users import (
    ProjectScheme,
)
from user_pool.delivery.http.controllers.schemes.users import (
    UserCreateScheme,
    UsersListScheme,
)
from user_pool.delivery.http.http_response_schemes import (
    BadRequest,
    InternalServerError,
    conflict,
    locked,
    not_found,
)

router = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
    },
    #dependencies=[Security(bearer_scheme)],
)
async def get_users(
    interactor: FromDishka[RetrieveUserShortHandler],
    filters: UsersListScheme = Depends(),
) -> list[UserShortDTO]:
    """Returns a list of users"""
    return await interactor.handle(filters.to_dto())


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        **InternalServerError,
        **BadRequest,
        **conflict("User already exists"),
    },
    #dependencies=[Security(bearer_scheme)],
)
async def create_user(
    interactor: FromDishka[UserCreatedHandler],
    create_data: UserCreateScheme = Body(...),
) -> UUID:
    return await interactor.handle(create_data.to_dto())


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
    },
    #dependencies=[Security(bearer_scheme)],
)
async def get_user_by_id(
    interactor: FromDishka[RetrieveUserRequestHandler],
    user_id: UUID,
) -> UserFullDTO:
    return await interactor.handle(user_id)


@router.post(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
        **locked("User is already locked"),
    },
   # dependencies=[Security(bearer_scheme)],
)
async def acquire_lock(
    interactor: FromDishka[UserLockedHandler],
    user_id: UUID,
    lock_data: ProjectScheme = Body(...),
) -> None:
    await interactor.handle(
        UserLocked(
            dto=lock_data.to_dto(),
            user_id=user_id,
        )
    )


@router.post(
    "/{user_id}/unlock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
    },
    #dependencies=[Security(bearer_scheme)],
)
async def release_lock(
    interactor: FromDishka[UserUnlockedHandler],
    user_id: UUID,
) -> None:
    await interactor.handle(user_id=user_id)

# @router.get("/my-projects", dependencies=[Security(bearer_scheme)])
# async def get_my_project() -> list[ProjectScheme]:
#     # return await service.get_projects_for_user(user_id)
#     pass