from fastapi import APIRouter

from user_pool.delivery.http.controllers.routers.users import (
    router as user_router,
)


def create_api_v1_router() -> APIRouter:
    router = APIRouter(
        prefix="/api/v1",
    )

    sub_routers = (user_router,)

    for sub_router in sub_routers:
        router.include_router(sub_router)

    return router
