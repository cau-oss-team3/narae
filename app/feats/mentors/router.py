from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AuthenticationFailedException
from app.settings import settings
from app.core.database import get_async_session
from app.feats.auth.router import login_user

from .models import Mentor
from .schemas import STICC, Mentor_Detail

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

router = APIRouter(prefix="/mentors", tags=["mentors"])


# access token으로 user_id 얻기
def get_user(access_token: str):
    for i in range(len(login_user)):
        if list(login_user[i].keys())[0] == access_token:
            return login_user[i].get(access_token)


# 멘토 생성
@router.post("")
async def createMentor(
    input_mentor_detail: Mentor_Detail,
    access_token: str = Header(default=None),
    db: AsyncSession = Depends(get_async_session),
):
    # TODO 3개 넘어가면 못만들게 막기 (423에러)
    # TODO creater_id none 값이면 처리..? 근데 없을수가 있나?
    creater_id = get_user(access_token)
    print(type(creater_id))
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
