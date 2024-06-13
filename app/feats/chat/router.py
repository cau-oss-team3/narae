from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketException, status
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.exceptions import AuthenticationFailedException
from app.core.websocket import WebsocketConnectionManager, get_websocket_manager
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user
from app.feats.chat.schemas import (
    ChatRequest,
    ChatResponseFail,
    MentorChatResponse,
    MentorInfoResponse,
)
from app.feats.chat.schemas import Chatting
from app.feats.chat.service import create_chatting, get_chatHistoryList
from app.feats.mentors.schemas import MentorDTO
from app.feats.mentors.service import get_mentor2_by_id
from app.feats.prompt.depends import get_openai_client
from app.feats.prompt.service import ask_question

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
    mentor_id: int,
    token: Annotated[str, Depends(get_token)],
    client: OpenAI = Depends(get_openai_client),
    manager: WebsocketConnectionManager = Depends(get_websocket_manager),
    db: AsyncSession = Depends(get_async_session),
):
    seq = 0
    try:
        user = await get_current_user(token, db)
        if user is None:
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token"
            )
    except Exception as e:
        if isinstance(e, AuthenticationFailedException):
            raise WebSocketException(
                code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token"
            )

    await manager.connect(websocket)

    # get mentor info and answer
    mentor: MentorDTO = await get_mentor2_by_id(mentor_id, user, db)
    # direction: str = format_direction_for_study(mentor.mentor_field)
    # answer = get_study_direction(direction, client).choices[0].message.content.strip()

    await manager.send_direct_message(
        MentorInfoResponse(seq=0).model_dump_json(), websocket
    )
    seq += 1

    while True:
        try:
            data = await websocket.receive_text()
            chat = ChatRequest.model_validate_json(data)
            answer = ask_question(chat.chat_data, mentor, client)
            await manager.send_direct_message(
                MentorChatResponse(seq=0, chat_data=answer).model_dump_json(), websocket
            )
            seq += 1
        except ValueError as e:
            await manager.send_direct_message(
                ChatResponseFail(err=f"Invalid JSON format: {e}").model_dump_json(),
                websocket,
            )


@router.post("/chathistory/{mentor_id}")
async def createChatHistory(
    mentor_id: int,
    chatting: Chatting,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    await create_chatting(chatting, current_user.id, mentor_id, db)

    return {"isSuccess": True}


@router.get("/chathistory/{mentor_id}")
async def getChatHistory(
    mentor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):

    found_chathistory = await get_chatHistoryList(current_user.id, mentor_id, db)

    return {"isSuccess": True, "chathistory": found_chathistory}
