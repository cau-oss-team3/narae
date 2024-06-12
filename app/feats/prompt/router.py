from fastapi import APIRouter

from .depends import *
from .schemas import *
from .service import *

router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/{mentor_id}/curriculum")
async def make_curriculum(
    request: CurriculumRequest,
    mentor: MentorDTO = Depends(get_mentor_from_path_variable),
    client: OpenAI = Depends(get_openai_client)
):
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
    return ask_actions(client, mentor, request.hint)


@router.get("/{mentor_id}/daily-action")
async def get_current_action(
    mentor: MentorDTO = Depends(get_mentor_from_path_variable)
):
    return mentor


@router.post("/{mentor_id}/daily-action")
async def set_new_action(
    mentor_id: int,
    request: SetNewActionRequest,
    # current_user: User = Depends(get_current_user),
    # db: AsyncSession = Depends(get_async_session),
    # client: OpenAI = Depends(get_openai_client),
):
    """
    현재 진행 중인 새로 설정합니다.
    """
    # TODO: check if mentor has current action
    # TODO: check if daily action is valid using openai
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
