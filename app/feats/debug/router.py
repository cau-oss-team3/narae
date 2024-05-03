from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AuthenticationFailedException
from app.core.database import get_async_session

router = APIRouter(prefix="/debug", tags=["debug"])


# daily-action list 가져오기
@router.get("/daily-actions")
async def getDailyActionList():
    # TODO daily action 리스트 받아오기
    daily_action_list = [
        {"id": "string", "daily-action": "string"},
        {"id": "string", "daily-action": "string"},
    ]

    return {"isSuccess": True, "daily-actions": daily_action_list}


# daily0action 가져오기
@router.get("/daily-actions/{id}")
async def getDailyActionList(id: str, db: AsyncSession = Depends(get_async_session)):

    # # TODO 해당 멘토의 daily action 받아오기(Table name 넣기)
    # async with db:
    #     query = select(Table_name).filter(id == Table_name.mentor_name)
    #     result = await db.execute(query)
    #     daily_action = result.scalar()

    # # 해당 멘토의 daily_action이 존재하지 않을 때 예외처리
    # if daily_action is None:
    #     raise AuthenticationFailedException(
    #         status_code=404, message="해당 멘토 id를 찾을 수 없거나 존재하지 않음"
    #     )

    # TODO daily acton 값 넣기
    return {"isSuccess": True, "daily-action": "daily action text"}


# chat-history 가져오기
@router.get("/chat-history/{id}")
async def getChatHistory(id: str, db: AsyncSession = Depends(get_async_session)):

    # # TODO 해당 id의 기존 대화 요약 가져오기 (TableName이랑 col 명 바꾸기)
    # async with db:
    #     query = select(TableName).filter(id == TableName.mentor_id)
    #     result = await db.execute(query)
    #     chat_history = result.scalar()

    # # 해당 멘토의 chat_history가 존재하지 않을 때 예외처리
    # if chat_history is None:
    #     raise AuthenticationFailedException(
    #         status_code=404, message="해당 멘토 id를 찾을 수 없거나 존재하지 않음"
    #     )

    # TODO return 값 변경하기(양식만 가져옴)
    return {"isSuccess": True, "id": id, "summary": "string"}
