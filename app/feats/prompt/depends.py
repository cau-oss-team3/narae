from fastapi import Depends, HTTPException
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user
from app.feats.mentors.schemas import MentorDTO
from app.feats.mentors.service import get_mentor2_by_id
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

#
# async def get_mentor_by_id(
#         mentor_id: int,
#         current_user_id: int,
#         db: AsyncSession
# ):
#     async with db:
#         query = select(Mentor2).filter(Mentor2.id == mentor_id, Mentor2.user_id == current_user_id)
#
#         result = await db.execute(query)
#         found_mentor = result.scalar()
#
#     if found_mentor is None:
#         raise AuthenticationFailedException(
#             status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
#         )
#
#     sticc_form = {
#         "situation": found_mentor.situation,
#         "task": found_mentor.task,
#         "intent": found_mentor.intent,
#         "concern": found_mentor.concern,
#         "calibrate": found_mentor.calibrate,
#     }
#     mentor_detail_form = {
#         "mentor_name": found_mentor.mentor_name,
#         "mentor_field": found_mentor.mentor_field,
#         "mentor_sticc": sticc_form,
#         "curriculum": "" if found_mentor.curriculum is None else found_mentor.curriculum,
#         "curriculum_phase": "" if found_mentor.curriculum_phase is None else found_mentor.curriculum_phase,
#     }
#
#     return MentorDTO(**mentor_detail_form)


async def get_mentor_id_from_request(request: CurriculumRequest) -> int:
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
