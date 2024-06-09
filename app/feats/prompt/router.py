from fastapi import APIRouter, Depends
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from .depends import (
    get_openai_client,
)
from .models import *
from .service import *
from ..auth.models import User
from ..auth.service import get_current_user
from ..mentors.service import get_mentor2_by_id
from ...core.database import get_async_session

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/curriculum/")
def get_curriculum(request: CurriculumRequest, client: OpenAI = Depends(get_openai_client)):
    try:
        return ask_curriculum(client, request.to_dict())
    except Exception as e:
        return {"error": str(e)}


@router.post("/action-recommendation/")
async def get_action(
    request: ActionRecommendationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    client: OpenAI = Depends(get_openai_client),
):
    # 1. retrieve mentor information
    mentor = await get_mentor2_by_id(request.mentor_id, current_user, db)
    # 2. ask for action recommendation
    return ask_actions(client, mentor)

@router.post("/recommendation/")
def get_daily_action(
        existing_learning,
        learning_goal,
        abandon_reason,
        recommend_action=Depends(get_prompt_of_daily_action),
        client: OpenAI = Depends(get_openai_client),
):
    return legacy_action(abandon_reason, client, existing_learning, learning_goal, recommend_action)


@router.post("/question/")
def get_qna(
        user_question,
        study_direction=Depends(get_prompt_of_qna),
        client: OpenAI = Depends(get_openai_client),
):
    return ask_question(client, study_direction, user_question)
