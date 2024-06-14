from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.feats.chat.models import ChatHistory
from app.feats.chat.schemas import Chatting


async def create_chatting(
    chatting: Chatting,
    user_id: int,
    mentor_id: int,
    db: AsyncSession,
):
    new_chat = ChatHistory(
        user_id=user_id,
        mentor_id=mentor_id,
        type=chatting.chat_type,
        chat_data=chatting.chat_data,
        visibility=chatting.visibility,
        timestamp=chatting.timestamp,
    )

    db.add(new_chat)
    await db.flush()
    await db.commit()
    await db.refresh(new_chat)

    new_chat.seq = new_chat.id
    return new_chat


async def get_chat_history_list(
    user_id: int,
    mentor_id: int,
    db: AsyncSession,
) -> Sequence[ChatHistory]:

    query = select(ChatHistory).filter(
        (user_id == ChatHistory.user_id) & (mentor_id == ChatHistory.mentor_id)
    ).order_by(ChatHistory.id)

    result = await db.execute(query)
    found_chatHistory = result.scalars().all()
    found_chatHistory = list(found_chatHistory)
    for elem in found_chatHistory:
        elem.seq = elem.id
        del elem.id

    return [chatHistory for chatHistory in found_chatHistory]
