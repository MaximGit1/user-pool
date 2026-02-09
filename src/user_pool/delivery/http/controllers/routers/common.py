from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from user_pool.application.queries.health_checker import RetrieveHealthRequestHandler
from user_pool.delivery.http.http_response_schemes import (
    SERVICE_UNAVAILABLE,
    InternalServerError,
)

router = APIRouter(
    prefix="", tags=["Checking service status"], route_class=DishkaRoute
)


@router.get("/startup", responses={**InternalServerError})
async def startup_probe() -> dict[str, str]:
    """Determine if the application has launched successfully"""

    return {"status": "ok"}


@router.get("/health", responses={**InternalServerError})
async def liveness() -> dict[str, bool]:
    """Make sure the app isn't frozen"""

    return {"alive": True}


@router.get("/ready", responses={**InternalServerError, **SERVICE_UNAVAILABLE})
async def readiness(interactor: FromDishka[RetrieveHealthRequestHandler]) -> None:
    """Ensure the application is ready to process requests.
    Check the internal infrastructure.
    """

    await interactor.handle()
