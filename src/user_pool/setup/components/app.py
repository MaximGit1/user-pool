from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from logging import Logger

from asgi_monitor.integrations.fastapi import (
    MetricsConfig,
    TracingConfig,
    setup_metrics,
    setup_tracing,
)
from dishka import AsyncContainer
from fastapi import APIRouter, FastAPI
from fastapi.responses import ORJSONResponse
from grpc.aio import Channel

from user_pool.delivery.http.exception_handler import init_exception_handlers
from user_pool.delivery.http.middlewares.cors import setup_cors_middleware
from user_pool.setup.config import ASGIConfig


def init_app(
    config: ASGIConfig, routers: list[APIRouter], logger: Logger
) -> FastAPI:
    app = FastAPI(
        version="1.1.0",
        title="User pool platform",
        summary="bot farm",
        debug=config.debug,
        lifespan=make_lifespan(logger=logger),
        default_response_class=ORJSONResponse,
    )

    for router in routers:
        app.include_router(router)

    logger.debug("routers are included")

    init_middlewares(app, config=config)
    logger.debug("middlewares are included")

    init_exception_handlers(app)
    logger.debug("exception handler are added")

    init_metrics(app)
    init_tracing(app)
    logger.debug("metrics handler are added")

    return app


def make_lifespan(logger: Logger):
    @asynccontextmanager
    async def lifespan(app_: FastAPI) -> AsyncGenerator[None]:
        logger.info("Application is starting...")

        yield

        logger.info("Application is stopping...")

        container: AsyncContainer = app_.state.dishka_container

        await (await container.get(Channel)).close()

        await container.close()

        logger.info("Application completed correctly")


def init_middlewares(app_: FastAPI, config: ASGIConfig) -> None:
    setup_cors_middleware(app_, config)


def init_metrics(app_: FastAPI) -> None:
    setup_metrics(
        app_,
        MetricsConfig(
            app_name="user_pool",
            include_trace_exemplar=False,
            include_metrics_endpoint=True,
        ),
    )


def init_tracing(app_: FastAPI) -> None:
    setup_tracing(app_, TracingConfig())
