from fastapi import APIRouter, Depends, Query, HTTPException
from openai import OpenAI

from .depends import get_mentor_from_path_variable, get_openai_client, get_actions, get_current_action
from .schemas import *
from .service import *

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/{mentor_id}/curriculum")
async def make_curriculum(
        request: CurriculumRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: OpenAI = Depends(get_openai_client)
):
    """
    멘토의 curriculum을 생성합니다.
    """
    try:
        return ask_curriculum(client, mentor, request)
    except Exception as e:
        return {"error": str(e)}


@router.post("/{mentor_id}/action-suggestion")
async def make_action_suggestions(
        request: ActionSuggestRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: OpenAI = Depends(get_openai_client),
):
    """
    멘토의 action suggestion을 3개 생성합니다.
    """
    return ask_actions(client, mentor, request.hint)


@router.get("/{mentor_id}/daily-actions")
async def get_all_actions(
        actions=Depends(get_actions),
        completed: Optional[bool] = Query(None, description="Filter actions by completion status"),
):
    """
    모든 데일리 액션을 반환합니다.
    """
    if completed is not None:
        return [action for action in actions if action.is_active == completed]
    return await actions


@router.get("/{mentor_id}/daily-actions/current")
async def get_current_action(
        actions=Depends(get_current_action)
):
    """
    현재 진행 중인 데일리 액션을 반환합니다.
    없으면 null을 반환합니다.
    """
    return await actions


@router.post("/{mentor_id}/daily-action")
async def set_new_action(
        mentor_id: int,
        request: SetNewActionRequest,
        actions=Depends(get_current_action)
        # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 새로운 데일리 액션을 설정합니다.
    만약 현재 진행 중인 액션이 있다면 비활성화합니다.
    """

    # TODO: save new action to database(set new action as current action)

    return {"error": "Not implemented"}


@router.patch("/{mentor_id}/daily-action")
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
