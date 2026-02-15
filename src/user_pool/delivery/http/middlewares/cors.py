from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from user_pool.setup.config import ASGIConfig


def setup_cors_middleware(app_: FastAPI, config: ASGIConfig) -> None:
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f"https://localhost:{config.port}",
            f"https://{config.host}:{config.port}",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
