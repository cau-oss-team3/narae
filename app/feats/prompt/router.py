from fastapi import APIRouter, Depends
from openai import OpenAI

from settings import settings
from .depends import (
    get_openai_client,
    get_prompt_of_curriculum,
    get_prompt_of_daily_action,
    get_prompt_of_qna,
)


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
    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the today's study direction and next short-term goal to the user. Your message is given to the user just before the study starts."
                + "Make sure your advice is specific enough to be actionable and at the right level of difficulty."
                + "Also, make sure to motivate the user to keep going."
                + f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease provide detailed guidance for the next steps in learning, taking into account the current knowledge and the desired learning outcome."
                + "please say it in Korean. Thank you.",
            },
            {
                "role": "assistant",
                "content": existing_learning,
            },
            {
                "role": "assistant",
                "content": learning_goal,
            },
            {
                "role": "user",
                "content": prompt.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    return response.choices[0].message.content


@router.post("/recommendation/")
def get_daliy_action(
    existing_learning,
    learning_goal,
    abandon_reason,
    recommend_action=Depends(get_prompt_of_daily_action),
    client: OpenAI = Depends(get_openai_client),
):
    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the next action which depends to the today's study direction. Your message is given to the user after the's study direction is given. Make sure your advice is specific enough to be actionable and at the right level of difficulty."
                + "Also, make sure to motivate the user to keep going."
                + "If the user completes the action, please provide feedback on how they completed it."
                + "If the user abandons the action, ask for the reason and suggest the next recommended action based on the reason."
                + f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease recommend an action that can be done according to today's learning direction.",
            },
            {
                "role": "assistant",
                "content": existing_learning,
            },
            {
                "role": "assistant",
                "content": learning_goal,
            },
            {
                "role": "user",
                "content": recommend_action.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )

    # 사용자가 액션을 완료할 시 이에 대한 응답
    response_text = response.choices[0].message.content.strip()
    if "completed" in response_text.lower():
        feedback_prompt = "Please provide feedback on how you completed the action."
        response_with_feedback = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": feedback_prompt,
                },
                {
                    "role": "user",
                    "content": response_text,
                },
            ],
            temperature=0.5,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text += (
            "\n\nFeedback: " + response_with_feedback.choices[0].message.content.strip()
        )

    # 사용자가 액션을 포기할 시 이에 대한 응답
    elif "abandoned" in response_text.lower():
        reason_prompt = "Please specify the reason for abandoning the action."
        next_action_prompt = "Based on your reason for abandoning the action, here's the next recommended action."

        reason_response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": reason_prompt,
                },
                {
                    "role": "user",
                    "content": abandon_reason,
                },
            ],
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        next_action_response = client.chat.completions.create(
            model=settings.gpt_model,
            messages=[
                {
                    "role": "system",
                    "content": next_action_prompt,
                },
                {
                    "role": "user",
                    "content": reason_response.choices[0].message.content.strip(),
                },
            ],
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        response_text += (
            f"\n\nReason for abandoning: {reason_response.choices[0].message.content.strip()}"
            f"\n\nNext recommended action: {next_action_response.choices[0].message.content.strip()}"
        )

    return response_text


@router.post("/qna/")
def get_qna(
    user_question,
    study_direction=Depends(get_prompt_of_qna),
    client: OpenAI = Depends(get_openai_client),
):
    response = client.chat.completions.create(
        model=settings.gpt_model,
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who gives answer to the question which the user gives. Please provide an answer to the user's question about your areas of interest.",
            },
            {
                "role": "user",
                "content": user_question,
            },
            {
                "role": "user",
                "content": study_direction.replace("\n", " "),
            },
        ],
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content.strip()
