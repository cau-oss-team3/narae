import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketException, status
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

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
from app.feats.chat.service import create_chatting, get_chat_history_list
from app.feats.embedding.service import retrieve_similar_documents
from app.feats.mentors.schemas import MentorDTO
from app.feats.prompt.depends import get_openai_async_client, get_mentor_from_path_variable
from app.feats.prompt.service import ask_question_async

router = APIRouter(prefix="/chat", tags=["chat"])
logger = logging.getLogger("websocket")


async def get_token(
    token: Annotated[str | None, Query()] = None,
):
    if token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return token


@router.post("/history/{mentor_id}")
async def create_chat_history(
    mentor_id: int,
    chatting: Chatting,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    chat = await create_chatting(chatting, current_user.id, mentor_id, db)
    return {"isSuccess": True, "chat": chat}


@router.get("/history/{mentor_id}")
async def get_chat_history(
    mentor_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    found_chat_history = await get_chat_history_list(current_user.id, mentor_id, db)
    return {"isSuccess": True, "chat": found_chat_history}


@router.websocket("/{mentor_id}")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    mentor_id: int,
    token: Annotated[str, Depends(get_token)],
    client: AsyncOpenAI = Depends(get_openai_async_client),
    manager: WebsocketConnectionManager = Depends(get_websocket_manager),
    db: AsyncSession = Depends(get_async_session),
):
    user = None
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

    try:
        await manager.connect(websocket)

        # get mentor info and answer
        mentor: MentorDTO = await get_mentor_from_path_variable(mentor_id, user, db)

        await manager.send_direct_message(
            MentorInfoResponse(seq=0).model_dump_json(), websocket
        )
        while True:
            try:
                # get user chat
                data = await websocket.receive_text()
                chat = ChatRequest.model_validate_json(data)

                document_excerpts = ""
                similar_documents = await retrieve_similar_documents(
                    client, db, mentor.mentor_field, chat.chat_data, 3
                )
                for idx, item in enumerate(similar_documents, 1):
                    document_excerpts += f"{idx}. [Document {idx}]\n   {item['document']}\n\n"

                # make mentor chat
                answer = (await ask_question_async(client, mentor, chat.chat_data, document_excerpts)).get(
                    "ANSWER", "죄송합니다. 다시 질문해주세요."
                )
                answer_data = MentorChatResponse(seq=0, chat_data=answer)

                # save chat history
                user_chat_history = await create_chatting(
                    chat.to_chat_history(), user.id, mentor_id, db
                )
                mentor_chat_history = await create_chatting(
                    answer_data.to_chat_history(), user.id, mentor_id, db
                )

                # send mentor chat if websocket is connected
                if manager.is_connected(websocket):
                    await manager.send_direct_message(
                        MentorChatResponse(
                            seq=mentor_chat_history.seq, chat_data=answer
                        ).model_dump_json(),
                        websocket,
                    )
            except WebSocketDisconnect:
                manager.disconnect(websocket)
                logger.info("WebSocket disconnected")
                break
            except ValueError as e:
                await manager.send_direct_message(
                    ChatResponseFail(err=f"Invalid JSON format: {e}").model_dump_json(),
                    websocket,
                )
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                await manager.send_direct_message(
                    MentorChatResponse(
                        seq=0,
                        chat_data="죄송합니다. 대답할 수 없는 질문입니다. 다르게 질문해주세요. :)",
                    ).model_dump_json(),
                    websocket,
                )
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    finally:
        manager.disconnect(websocket)