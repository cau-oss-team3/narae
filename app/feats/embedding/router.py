from fastapi import APIRouter, Depends
from openai import AsyncOpenAI

from app.feats.embedding.service import test_embedding
from app.feats.prompt.depends import get_openai_async_client

router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.get(
    "/embedding/",
    description="Test embedding",
)
async def embedding(
        client: AsyncOpenAI = Depends(get_openai_async_client),
):
    test = await test_embedding(client)
    return test
