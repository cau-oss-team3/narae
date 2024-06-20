from fastapi import APIRouter, Depends
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.embedding.models import EmbeddingItem
from app.feats.embedding.schemas import CreateVectorItemRequest, PatchVectorItemRequest, CreateDocumentRequest
from app.feats.embedding.service import num_tokens_from_string, save_document_embedding, get_embedding, \
    calculate_similar_vector_item
from app.feats.prompt.depends import get_openai_async_client

router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.post("/document/", description="Test saving document to db")
async def create_document_item(
        request: CreateDocumentRequest,
        client: AsyncOpenAI = Depends(get_openai_async_client),
        session: AsyncSession = Depends(get_async_session)
):
    return await save_document_embedding(client, session, request)


@router.post("/vector/", description="Test saving embedding to db")
async def create_vector_item(
        request: CreateVectorItemRequest,
        session: AsyncSession = Depends(get_async_session)
):
    new_item = EmbeddingItem(**request.dict())
    async with session:
        session.add(new_item)
        await session.commit()
    return new_item


@router.patch("/vector/", description="Test getting embedding from db")
async def patch_vector_item_by_similarity(
        request: PatchVectorItemRequest,
        session: AsyncSession = Depends(get_async_session)
):
    return await calculate_similar_vector_item(request, session)


@router.get(
    "/tokens/",
    description="Get number of tokens in a string",
)
async def get_token_count(
        text: str,
):
    return num_tokens_from_string(text)


@router.get(
    "/embedding/",
    description="Test embedding",
)
async def test_embedding(
        text: str = "This is a test",
        client: AsyncOpenAI = Depends(get_openai_async_client),
):
    return await get_embedding(client, text)
