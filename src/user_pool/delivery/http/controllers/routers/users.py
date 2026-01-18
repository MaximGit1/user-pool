from uuid import UUID

from bazario.asyncio import Publisher, Sender
from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, Body, Depends
from starlette import status

from user_pool.application.commands.user_locked import UserLocked
from user_pool.application.commands.user_unlocked import UserUnlocked
from user_pool.application.common.data.dtos.users import (
    UserFullDTO,
    UserShortDTO,
)
from user_pool.application.queries.get_user_id import RetrieveNewUserIDRequest
from user_pool.application.queries.user_get_by_id import RetrieveUserRequest
from user_pool.application.queries.user_is_locked import (
    RetrieveUserIsLockedRequest,
)
from user_pool.application.queries.users_list import RetrieveUsersListRequest
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
)
async def get_users(
    sender: FromDishka[Sender],
    filters: UsersListScheme = Depends(),
) -> list[UserShortDTO]:
    """Returns a list of users"""
    return await sender.send(RetrieveUsersListRequest(*filters.to_dto()))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        **InternalServerError,
        **BadRequest,
        **conflict("User already exists"),
    },
)
async def create_user(
    sender: FromDishka[Sender],
    create_data: UserCreateScheme = Body(...),
) -> UUID:
    return await sender.send(
        RetrieveNewUserIDRequest(dto=create_data.to_dto())
    )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
    },
)
async def get_user_by_id(
    sender: FromDishka[Sender], user_id: UUID
) -> UserFullDTO:
    return await sender.send(RetrieveUserRequest(user_id=user_id))


@router.post(
    "/{user_id}/lock",
    status_code=status.HTTP_200_OK,
    responses={
        **InternalServerError,
        **not_found("User not found"),
        **locked("User is already locked"),
    },
)
async def acquire_lock(
    sender: FromDishka[Sender],
    publisher: FromDishka[Publisher],
    user_id: UUID,
    lock_data: ProjectScheme = Body(...),
) -> None:
    user_is_locked = await sender.send(
        RetrieveUserIsLockedRequest(user_id=user_id)
    )
    await publisher.publish(
        UserLocked(
            dto=lock_data.to_dto(),
            user_is_locked=user_is_locked,
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
)
async def release_lock(
    publisher: FromDishka[Publisher],
    user_id: UUID,
) -> None:
    await publisher.publish(UserUnlocked(user_id=user_id))
