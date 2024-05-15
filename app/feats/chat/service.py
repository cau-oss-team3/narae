from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.feats.chat.schemas import Chatting
from app.feats.chat.models import ChatHistory


async def create_chatting(
    chatting: Chatting,
    user_id: int,
    mentor_id: int,
    db: AsyncSession = Depends(get_async_session),
):
    # TODO 양식 검사
    # TODO candidate 리스트를 str로 반환해서 넘기는 중
    new_chat = ChatHistory(
        user_id=user_id,
        mentor_id=mentor_id,
        seq=chatting.seq,
        type=chatting.chat_type,
        chat_data=chatting.chat_data,
        visibility=chatting.visibility,
        candidates=str(chatting.candidates),
    )

    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)


async def get_chatHistoryList(
    user_id: int,
    mentor_id: int,
    db: AsyncSession = Depends(get_async_session),
) -> list[ChatHistory]:

    query = select(ChatHistory).filter(
        (user_id == ChatHistory.user_id) & (mentor_id == ChatHistory.mentor_id)
    )
    result = await db.execute(query)
    found_chatHistory = result.scalars().all()

    return found_chatHistory
