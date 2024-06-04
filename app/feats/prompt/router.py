from fastapi import APIRouter, Depends
from openai import OpenAI

from .depends import (
    get_openai_client,
)
from .const import (
    get_prompt_of_curriculum,
    get_prompt_of_daily_action,
    get_prompt_of_qna,
)
from .service import make_curriculum, make_action, ask_question


router = APIRouter(prefix="/prompt", tags=["prompt"])


@router.post("/curriculum/")
def get_curriculum(
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
    return make_curriculum(client, existing_learning, learning_goal, prompt)


@router.post("/recommendation/")
def get_daliy_action(
        existing_learning,
        learning_goal,
        abandon_reason,
        recommend_action=Depends(get_prompt_of_daily_action),
        client: OpenAI = Depends(get_openai_client),
):
    return make_action(abandon_reason, client, existing_learning, learning_goal, recommend_action)


@router.post("/question/")
def get_qna(
        user_question,
        study_direction=Depends(get_prompt_of_qna),
        client: OpenAI = Depends(get_openai_client),
):
    return ask_question(client, study_direction, user_question)
