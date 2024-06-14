from fastapi import APIRouter, Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.database import get_async_session
from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user
from .models import Mentor2
from .schemas import MentorDTO, CreateMentorDTO
from .service import retrieve_current_action

router = APIRouter(prefix="/mentors2", tags=["mentors2"])


# 멘토 생성
@router.post("")
async def create_mentor(
        input_mentor_detail: CreateMentorDTO,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    creator_id = current_user.id

    async with db:
        query = select(Mentor2).filter(creator_id == Mentor2.user_id)
        result = await db.execute(query)
        found_mentor = result.scalars().all()

    if len(found_mentor) >= 3:
        raise AuthenticationFailedException(
            status_code=423, message="멘토 최대 생성 제한 도달"
        )

    new_mentor = Mentor2(
        mentor_name=input_mentor_detail.mentor_name,
        mentor_field=input_mentor_detail.mentor_field,
        user_id=creator_id,
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

    return {"isSuccess": True, "id": new_mentor.id}


# 멘토 리스트 얻기 - getMentorList
@router.get("")
async def get_mentor_list(
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    creator_id = current_user.id
    async with db:
        query = select(Mentor2).filter(creator_id == Mentor2.user_id)
        result = await db.execute(query)
        found_mentor = result.scalars().all()

    return_mentor = []

    for i in range(len(found_mentor)):
        daily_action = await retrieve_current_action(db, found_mentor[i].id)
        return_mentor.append(
            {
                "id": found_mentor[i].id,
                "name": found_mentor[i].mentor_name,
                "daily_action": daily_action
            }
        )

    return {"isSuccess": True, "mentors": return_mentor}


# 멘토 얻기 - getMentor
@router.get("/{id}")
async def get_mentor(
        id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor2).filter(Mentor2.id == id, Mentor2.user_id == current_user.id)

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
        "mentor_id": found_mentor.id,
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
        "chat_history": ["기존의 채팅 데이터 불러오기는 아직 지원되지 않습니다. 미래에 지원될 예정입니다. :)"],
    }


@router.put("/{id}")
async def update_mentor(
        id: int,
        input_mentor_detail: MentorDTO,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor2).filter(id == Mentor2.id, Mentor2.user_id == current_user.id)
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
            update(Mentor2)
            .where(Mentor2.id == found_mentor.id)
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
async def delete_mentor(
        id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
):
    async with db:
        query = select(Mentor2).options(joinedload(Mentor2.chat_histories)).filter(
            Mentor2.id == id,
            Mentor2.user_id == current_user.id
        )
        result = await db.execute(query)
        mentor_to_delete = result.scalar()

    if mentor_to_delete is None:
        raise AuthenticationFailedException(
            status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
        )

    async with db:
        await db.delete(mentor_to_delete)
        await db.commit()

    return {"isSuccess": True}
