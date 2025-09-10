from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import init_router
from app.api.errors.handlers import register_exception_handlers
from app.dependencies.web_app import WebAppContainer
from app.infrastructure.logging import setup_logging
from app.infrastructure.middlewares.logging_middleware import init_logging_middleware
from app.persistent.db_schemas import init_mappers


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    init_mappers()
    container: WebAppContainer = app.state.container

    if coro := container.init_resources():
        await coro

    yield

    if coro := container.shutdown_resources():
        await coro


def create_app() -> FastAPI:
    container = WebAppContainer()
    settings = container.settings()
    setup_logging(settings.logging)

    app = FastAPI(title=settings.srv.app_name, version="0.1.0", lifespan=lifespan)
    app.state.container = container
    init_middlewares(app=app)
    init_router(app)
    register_exception_handlers(app)
    init_logging_middleware(app=app)
    container.init_resources()

    return app
