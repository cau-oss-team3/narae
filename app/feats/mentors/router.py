from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.core.exceptions import AuthenticationFailedException
from app.core.database import get_async_session
from app.feats.auth.router import active_user

from .models import Mentor
from .schemas import MentorDTO

router = APIRouter(prefix="/mentors", tags=["mentors"])


# token으로 user_id 얻기
def get_user(token):
    for i in range(len(active_user)):
        if list(active_user[i].keys())[0] == token:
            return active_user[i].get(token)


# 멘토 생성
@router.post("")
async def createMentor(
    input_mentor_detail: MentorDTO,
    token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    creater_id = get_user(token)

    async with db:
        query = select(Mentor).filter(creater_id == Mentor.user_id)
        result = await db.execute(query)
        found_mentor = result.scalars().all()

    if len(found_mentor) >= 3:
        raise AuthenticationFailedException(
            status_code=423, message="멘토 최대 생성 제한 도달"
        )

    mentor_id = str(creater_id) + input_mentor_detail.mentor_name

    new_mentor = Mentor(
        id=mentor_id,
        mentor_name=input_mentor_detail.mentor_name,
        mentor_field=input_mentor_detail.mentor_field,
        user_id=creater_id,
        situation=input_mentor_detail.mentor_sticc.situation,
        task=input_mentor_detail.mentor_sticc.task,
        intent=input_mentor_detail.mentor_sticc.intent,
        concern=input_mentor_detail.mentor_sticc.concern,
        calibrate=input_mentor_detail.mentor_sticc.calibrate,
    )

    async with db:
        db.add(new_mentor)
        await db.commit()
        await db.refresh(new_mentor)

    return {"isSuccess": True, "id": mentor_id}


# 멘토 리스트 얻기 - getMentorList
@router.get("")
async def getMentorList(
    token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    creater_id = get_user(token)
    async with db:
        query = select(Mentor).filter(creater_id == Mentor.user_id)
        result = await db.execute(query)
        found_mentor = result.scalars().all()

    return_mentor = []

    for i in range(len(found_mentor)):
        # TODO 후에 daily-action 값 가져오기
        return_mentor.append(
            {
                "id": found_mentor[i].id,
                "name": found_mentor[i].mentor_name,
                "daily_action": "today's daily action",
            }
        )

    return {"isSuccess": True, "mentors": return_mentor}


# 멘토 얻기 - getMentor
@router.get("/{id}")
async def getMentor(
    id: str,
    token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor).filter(id == Mentor.id)
        result = await db.execute(query)
        found_mentor = result.scalar()

    if found_mentor is None:
        raise AuthenticationFailedException(
            status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
        )

    # Mentor_Detail 객체로 만들어주기
    sticc_form = {
        "situation": found_mentor.situation,
        "task": found_mentor.task,
        "intent": found_mentor.intent,
        "concern": found_mentor.concern,
        "calibrate": found_mentor.calibrate,
    }
    mentor_detail_form = {
        "mentor_name": found_mentor.mentor_name,
        "mentor_field": found_mentor.mentor_field,
        "mentor_sticc": sticc_form,
    }
    found_mentor_detail = MentorDTO(**mentor_detail_form)

    # TODO chat data array 반환해주기
    return {
        "isSuccess": True,
        "id": id,
        "mentor_detail": found_mentor_detail,
        "chat_history": "chat-data array가 들어가는 부분",
    }


@router.put("/{id}")
async def updateMentor(
    id: str,
    input_mentor_detail: MentorDTO,
    token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor).filter(id == Mentor.id)
        result = await db.execute(query)
        found_mentor = result.scalar()

    if found_mentor is None:
        raise AuthenticationFailedException(
            status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
        )

    # input이 비어있지 않으면 db 내용을 바꿔줌
    if input_mentor_detail.mentor_name != "":
        found_mentor.mentor_name = input_mentor_detail.mentor_name
    if input_mentor_detail.mentor_field != "":
        found_mentor.mentor_field = input_mentor_detail.mentor_field
    if input_mentor_detail.mentor_sticc.situation != "":
        found_mentor.situation = input_mentor_detail.mentor_sticc.situation
    if input_mentor_detail.mentor_sticc.task != "":
        found_mentor.task = input_mentor_detail.mentor_sticc.task
    if input_mentor_detail.mentor_sticc.intent != "":
        found_mentor.intent = input_mentor_detail.mentor_sticc.intent
    if input_mentor_detail.mentor_sticc.concern != "":
        found_mentor.concern = input_mentor_detail.mentor_sticc.concern
    if input_mentor_detail.mentor_sticc.calibrate != "":
        found_mentor.calibrate = input_mentor_detail.mentor_sticc.calibrate

    async with db:
        query = (
            update(Mentor)
            .where(Mentor.id == found_mentor.id)
            .values(
                mentor_name=found_mentor.mentor_name,
                mentor_field=found_mentor.mentor_field,
                situation=found_mentor.situation,
                task=found_mentor.task,
                intent=found_mentor.intent,
                concern=found_mentor.concern,
                calibrate=found_mentor.calibrate,
            )
        )
        result = await db.execute(query)
        await db.commit()

    return {"isSuccess": True, "id": id}


@router.delete("/{id}")
async def deleteMentor(
    id: str,
    token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor).filter(id == Mentor.id)
        result = await db.execute(query)
        mentor_to_delete = result.scalar()

    if mentor_to_delete is None:
        raise AuthenticationFailedException(
            status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
        )

    async with db:
        query = delete(Mentor).where(Mentor.id == id)
        await db.execute(query)
        await db.commit()

    return {"isSuccess": True}
