from fastapi import APIRouter, Depends
from openai import OpenAI

from .schemas import GPTRequest, GPTResponse
from .depends import get_openai_client


router = APIRouter(prefix="/debug", tags=["debug"])


@router.post(
    "/gpt-test/",
    description="Simple demo for testing GPT-3-turbo model",
    response_model=GPTResponse,
)
async def gpt_test(request: GPTRequest, client: OpenAI = Depends(get_openai_client)):
    system_content = f"""
    I've heard that you are a world-renowned coach in the field of backend development coaching.
    I want to improve my expertise in {request.interest} within this field, but I'm having trouble.
    Here are the details of what I've tried so far and what hasn't worked: {request.session_details}

    Based on this information, could you assess my current progress, identify obstacles, and suggest next action items?
    If necessary, please provide motivational feedback.
    Additionally, please use the following details to ask me questions to enhance my API design skills and provide expert feedback on my responses. If my responses are lacking, kindly suggest areas for improvement, necessary understandings, and request further explanation.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": "Given the details I've provided, could you assess my current progress, identify obstacles, and suggest next action items?",
            },
        ],
        temperature=0.5,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return GPTResponse(response=response.choices[0].message.content)
