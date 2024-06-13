from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.models import User
from app.feats.mentors.models import Mentor2, Action
from app.feats.mentors.schemas import MentorDTO


async def get_mentor2_by_id(
        mentor_id: int,
        current_user: User,
        db: AsyncSession
):
    async with db:
        query = select(Mentor2).filter(Mentor2.id == mentor_id, Mentor2.user_id == current_user.id)

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
        "mentor_id": found_mentor.id,
        "mentor_name": found_mentor.mentor_name,
        "mentor_field": found_mentor.mentor_field,
        "mentor_sticc": sticc_form,
        "curriculum": "" if found_mentor.curriculum is None else found_mentor.curriculum,
        "curriculum_phase": "" if found_mentor.curriculum_phase is None else found_mentor.curriculum_phase,
    }

    return MentorDTO(**mentor_detail_form)


async def retrieve_all_actions(
        mentor_id: int,
        db: AsyncSession
):
    async with db:
        query = select(Action).filter(Action.mentor_id == mentor_id)
        result = await db.execute(query)
        actions = result.scalars().all()
        actions = [action for action in actions]

    if not actions:
        return []

    return actions


async def retrieve_completed_actions(
        mentor_id: int,
        db: AsyncSession,
):
    async with db:
        query = select(Action).filter(Action.mentor_id == mentor_id, Action.is_active == False)
        result = await db.execute(query)
        actions = result.scalars().all()
        actions = [action for action in actions]

    if not actions:
        return []

    return actions


async def retrieve_current_action(
        mentor_id: int,
        db: AsyncSession,
):
    async with db:
        query = select(Action).filter(Action.mentor_id == mentor_id, Action.is_active == True)
        result = await db.execute(query)
        current_action = result.scalar()

    if current_action is None:
        return None

    return current_action


async def set_new_action(
        mentor_id: int,
        db: AsyncSession,
        action: str,
):
    async with db:
        query = select(Action).filter(Action.mentor_id == mentor_id, Action.is_active == True)
        result = await db.execute(query)
        current_action = result.scalar()

        if current_action is not None:
            current_action.is_active = False
            current_action.result = "다른 액션을 진행하기 위해 비활성화됐습니다."
            db.add(current_action)

        new_action = Action(mentor_id=mentor_id, action=action, is_active=True)
        db.add(new_action)
        await db.commit()
        await db.refresh(new_action)

    return new_action

async def complete_current_action_result(
        mentor_id: int,
        db: AsyncSession,
        result: str,
):
    async with db:
        query = select(Action).filter(Action.mentor_id == mentor_id, Action.is_active == True)
        result = await db.execute(query)
        current_action = result.scalar()

        if current_action is None:
            return None

        current_action.is_active = False
        current_action.result = result
        db.add(current_action)
        await db.commit()
        await db.refresh(current_action)

    return current_action