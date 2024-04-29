from openai import OpenAI

from app.settings import settings


def get_openai_client():
    return OpenAI(api_key=settings.gpt_key)