"""
무엇을 위한 코드인가: 사용자의 응답을 받아서 GPT가 출력하게 하는 코드
프롬프트 문장은 여기에다 넣음
"""

from fastapi import FastAPI, APIRouter, Depends
from openai import OpenAI

from schemas import UserSituationRequest
from .depends import get_openai_client

app = FastAPI()

# 사용자에게 무엇을 할 것인지 알려주는 메시지가 들어가야 함
SYSTEM_PROMPT = """
I'm here to guide you through your learning journey. Today, I'll be providing advice on study direction and next steps. How can I assist you?
"""

"""
    1. 다음에 해야 하는 ***학습 방향***을 제시해줘야 한다.
    - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
    - 오늘 접속한 경우 띄워준다.
    - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.
"""


def format_direction_for_study():
    direction_content = f"""
    I've heard that you are a world-renowned coach in the field of backend development coaching. I want to improve my expertise in backend within this field, but I'm having trouble. I will tell you what I've tried so far and what hasn't worked. 
    Based on this information, could you assess my current progress, identify obstacles, and suggest next action items? If necessary, please provide motivational feedback. Additionally, please use the following details to ask me questions to enhance my API design skills and provide expert feedback on my responses. If my responses are lacking, kindly suggest areas for improvement, necessary understandings, and request further explanation.
    I've heard from various sources about your esteemed reputation as a world-renowned coach specializing in backend development. My eagerness to enhance my proficiency in backend within this vast domain led me to seek your guidance. Despite my sincere efforts, I find myself encountering hurdles along the way. I'm determined to overcome these obstacles and propel my skills forward. To provide you with context, I'll outline the strategies I've employed thus far, along with the challenges I've faced in executing them effectively.
    Given this backdrop, I humbly request your assessment of my current progress. I'm keen to receive your expert insights into the roadblocks impeding my advancement. Additionally, I seek your guidance on charting the most effective course of action moving forward. Your tailored recommendations, aligned with my current progress and aspirations, would be invaluable. Moreover, I'm open to receiving motivational feedback to bolster my resolve and ignite a renewed sense of determination. Furthermore, I eagerly anticipate your expertise in refining my API design skills. Feel free to pose questions aimed at enhancing my understanding and providing constructive feedback on my responses. Your guidance in identifying areas for improvement and suggesting necessary insights would be greatly appreciated.
    Your reputation as a distinguished coach in backend development precedes you, and I'm eager to tap into your expertise to elevate my skills in this domain. Despite my earnest efforts, I've hit a roadblock in my quest for improvement. I believe sharing my experiences and challenges with you can provide valuable insights to chart a more effective path forward.
    Additionally, I'm eager to leverage your expertise to enhance my API design skills. Please don't hesitate to engage me with thought-provoking questions and offer expert feedback on my responses. Your guidance in pinpointing areas for improvement and providing necessary clarifications will be invaluable as I strive for excellence in this field.
    """

    return direction_content


"""
    2. 오늘 학습 방향에 따라 실천 가능한 ***액션을*** 추천한다.
    - 이때 실천 가능할만큼 구체적이고 적절한 난이도의 조언을 해야 한다.
    - 내가 처음인지/어디까지 해봤는지 알아야 한다.
    - 액션을 어떻게 완수했는지 알릴 수 있어야 한다. 액션 완수 내용을 말하면 피드백 해줘야 한다.
    - 액션 포기가 가능해야 한다. 포기하는 경우 이유를 말해고 다음 액션을 추천해준다.(+서버에 저장)
"""


def format_recommend_action():
    recommend_content = f"""
    It's commendable that you're actively seeking to align your learning direction with actionable tasks. By tailoring these tasks to your interests and proficiency level, you can effectively bridge the gap between theory and practice. Let's delve into specific recommendations that offer a tangible pathway to progress.
    Considering your current focus on backend development coaching, a practical step could involve dedicating regular time slots to hands-on coding exercises. These exercises should not only reinforce your theoretical understanding but also enhance your practical skills. Start with relatively simple tasks, such as debugging code snippets or implementing basic functionalities, gradually increasing the complexity as you gain confidence. Additionally, consider engaging in collaborative projects or contributing to open-source repositories to broaden your exposure to real-world scenarios and foster teamwork skills.
    It's crucial to strike a balance between challenging yourself and avoiding overwhelming tasks. Set realistic goals for each session, breaking them down into manageable chunks. For instance, if you're exploring a new concept or language feature, aim to implement it in a small project or integrate it into an existing codebase. Regularly review your progress and adjust your learning plan accordingly, identifying areas for improvement and seeking resources or mentorship when needed. By adopting this iterative approach to learning, you'll not only solidify your understanding but also cultivate a proactive mindset towards continuous improvement.
    """

    return recommend_content


"""
    3. 나의 현재 학습 분야에 대한 질문에 ***답***을 해줘야 한다.
    - 기본적인 채팅의 형태로 이루어진다.
    - 임베딩이 사용할 수 있으면 좋다.
"""


def format_answer_for_question():
    answer_content = f"""
    Respond to queries about your areas of interest in a chat-based format, engaging in conversational dialogue and providing detailed insights.
    Provide answers to questions about your areas of interest, addressing inquiries comprehensively and in a conversational manner.
    Offer responses to questions related to your areas of interest, engaging users in informative and engaging discussions.
    Engage in casual conversation and provide answers to inquiries regarding your areas of interest, ensuring responses are informative and engaging.
    Answer questions regarding your areas of interest in a chat-friendly format, fostering an engaging and interactive conversation.
    """

    return answer_content


"""
    현재로서는 사용할 지 알 수 없음
    Format the user's situation using the STICC model to enhance the clarity and detail of the input for coaching purposes.
    Parameters:
    - sticc (object): An object containing attributes of the STICC model (situation, task, intent, concerns, calibration).
    Returns:
    - str: A formatted string suitable for prompting GPT with the details necessary for effective coaching.
"""


def format_sticc_for_coaching(sticc):
    # Construct the STICC content string with clear labels and user input.
    sticc_content = f"""
    I will describe my situation using the STICC model to facilitate more tailored and effective coaching.
    Situation: The current context or environment in which I'm operating is "{sticc.situation}".
    Task: My specific task or objective is "{sticc.task}".
    Intent: My intention or goal in this scenario is "{sticc.intent}".
    Concerns: My concerns or challenges are "{sticc.concerns}".
    Calibration: Any specific adjustments or calibrations needed are "{sticc.calibration}".
    """

    return sticc_content


# 1에 대한 함수(existing_learning: 이전 학습 기록, learning_goal: 커리큘럼과 마일스톤)
@app.post("/direction/")
def get_study_direction(
    study_direction: format_direction_for_study,
    existing_learning,
    learning_goal,
    client: OpenAI = Depends(get_openai_client),
):
    prompt = f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease provide detailed guidance for the next steps in learning, taking into account the current knowledge and the desired learning outcome."
    response = client.Completion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the today's study direction and next short-term goal to the user. Your message is given to the user just before the study starts.",
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
        prompt=prompt,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    return response.choices[0].text.strip()


# 2에 대한 함수(existing_learning: 이전 학습 기록, learning_goal: 커리큘럼과 마일스톤)
@app.post("/recommendation/")
def get_recommended_action(
    recommend_action: format_recommend_action,
    existing_learning,
    learning_goal,
    client: OpenAI = Depends(get_openai_client),
):
    prompt = f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease recommend an action that can be done according to today's learning direction."
    response = client.Completion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the next action which depends to the today's study direction. Your message is given to the user after the's study direction is given. Make sure your advice is specific enough to be actionable and at the right level of difficulty.",
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
        prompt=prompt,
        temperature=0.75,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )

    # 사용자가 액션을 완료할 시 이에 대한 응답
    if "completed" in response_text.lower():
        feedback_prompt = "Please provide feedback on how you completed the action."
        response_with_feedback = client.Completion.create(
            model="gpt-3.5-turbo-1106",
            prompt=feedback_prompt,
            temperature=0.5,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )
        response_text += (
            "\n\nFeedback: " + response_with_feedback.choices[0].text.strip()
        )

    # 사용자가 액션을 포기할 시 이에 대한 응답
    elif "abandoned" in response_text.lower():
        reason_prompt = "Please specify the reason for abandoning the action."
        next_action_prompt = "Based on your reason for abandoning the action, here's the next recommended action."

        reason_response = client.Completion.create(
            model="gpt-3.5-turbo-1106",
            prompt=reason_prompt,
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

        next_action_response = client.Completion.create(
            model="gpt-3.5-turbo-1106",
            prompt=next_action_prompt,
            temperature=0.75,
            max_tokens=150,
            frequency_penalty=0,
            presence_penalty=0,
        )

    return response_text


# 3에 대한 함수
@app.post("/question/")
def get_answer_question(
    study_direction: format_answer_for_question,
    user_question,
    client: OpenAI = Depends(get_openai_client),
):
    prompt = (
        f"Please provide an answer to the user's question about your areas of interest."
    )
    response = client.Completion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are a teacher who gives answer to the question which the user gives.",
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
        prompt=prompt,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].text.strip()


"""
# @app.post("/test-gpt/")
def test_gpt(sticc: UserSituationRequest, client: OpenAI = Depends(get_openai_client)):
    userInput = format_sticc_for_coaching(sticc)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
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
