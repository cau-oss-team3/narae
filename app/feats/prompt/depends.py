from openai import OpenAI

from app.feats.prompt.schemas import UserSituationRequest
from app.settings import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.gpt_key)


def get_direction_for_study() -> str:
    return format_direction_for_study()


def get_recommend_action() -> str:
    return format_recommend_action()


def get_answer_for_question() -> str:
    return format_answer_for_question()


def format_direction_for_study():
    """
    1. 다음에 해야 하는 "학습 방향"을 제시해줘야 한다.
    - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
    - 오늘 접속한 경우 띄워준다.
    - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.
    """

    return """
    I've heard that you are a world-renowned coach in the field of backend development coaching. I want to improve my expertise in backend within this field, but I'm having trouble. I will tell you what I've tried so far and what hasn't worked.
    Based on this information, could you assess my current progress, identify obstacles, and suggest next action items? If necessary, please provide motivational feedback. Additionally, please use the following details to ask me questions to enhance my API design skills and provide expert feedback on my responses. If my responses are lacking, kindly suggest areas for improvement, necessary understandings, and request further explanation.
    I've heard from various sources about your esteemed reputation as a world-renowned coach specializing in backend development. My eagerness to enhance my proficiency in backend within this vast domain led me to seek your guidance. Despite my sincere efforts, I find myself encountering hurdles along the way. I'm determined to overcome these obstacles and propel my skills forward. To provide you with context, I'll outline the strategies I've employed thus far, along with the challenges I've faced in executing them effectively.
    Given this backdrop, I humbly request your assessment of my current progress. I'm keen to receive your expert insights into the roadblocks impeding my advancement. Additionally, I seek your guidance on charting the most effective course of action moving forward. Your tailored recommendations, aligned with my current progress and aspirations, would be invaluable. Moreover, I'm open to receiving motivational feedback to bolster my resolve and ignite a renewed sense of determination. Furthermore, I eagerly anticipate your expertise in refining my API design skills. Feel free to pose questions aimed at enhancing my understanding and providing constructive feedback on my responses. Your guidance in identifying areas for improvement and suggesting necessary insights would be greatly appreciated.
    Your reputation as a distinguished coach in backend development precedes you, and I'm eager to tap into your expertise to elevate my skills in this domain. Despite my earnest efforts, I've hit a roadblock in my quest for improvement. I believe sharing my experiences and challenges with you can provide valuable insights to chart a more effective path forward.
    Additionally, I'm eager to leverage your expertise to enhance my API design skills. Please don't hesitate to engage me with thought-provoking questions and offer expert feedback on my responses. Your guidance in pinpointing areas for improvement and providing necessary clarifications will be invaluable as I strive for excellence in this field.
    """


def format_recommend_action():
    """
    2. 오늘 학습 방향에 따라 실천 가능한 ***액션을*** 추천한다.
    - 이때 실천 가능할만큼 구체적이고 적절한 난이도의 조언을 해야 한다.
    - 내가 처음인지/어디까지 해봤는지 알아야 한다.
    - 액션을 어떻게 완수했는지 알릴 수 있어야 한다. 액션 완수 내용을 말하면 피드백 해줘야 한다.
    - 액션 포기가 가능해야 한다. 포기하는 경우 이유를 말해고 다음 액션을 추천해준다.(+서버에 저장)
    """

    return """
    It's commendable that you're actively seeking to align your learning direction with actionable tasks. By tailoring these tasks to your interests and proficiency level, you can effectively bridge the gap between theory and practice. Let's delve into specific recommendations that offer a tangible pathway to progress.
    Considering your current focus on backend development coaching, a practical step could involve dedicating regular time slots to hands-on coding exercises. These exercises should not only reinforce your theoretical understanding but also enhance your practical skills. Start with relatively simple tasks, such as debugging code snippets or implementing basic functionalities, gradually increasing the complexity as you gain confidence. Additionally, consider engaging in collaborative projects or contributing to open-source repositories to broaden your exposure to real-world scenarios and foster teamwork skills.
    It's crucial to strike a balance between challenging yourself and avoiding overwhelming tasks. Set realistic goals for each session, breaking them down into manageable chunks. For instance, if you're exploring a new concept or language feature, aim to implement it in a small project or integrate it into an existing codebase. Regularly review your progress and adjust your learning plan accordingly, identifying areas for improvement and seeking resources or mentorship when needed. By adopting this iterative approach to learning, you'll not only solidify your understanding but also cultivate a proactive mindset towards continuous improvement.
    """


def format_answer_for_question():
    """
    3. 나의 현재 학습 분야에 대한 질문에 ***답***을 해줘야 한다.
    - 기본적인 채팅의 형태로 이루어진다.
    - 임베딩이 사용할 수 있으면 좋다.
    """

    return """
    Respond to queries about your areas of interest in a chat-based format, engaging in conversational dialogue and providing detailed insights.
    Provide answers to questions about your areas of interest, addressing inquiries comprehensively and in a conversational manner.
    Offer responses to questions related to your areas of interest, engaging users in informative and engaging discussions.
    Engage in casual conversation and provide answers to inquiries regarding your areas of interest, ensuring responses are informative and engaging.
    Answer questions regarding your areas of interest in a chat-friendly format, fostering an engaging and interactive conversation.
    """


def format_sticc_for_coaching(sticc: UserSituationRequest):
    """
    NOTE: 현재로서는 사용할 지 알 수 없음

    Format the user's situation using the STICC model to enhance the clarity and detail of the input for coaching purposes.

    Parameters:
    - sticc (object): An object containing attributes of the STICC model (situation, task, intent, concerns, calibration).
    Returns:
    - str: A formatted string suitable for prompting GPT with the details necessary for effective coaching.
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
