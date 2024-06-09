from fastapi import APIRouter, Depends
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from .depends import (
    get_openai_client,
)
from .schemas import CurriculumRequest, ActionSuggestionRequest, QuestionRequest
from .service import *
from ..auth.models import User
from ..auth.service import get_current_user
from ..mentors.service import get_mentor2_by_id
from ...core.database import get_async_session

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/curriculum/")
async def make_curriculum(request: CurriculumRequest, client: OpenAI = Depends(get_openai_client)):
    try:
        return ask_curriculum(client, request.to_dict())
    except Exception as e:
        return {"error": str(e)}


@router.post("/action-suggestion/")
async def make_action_suggestions(
    request: ActionSuggestionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    client: OpenAI = Depends(get_openai_client),
):
    """
    데일리 액션 추천을 3가지 받아옵니다.
    """
    # 1. retrieve mentor information
    mentor = await get_mentor2_by_id(request.mentor_id, current_user, db)
    # 2. ask for action recommendation
    return ask_actions(client, mentor)


@router.get("/daily-action/")
async def get_current_action(
    # request: CurrentActionRequest,
    # current_user: User = Depends(get_current_user),
    # db: AsyncSession = Depends(get_async_session),
    # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 데일리 액션을 받아옵니다.
    """
    return {"error": "Not implemented"}


@router.post("/daily-action/")
async def set_new_action(
    # request: SetNewActionRequest,
    # current_user: User = Depends(get_current_user),
    # db: AsyncSession = Depends(get_async_session),
    # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 새로 설정합니다.
    """
    return {"error": "Not implemented"}


@router.patch("/daily-action/")
async def complete_current_action_result(
    # request: completeActionResultRequest,
    # current_user: User = Depends(get_current_user),
    # db: AsyncSession = Depends(get_async_session),
    # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 데일리 액션을 완료하고 결과를 저장하고 피드백을 반환합니다.
    """
    return {"error": "Not implemented"}


@router.post("/question/")
async def make_question(
    request: QuestionRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
    client: OpenAI = Depends(get_openai_client),
):
    """
    질문을 받아 답변을 생성합니다.
    """
    mentor = await get_mentor2_by_id(request.mentor_id, current_user, db)
    return ask_question(client, mentor, request.question)
