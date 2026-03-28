from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from user_pool.delivery.http.controllers.main_router import create_main_router
from user_pool.setup.components.app import init_app
from user_pool.setup.components.di.main import container_factory
from user_pool.setup.components.logger import init_logger
from user_pool.setup.config import (
    Config,
    create_config,
)


def init_di(config: Config, app_: FastAPI) -> AsyncContainer:
    container = container_factory(config)
    setup_dishka(container, app_)

    return container


def create_entry_point() -> FastAPI:
    config = create_config()
    logger = init_logger(config=config.logging)
    app = init_app(
        config=config.asgi, routers=[create_main_router()], logger=logger
    )
    _ = init_di(config=config, app_=app)

    return app


if __name__ == "__main__":  # for local launch
    import uvicorn

    uvicorn.run(create_entry_point())
