from fastapi import APIRouter
from starlette.responses import RedirectResponse

from user_pool.delivery.http.controllers.api_v1_router import (
    create_api_v1_router,
)
from user_pool.delivery.http.controllers.routers.common import (
    router as check_router,
)


def create_main_router() -> APIRouter:
    router = APIRouter(
        prefix="",
    )

    @router.get("/", tags=["General"])
    async def redirect_to_docs() -> RedirectResponse:
        """Redirects to Swagger documentation"""
        return RedirectResponse(url="docs/")

    sub_routers = (
        check_router,
        create_api_v1_router(),
    )

    for sub_router in sub_routers:
        router.include_router(sub_router)

    return router
