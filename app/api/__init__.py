from fastapi import APIRouter, FastAPI

from app.api.chats.handlers import router as chat_router
from app.api.srv.handlers import router as srv_router

API_V1_PREFIX = "/api/v1"

root_router = APIRouter()
root_router.include_router(srv_router)
root_router.include_router(chat_router)


def init_router(app: FastAPI) -> None:
    app.include_router(root_router)
