from fastapi import APIRouter, Depends, Query, HTTPException
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from .depends import get_mentor_from_path_variable, get_openai_client, get_actions, get_current_action
from .schemas import *
from .service import *
from ..mentors.schemas import ActionStatus
from ...core.database import get_async_session

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/{mentor_id}/curriculum")
async def make_curriculum(
        request: CurriculumRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        db: AsyncSession = Depends(get_async_session),
        client: OpenAI = Depends(get_openai_client)
):
    """
    멘토의 curriculum을 생성합니다.
    """
    try:
        response = ask_curriculum(client, mentor, request)
        curriculum = response.get("CURRICULUM", "")
        await save_curriculum(db, mentor, curriculum)

        return response
    except Exception as e:
        return {"error": str(e)}

@router.get("/{mentor_id}/curriculum")
async def get_curriculum(
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
):
    """
    멘토의 curriculum을 반환합니다.
    """
    return {
        "CURRICULUM": mentor.curriculum,
        "PHASE": mentor.curriculum_phase
    }


@router.post("/{mentor_id}/action-suggestion")
async def make_action_suggestions(
        request: ActionSuggestRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: OpenAI = Depends(get_openai_client),
):
    """
    멘토의 action suggestion을 3개 생성합니다.
    """
    return suggest_actions(client, mentor, request.hint)


@router.get("/{mentor_id}/daily-actions")
async def get_all_actions(
        actions=Depends(get_actions),
        action_status: ActionStatus = Query(ActionStatus.all, description="completed status")
):
    """
    모든 데일리 액션을 반환합니다.
    """
    actions = await actions
    if action_status == ActionStatus.done:
        filtered_actions = [action for action in actions if not action.is_active]
    elif action_status == ActionStatus.current:
        filtered_actions = [action for action in actions if action.is_active]
    else:
        filtered_actions = actions

    return filtered_actions


@router.get("/{mentor_id}/daily-actions/current")
async def get_current_action(
        action=Depends(get_current_action)
):
    """
    현재 진행 중인 데일리 액션을 반환합니다.
    없으면 null을 반환합니다.
    """
    return await action


@router.post("/{mentor_id}/daily-actions/current")
async def create_current_action(
        request: CreateCurrentActionRequest,
        db: AsyncSession = Depends(get_async_session),
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: OpenAI = Depends(get_openai_client),
):
    return await make_current_action(client, db, mentor, request.action)


@router.patch("/{mentor_id}/daily-action/current")
async def complete_current_action_result(
        mentor_id: int,
        request: CompleteActionResultRequest,
        # current_user: User = Depends(get_current_user),
        # db: AsyncSession = Depends(get_async_session),
        # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 데일리 액션을 완료하고 결과를 저장하고 피드백을 반환합니다.
    """
    # TODO: check if mentor has current action
    # TODO: save action result to database
    # TODO: get feedback from openai and return
    return {"error": "Not implemented"}


@router.patch("/{mentor_id}/daily-action/current")
async def giveup_current_action_result(
        mentor_id: int,
        request: CompleteActionResultRequest,
        # current_user: User = Depends(get_current_user),
        # db: AsyncSession = Depends(get_async_session),
        # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 데일리 액션을 완료하고 결과를 저장하고 피드백을 반환합니다.
    """
    # TODO: check if mentor has current action
    # TODO: save action result to database
    # TODO: get feedback from openai and return
    return {"error": "Not implemented"}


@router.post("/{mentor_id}/question")
async def make_question(
        request: QuestionRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: OpenAI = Depends(get_openai_client),
):
    """
    질문을 받아 답변을 생성합니다.
    """
    return ask_question(client, mentor, request.question)
