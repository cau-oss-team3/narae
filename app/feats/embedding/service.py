from openai import AsyncOpenAI

from app.settings import settings

EMBEDDING_MODEL = settings.gpt_embedding_model


async def get_embedding(client: AsyncOpenAI, text):
    text = text.replace("\n", " ")
    response = await client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return response.data[0].embedding


async def test_embedding(client: AsyncOpenAI):
    text = "I am happy"
    return await get_embedding(client, text)
