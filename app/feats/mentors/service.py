from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.models import User
from app.feats.mentors.models import Mentor2
from app.feats.mentors.schemas import MentorDTO


async def get_mentor2_by_id(
        id: int,
        current_user: User,
        db: AsyncSession
):
    async with db:
        query = select(Mentor2).filter(Mentor2.id == id, Mentor2.user_id == current_user.id)

        result = await db.execute(query)
        found_mentor = result.scalar()

    if found_mentor is None:
        raise AuthenticationFailedException(
            status_code=404, message="해당 멘토 id가 없거나, 찾을 수 없음"
        )

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
        "curriculum": "" if found_mentor.curriculum is None else found_mentor.curriculum,
        "curriculum_phase": "" if found_mentor.curriculum_phase is None else found_mentor.curriculum_phase,
    }

    return MentorDTO(**mentor_detail_form)
