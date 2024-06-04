from enum import Enum

from app.feats.prompt.schemas import UserSituationRequest


class Field(int, Enum):
    BACKEND = 0
    FRONTEND = 1
    FULL_STACK = 2

    @staticmethod
    def get_field_name(field_number: int) -> str:
        return {
            0: "backend development",
            1: "frontend development",
            2: "full-stack development",
        }[field_number]


def get_prompt_of_curriculum(field: Field = Field.BACKEND) -> str:
    """
    Returns a prompt for requesting expert assessment and guidance in a specific field of development.
    Should motivate the user to

    Parameters:
        field (Field): The field of development for which expert guidance is requested.

    Returns:
        str: A prompt requesting expert assessment, guidance, and feedback in the specified field of development.

    Example: >>> get_prompt_of_curriculum(Field.BACKEND) "I've heard that you are a world-renowned coach in the field
    of backend development coaching. I want to improve my expertise in backend development, but I'm having trouble. I
    will tell you what I've tried so far and what hasn't worked. Based on this information, could you assess my
    current progress, identify obstacles, and suggest next action items? If necessary, please provide motivational
    feedback. Additionally, please use the following details to ask me questions to enhance my skills and provide
    expert feedback on my responses. If my responses are lacking, kindly suggest areas for improvement,
    necessary understandings, and request further explanation. I believe sharing my experiences and challenges with
    you can provide valuable insights to chart a more effective path forward. Additionally, I'm eager to leverage
    your expertise to enhance my backend development skills. Please don't hesitate to engage me with
    thought-provoking questions and offer expert feedback on my responses. Your guidance in pinpointing areas for
    improvement and providing necessary clarifications will be invaluable as I strive for excellence in this field.
    Please consider my journey thus far and provide your expert assessment of my progress. I'm eager to receive your
    insights on overcoming obstacles and identifying actionable steps to propel my learning journey forward. Your
    tailored recommendations, motivational feedback, and expert guidance on backend development area will be
    instrumental in shaping my growth and development. Use only Korean for responses."
    """
    field = Field.get_field_name(field)

    return f"""
    I've heard that you are a world-renowned coach in the field of {field} coaching. I want to improve my expertise 
    in {field}, but I'm having trouble. I will tell you what I've tried so far and what hasn't worked. Based on this 
    information, could you assess my current progress, identify obstacles, and suggest next action items? If 
    necessary, please provide motivational feedback. Additionally, please use the following details to ask me 
    questions to enhance my skills and provide expert feedback on my responses. If my responses are lacking, 
    kindly suggest areas for improvement, necessary understandings, and request further explanation. I believe 
    sharing my experiences and challenges with you can provide valuable insights to chart a more effective path 
    forward. Additionally, I'm eager to leverage your expertise to enhance my {field} skills. Please don't hesitate 
    to engage me with thought-provoking questions and offer expert feedback on my responses. Your guidance in 
    pinpointing areas for improvement and providing necessary clarifications will be invaluable as I strive for 
    excellence in this field. Please consider my journey thus far and provide your expert assessment of my progress. 
    I'm eager to receive your insights on overcoming obstacles and identifying actionable steps to propel my learning 
    journey forward. Your tailored recommendations, motivational feedback, and expert guidance on {field} area will 
    be instrumental in shaping my growth and development.
    Use only Korean for responses.
    """


def get_prompt_of_daily_action() -> str:
    """
    2. 오늘 학습 방향에 따라 실천 가능한 **액션을** 추천한다.
    - 이때 실천 가능할만큼 구체적이고 적절한 난이도의 조언을 해야 한다.
    - 내가 처음인지/어디까지 해봤는지 알아야 한다.
    - 액션을 어떻게 완수했는지 알릴 수 있어야 한다. 액션 완수 내용을 말하면 피드백 해줘야 한다.
    - 액션 포기가 가능해야 한다. 포기하는 경우 이유를 말해고 다음 액션을 추천해준다.(+서버에 저장)
    """

    return """It's commendable that you're actively seeking to align your learning direction with actionable tasks. 
    By tailoring these tasks to your interests and proficiency level, you can effectively bridge the gap between 
    theory and practice. Let's delve into specific recommendations that offer a tangible pathway to progress. 
    Considering your current focus on backend development coaching, a practical step could involve dedicating regular 
    time slots to hands-on coding exercises. These exercises should not only reinforce your theoretical understanding 
    but also enhance your practical skills. Start with relatively simple tasks, such as debugging code snippets or 
    implementing basic functionalities, gradually increasing the complexity as you gain confidence. Additionally, 
    consider engaging in collaborative projects or contributing to open-source repositories to broaden your exposure 
    to real-world scenarios and foster teamwork skills. It's crucial to strike a balance between challenging yourself 
    and avoiding overwhelming tasks. Set realistic goals for each session, breaking them down into manageable chunks. 
    For instance, if you're exploring a new concept or language feature, aim to implement it in a small project or 
    integrate it into an existing codebase. Regularly review your progress and adjust your learning plan accordingly, 
    identifying areas for improvement and seeking resources or mentorship when needed. By adopting this iterative 
    approach to learning, you'll not only solidify your understanding but also cultivate a proactive mindset towards 
    continuous improvement."""


def get_prompt_of_qna() -> str:
    """
    3. 나의 현재 학습 분야에 대한 질문에 **답**을 해줘야 한다.
    - 기본적인 채팅의 형태로 이루어진다.
    - 임베딩이 사용할 수 있으면 좋다.
    """

    return """Respond to queries about your areas of interest in a chat-based format, engaging in conversational 
    dialogue and providing detailed insights. Provide answers to questions about your areas of interest, addressing 
    inquiries comprehensively and in a conversational manner. Offer responses to questions related to your areas of 
    interest, engaging users in informative and engaging discussions. Engage in casual conversation and provide 
    answers to inquiries regarding your areas of interest, ensuring responses are informative and engaging. Answer 
    questions regarding your areas of interest in a chat-friendly format, fostering an engaging and interactive 
    conversation."""


def format_sticc_for_coaching(sticc: UserSituationRequest):
    """
    Format the user's situation using the STICC model to enhance the clarity and detail of the input for coaching
    purposes.

    Parameters: - sticc (object): An object containing attributes of the STICC model (situation, task, intent,
    concerns, calibration). Returns: - str: A formatted string suitable for prompting GPT with the details necessary
    for effective coaching.
    """

    # Construct the STICC content string with clear labels and user input.
    return f"""
    I will describe my situation using the STICC model to facilitate more tailored and effective coaching.
    Situation: The current context or environment in which I'm operating is "{sticc.situation}".
    Task: My specific task or objective is "{sticc.task}".
    Intent: My intention or goal in this scenario is "{sticc.intent}".
    Concerns: My concerns or challenges are "{sticc.concerns}".
    Calibration: Any specific adjustments or calibrations needed are "{sticc.calibration}".
    """
