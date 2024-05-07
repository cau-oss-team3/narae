from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import AuthenticationFailedException
from app.core.websocket import WebsocketConnectionManager, get_websocket_manager
from app.feats.auth.service import get_current_user
from app.feats.chat.schemas import ChatRequest, ChatResponseFail, MentorResponseSuccess


router = APIRouter(prefix="/chat", tags=["chat"])


async def get_token(
    token: Annotated[str | None, Query()] = None,
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


@router.websocket("/{mentor_id}")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    token: Annotated[str, Depends(get_token)],
    manager: WebsocketConnectionManager = Depends(get_websocket_manager),
    db: AsyncSession = Depends(get_async_session),
):
    seq = 0
    try:
        user = await get_current_user(token, db)
        if user is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION,reason="Invalid token")
    except Exception as e:
        if isinstance(e, AuthenticationFailedException):
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION,reason="Invalid token")

    await manager.connect(websocket)
    while True:
        try:
            data = await websocket.receive_text()
            print("Received data: ", data)
            chat = ChatRequest.model_validate_json(data)
            print(chat)

            await manager.send_direct_message(
                MentorResponseSuccess(seq=0, chat_data=f"Hello, {user.email}, you sent: {chat.chat_data}").model_dump_json(), websocket
            )
            seq += 1
        except ValueError as e:
            await manager.send_direct_message(ChatResponseFail(
                err = f"Invalid JSON format: {e}"
            ).model_dump_json(), websocket)
