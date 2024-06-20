import asyncio

import tiktoken
from openai import AsyncOpenAI
from sqlalchemy import select

from app.feats.embedding.models import DocumentChunk, EmbeddingItem
from app.feats.embedding.schemas import CreateDocumentRequest
from app.settings import settings

EMBEDDING_MODEL = settings.gpt_embedding_model
DIMENSION_OF_MODEL = settings.gpt_embedding_dimension


async def save_document_embedding(client: AsyncOpenAI, session, request: CreateDocumentRequest):
    # TODO: langchain chunker로 변경
    paragraphs = request.document.split("\n")

    embeddings = await asyncio.gather(
        *[get_embedding(client, paragraph) for paragraph in paragraphs]
    )

    async with session:
        for i, embedding in enumerate(embeddings):
            chunk = DocumentChunk(field=request.field, document=embedding[0], embedding=embedding[1])
            session.add(chunk)
        await session.commit()

    # make embeddings's embedding to smaller size
    return [(embedding[0], embedding[1][:10]) for embedding in embeddings]


async def get_document_embedding(session, field, user_input):
    async with session:
        query = session.query(DocumentChunk).filter(DocumentChunk.field == field)
        chunks = await query.all()
        embeddings = [chunk.embedding for chunk in chunks]


async def calculate_similar_vector_item(request, session):
    query = select(
        EmbeddingItem,
        (1 - EmbeddingItem.embedding.cosine_distance(request.embedding)).label('distance')
    )
    async with session:
        items = (await session.execute(query)).all()
        result = [
            {
                "name": item[0].name,
                "embedding": item[0].embedding.tolist(),
                "distance": item[1]
            }
            for item in items
        ]
    return result


async def get_embedding(client: AsyncOpenAI, text):
    text = text.replace("\n", " ")
    response = await client.embeddings.create(input=[text], model=EMBEDDING_MODEL)
    return text, response.data[0].embedding


def num_tokens_from_string(string: str, encoding_name="cl100k_base") -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens
