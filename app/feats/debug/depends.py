from openai import OpenAI

from app import settings


def get_openai_client():
    return OpenAI(settings.gpt_key)