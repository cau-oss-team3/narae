from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.exceptions import AuthenticationFailedException

from app.settings import settings
from app.core.database import get_async_session

from .models import Mentor
from .schemas import STICC, Mentor_detail

# uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

router = APIRouter(prefix="/mentors", tags=["mentors"]) #TODO router 추가하기

@router.post("")
async createMentor(input_mentor_detail : Mentor_detail, )

@router.get("")
