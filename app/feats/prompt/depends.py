from fastapi import Depends, HTTPException
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user
from app.feats.mentors.schemas import MentorDTO
from app.feats.mentors.service import get_mentor2_by_id, retrieve_all_actions, retrieve_current_action
from app.feats.prompt.schemas import CurriculumRequest
from app.settings import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.gpt_key)


def get_embedding(text, client: OpenAI = Depends(settings.gpt_model)):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=settings.gpt_embedding_model)
        .data[0]
        .embedding
    )


"""
mentors
"""


async def get_mentor_id_from_request(request) -> int:
    return request.mentor_id


async def get_mentor_from_request(
        request: CurriculumRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
) -> MentorDTO:
    mentor = await get_mentor2_by_id(request.mentor_id, current_user, db)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor


async def get_mentor_from_path_variable(
        mentor_id: int,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_async_session),
) -> MentorDTO:
    mentor = await get_mentor2_by_id(mentor_id, current_user, db)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return mentor


"""
actions
"""


async def get_actions(
        mentor_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    return retrieve_all_actions(mentor_id, db)


async def get_current_action(
        mentor_id: int,
        db: AsyncSession = Depends(get_async_session),
):
    return retrieve_current_action(mentor_id, db)
