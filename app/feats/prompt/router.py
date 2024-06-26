import re

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from .depends import get_mentor_from_path_variable, get_openai_async_client, get_actions, get_current_action
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
        client: AsyncOpenAI = Depends(get_openai_async_client)
):
    """
    멘토의 curriculum을 생성합니다.
    """
    try:
        await save_curriculum(db, mentor, "커리큘럼이 생성 중입니다. 잠시 후 다시 시도해주세요.")  # 중복 요청 방지
        response = await ask_curriculum_async(client, mentor, request)
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
    멘토의 curriculum 반환합니다.
    """
    return {
        "CURRICULUM": mentor.curriculum,
        "PHASE": mentor.curriculum_phase
    }


@router.post("/{mentor_id}/action-suggestion")
async def make_action_suggestions(
        request: ActionSuggestRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: AsyncOpenAI = Depends(get_openai_async_client),
):
    """
    멘토의 action suggestion을 3개 생성합니다.
    """
    suggestion_result = await suggest_actions_async(client, mentor, request.hint)
    actions = []
    if "ACTIONS" in suggestion_result:
        actions_str = suggestion_result["ACTIONS"]
        actions = re.findall(r'<ACTION\d+>(.*?)</ACTION\d+>', actions_str, re.DOTALL)

    motivation = suggestion_result.get("MOTIVATION", "").strip()

    return {
        "actions": actions,
        "motivation": motivation
    }


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
    return action


@router.post("/{mentor_id}/daily-actions/current")
async def create_current_action(
        request: CreateCurrentActionRequest,
        db: AsyncSession = Depends(get_async_session),
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: AsyncOpenAI = Depends(get_openai_async_client),
):
    return await make_current_action(client, db, mentor, request.action)


@router.patch("/{mentor_id}/daily-actions/current")
async def complete_current_action_result(
        request: CompleteActionResultRequest,
        current_action=Depends(get_current_action),
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        client: AsyncOpenAI = Depends(get_openai_async_client),
        db: AsyncSession = Depends(get_async_session),
):
    """
    현재 진행 중인 데일리 액션을 완료하고 결과를 저장하고 피드백을 반환합니다.
    """
    if current_action is None or not current_action.is_active:
        raise HTTPException(status_code=404, detail="Current action not found")

    if request.success:
        return await complete_action_async(client, db, mentor, current_action, request.comment)
    else:
        return await giveup_action_async(client, db, mentor, current_action, request.comment)


@router.post("/{mentor_id}/question")
async def make_question(
        request: QuestionRequest,
        mentor: MentorDTO = Depends(get_mentor_from_path_variable),
        session: AsyncSession = Depends(get_async_session),
        client: AsyncOpenAI = Depends(get_openai_async_client),
):
    """
    질문을 받아 답변을 생성합니다.
    """
    document_excerpts = ""
    similar_documents = await retrieve_similar_documents(
        client, session, mentor.mentor_field, request.question, 3
    )
    for idx, item in enumerate(similar_documents, 1):
        document_excerpts += f"{idx}. [Document {idx}]\n   {item['document']}\n\n"

    return await ask_question_async(client, mentor, request.question, document_excerpts)
