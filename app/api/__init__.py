from fastapi import APIRouter, FastAPI

from app.api.srv.handlers import router as srv_router

API_V1_PREFIX = "/api/v1"

root_router = APIRouter()
root_router.include_router(srv_router)


def init_router(app: FastAPI) -> None:
    app.include_router(root_router)
