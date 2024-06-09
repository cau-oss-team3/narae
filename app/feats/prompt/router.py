from fastapi import APIRouter, Depends
from openai import OpenAI

from app.settings import settings
from .depends import (
    get_openai_client,
)
from .const import *
from .models import CurriculumRequest
from .service import ask_curriculum, legacy_action, ask_question
from .utils import inject_variables, extract_tagged_sections


router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/curriculum/")
def get_curriculum(request: CurriculumRequest, client: OpenAI = Depends(get_openai_client)):
    try:
        return ask_curriculum(client, request.to_dict())
    except Exception as e:
        return {"error": str(e)}

@router.post("/curriculum2/")
def get_curriculum_legacy(
        existing_learning="",
        learning_goal="",
        prompt=Depends(get_prompt_of_curriculum),
        client: OpenAI = Depends(get_openai_client),
):
    """
    <학습 방향>에 대한 함수

    용어
     - Action: 오늘 당장 실행할 수 있는 Task

    다음에 해야 하는 **학습 방향**을 제시해줘야 한다.
     - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
     - 오늘 접속한 경우 띄워준다.
     - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.

    Parameters:
     - existing_learning: 이전 학습 기록
     - learning_goal: 커리큘럼과 마일스톤
    """
    return ask_curriculum(client, existing_learning, learning_goal, prompt)


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
