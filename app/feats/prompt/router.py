from fastapi import APIRouter, Depends
from openai import OpenAI

from .depends import (
    get_answer_for_question,
    get_direction_for_study,
    get_recommend_action,
    get_openai_client,
)

"""
Action: 오늘 당장 실행할 수 있는 Task
커리큘럼: 사용자의 장기적인 학습 행동 방침 - 장기간의 거대한 목표, 체계적인 지식 습득 위함, 향후 참조할 대량의 자료, 마일스톤
학습방향: 사용자의 단기적인 학습 행동 방침 - 단기간의 일시적 목표, 자신의 능력 향상을 위함, 지금 참조할 소량의 자료, 플래그

시스템 프롬프트의 의도 [평가표] <- 만점이 나오도록 프롬프트 엔지니어링을 해야 함 (별도의 프롬프트로 분리)
기본 전제: (포기하지 않도록 동기 부여를 해줘야 한다.)

1. 다음에 해야 하는 ***학습 방향***을 제시해줘야 한다.
   - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
   - 오늘 접속한 경우 띄워준다.
   - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.
2. 오늘 학습 방향에 따라 실천 가능한 ***액션을*** 추천한다.
   - 이때 실천 가능할만큼 구체적이고 적절한 난이도의 조언을 해야 한다.
   - 내가 처음인지/어디까지 해봤는지 알아야 한다.
   - 액션을 어떻게 완수했는지 알릴 수 있어야 한다. 액션 완수 내용을 말하면 피드백 해줘야 한다.
   - 액션 포기가 가능해야 한다. 포기하는 경우 이유를 말해고 다음 액션을 추천해준다.(+서버에 저장)
3. 나의 관심분야에 대한 질문에 ***답***을 해줘야 한다.
   - 기본적인 채팅의 형태로 이루어진다.
   - 임베딩이 사용할 수 있으면 좋다.
"""


router = APIRouter(prefix="/prompt", tags=["prompt"])

OPENAI_MODEL = "gpt-3.5-turbo-1106"
# @router.post(
#     "/test/",
#     description="Narae service which uses openai model",
#     response_model=GPTResponse,
# )
# async def gpt_narae(request: GPTRequest, client: OpenAI = Depends(get_openai_client)):
#     response = service.get_coaching_info_from_gpt(client, request.sticc)
#     return GPTResponse(response)


@router.post("/direction/")
def get_study_direction(
    existing_learning,
    learning_goal,
    study_direction=Depends(get_direction_for_study),
    client: OpenAI = Depends(get_openai_client),
):
    """
    1에 대한 함수(existing_learning: 이전 학습 기록, learning_goal: 커리큘럼과 마일스톤)
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the today's study direction and next short-term goal to the user. Your message is given to the user just before the study starts." + \
                           "Make sure your advice is specific enough to be actionable and at the right level of difficulty." + \
                           "Also, make sure to motivate the user to keep going." + \
                           f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease provide detailed guidance for the next steps in learning, taking into account the current knowledge and the desired learning outcome."
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
                "content": study_direction.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    return response.choices[0].message.content


# 2에 대한 함수(existing_learning: 이전 학습 기록, learning_goal: 커리큘럼과 마일스톤)
@router.post("/recommendation/")
def get_recommended_action(
    existing_learning,
    learning_goal,
    abandon_reason,
    recommend_action = Depends(get_recommend_action),
    client: OpenAI = Depends(get_openai_client),
):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the next action which depends to the today's study direction. Your message is given to the user after the's study direction is given. Make sure your advice is specific enough to be actionable and at the right level of difficulty." + \
                           "Also, make sure to motivate the user to keep going." + \
                           "If the user completes the action, please provide feedback on how they completed it." + \
                           "If the user abandons the action, ask for the reason and suggest the next recommended action based on the reason." + \
                           f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease recommend an action that can be done according to today's learning direction."
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
            model=OPENAI_MODEL,
            messages=[
                  {
                     "role": "system",
                     "content": feedback_prompt,
                  },
                  {
                     "role": "user",
                     "content": response_text,
                  }
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
            model=OPENAI_MODEL,
            messages=[
                {
                     "role": "system",
                     "content": reason_prompt,
                },
                {
                    "role": "user",
                    "content": abandon_reason,
                }
            ],
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        next_action_response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                  {
                     "role": "system",
                     "content": next_action_prompt,
                  },
                  {
                     "role": "user",
                     "content": reason_response.choices[0].message.content.strip(),
                  }
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


# 3에 대한 함수
@router.post("/question/")
def get_answer_question(
    user_question,
    study_direction=Depends(get_answer_for_question),
    client: OpenAI = Depends(get_openai_client),
):
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
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


"""
# @router.post("/test-gpt/")
def test_gpt(sticc: UserSituationRequest, client: OpenAI = Depends(get_openai_client)):
   userInput = format_sticc_for_coaching(sticc)

   response = client.chat.completions.create(
      model=OPENAI_MODEL,
      ## TODO: 만들어야 하는 것: 주어진 시나리오가 가능하도록 하게 함
      ## TODO: tempeture 등 정보의 적절한 값을 검색하기
      messages=[
            {
               "role": "user",
               "content": system_prompt,
            },
            {
               "role": "assistant",
               "content": sticc_content,
            },
            {
               "role": "user",
               "content": sticc_content,
            },
            {
               "role": "user",
               "content": "Given the details I've provided, could you assess my current progress, identify obstacles, and suggest next action items?"
            }
      ],
      temperature=0.5,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
   )

   return {"response": response.choices[0].message.content}

"""
