from openai import OpenAI

from fastapi import FastAPI
from fastapi import APIRouter, Depends
from app.feats.mentors.schemas import MentorDTO


OPENAI_MODEL = "gpt-3.5-turbo-1106"  ## "gpt-4o"
OPENAI_EMB_MODEL = "text-embedding-3-small"

app = FastAPI()


def get_embedding(text, client: OpenAI = Depends(OPENAI_MODEL)):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=OPENAI_EMB_MODEL).data[0].embedding
    )


## @app.get("/get-study-direction/")
def get_study_direction(
    study_direction,
    client: OpenAI,
    existing_learning="",
    learning_goal="",
    RAG_data="",
):
    """
    <학습 방향>에 대한 함수

    용어
     - Action: 오늘 당장 실행할 수 있는 Task

    다음에 해야 하는 ***학습 방향***을 제시해줘야 한다.
     - DB에 저장해서 사용자가 다시 찾아볼 수 있도록 제공한다.
     - 오늘 접속한 경우 띄워준다.
     - 액션을 하기 전 사용자가 학습 방향을 먼저 제시받아야 한다.

    Parameters:
     - existing_learning: 이전 학습 기록
     - learning_goal: 커리큘럼과 마일스톤
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a guide who suggests the today's study direction and next short-term goal to the user. Your message is given to the user just before the study starts."
                + "Make sure your advice is specific enough to be actionable and at the right level of difficulty."
                + "Also, make sure to motivate the user to keep going."
                + f"Existing learning content: {existing_learning}\nLearning goal: {learning_goal}\nPlease provide detailed guidance for the next steps in learning, taking into account the current knowledge and the desired learning outcome."
                + "You should not exceed 200 words. Please say it in Korean. Thank you.",
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
                "role": "assistant",
                "content": RAG_data
                + " When generating a response, make sure to reference and cross-verify the output using data retrieved through Retrieval-Augmented Generation(RAG). Follow these steps to ensure accuracy."
                + "1. Retrieve Relevant Data: Use the RAG system to fetch pertinent information that can support the response."
                + "2. Cross-Verify Information: Check the generated response against the retrieved data to confirm its correctness."
                + "3. Identify Discrepancies: If there are any discrepancies between the generated response and the RAG data, prioritize the information from the RAG data."
                + "4. Provide Justification: Include references or explanations based on the RAG data to justify the response.",
            },
            {
                "role": "user",
                "content": study_direction.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    study_direction_response = response.choices[0].message.content

    embedding = get_embedding(study_direction_response, client)
    return {"message": study_direction_response, "embedding": embedding}


## @app.get("/get-qna-answer/")
def get_qna_answer(
    question,
    mentor: MentorDTO,
    client: OpenAI,
    existing_learning="",
    RAG_data="",
):
    response = client.chat.completions.create, get_embedding(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": f"You are a guide specializing in {mentor.mentor_field} with the expertise of {mentor.mentor_sticc}. "
                + "Your task is to suggest today's study direction and the next short-term goal to the user, "
                + "tailoring your advice to the user’s current knowledge level in {mentor.mentor_field} and desired learning outcomes. "
                + "Your message is delivered just before the study session begins. "
                + "Ensure your advice is specific, actionable, and motivating, encouraging the user to persist in their studies."
                + f"Question: {question}\nPlease provide detailed guidance for the next steps in learning, taking into account the current knowledge and the desired learning outcome."
                + "You should not exceed 200 words and please provide the response in Korean.",
            },
            {
                "role": "assistant",
                "content": existing_learning,
            },
            {
                "role": "assistant",
                "content": RAG_data
                + " When generating a response, make sure to reference and cross-verify the output using data retrieved through Retrieval-Augmented Generation(RAG). Follow these steps to ensure accuracy."
                + "1. Retrieve Relevant Data: Use the RAG system to fetch pertinent information that can support the response."
                + "2. Cross-Verify Information: Check the generated response against the retrieved data to confirm its correctness."
                + "3. Identify Discrepancies: If there are any discrepancies between the generated response and the RAG data, prioritize the information from the RAG data."
                + "4. Provide Justification: Include references or explanations based on the RAG data to justify the response.",
            },
            {
                "role": "user",
                "content": question.replace("\n", " "),
            },
        ],
        temperature=0.75,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.75,
    )
    qna_answer_response = response.choices[0].message.content

    embedding = get_embedding(qna_answer_response, client)
    return {"message": qna_answer_response, "embedding": embedding}
