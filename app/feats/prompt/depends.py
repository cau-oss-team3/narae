from fastapi import Depends
from openai import OpenAI

from app.settings import settings


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=settings.gpt_key)


def get_embedding(text, client: OpenAI = Depends(settings.gpt_model)):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=settings.gpt_embedding_model)
        .data[0]
        .embedding
    )
