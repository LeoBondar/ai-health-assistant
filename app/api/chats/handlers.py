from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Form, Path, Query

from app.api.chats.schemas import AddChatCommand, AddChatMessageResponse, AddChatResponse, GetChatsResponse
from app.api.errors.api_error import ErrorCode
from app.api.models.base import ApiResponse
from app.dependencies.web_app import WebAppContainer
from app.use_cases.chat.add_chat import AddChatUseCase
from app.use_cases.chat.add_message import AddChatMessageUseCase
from app.views.chats.get_chats import GetChatsView

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", description="Добавить чат", status_code=201)
@inject
async def add_chat(
    cmd: AddChatCommand,
    chat_add_use_case: AddChatUseCase = Depends(Provide[WebAppContainer.chat_add_use_case]),
) -> ApiResponse[AddChatResponse]:
    result = await chat_add_use_case(cmd=cmd)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.get("/", description="Получить чаты")
@inject
async def get_chats(
    limit: int = Query(10, description="Лимит"),
    offset: int = Query(0, description="Оффсет"),
    user_id: str = Query(description="Идентификатор пользователя", alias="userId", validation_alias="userId"),
    view: GetChatsView = Depends(Provide[WebAppContainer.chat_get_chats_view]),
) -> ApiResponse[GetChatsResponse]:
    result = await view(limit=limit, offset=offset, user_id=user_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")


@router.post("/{chatId}/message", description="Добавить сообщение в чат", status_code=201)
@inject
async def add_chat_message(
    text: str = Form(description="Текст сообщения", alias="text"),
    chat_id: UUID = Path(description="Идентификатор чата", alias="chatId"),
    user_id: str = Query(description="Идентификатор пользователя", alias="userId"),
    use_case: AddChatMessageUseCase = Depends(Provide[WebAppContainer.chat_add_message_use_case]),
) -> ApiResponse[AddChatMessageResponse]:
    result = await use_case(text=text, user_id=user_id, chat_id=chat_id)
    return ApiResponse(result=result, error_code=ErrorCode.SUCCESS, message="Success")
