import asyncio

import tiktoken
from fastapi import HTTPException
from openai import AsyncOpenAI
from sqlalchemy import select
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.feats.embedding.models import DocumentChunk, EmbeddingItem
from app.feats.embedding.schemas import CreateDocumentRequest
from app.settings import settings

EMBEDDING_MODEL = settings.gpt_embedding_model
DIMENSION_OF_MODEL = settings.gpt_embedding_dimension


async def read_all_documents(session):
    async with session:
        query = select(DocumentChunk.field, DocumentChunk.document)
        items = (await session.execute(query)).all()
        return [
            {
                "field": "backend" if item.field == 0 else ("frontend" if item.field == 1 else "fullstack"),
                "document": item.document,
                "embedding": "not shown"
            }
            for item in items
        ]


async def retrieve_similar_documents(client: AsyncOpenAI, session, field: int, user_input: str, top_n: int = 3) -> list:
    user_input_embedding = (await get_embedding(client, user_input))[1]
    query = select(
        DocumentChunk,
        1 - DocumentChunk.embedding.cosine_distance(user_input_embedding)
    ).filter(
        (DocumentChunk.field == field) & (DocumentChunk.embedding.cosine_distance(user_input_embedding) < 0.5)
    )

    async with session:
        items = (await session.execute(query)).all()
        items = sorted(items, key=lambda x: x[1], reverse=True)
        return [
            {
                "document": item[0].document,
                "embedding": item[0].embedding.tolist()[0:10],
                "distance": item[1]
            }
            for item in items[:top_n]
        ]


async def save_document_embedding(client: AsyncOpenAI, session, request: CreateDocumentRequest):
    # Split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=20, length_function=len)
    chunks = text_splitter.split_text(request.document)
    if not chunks:
        raise HTTPException(status_code=400, detail="Document could not be split into valid chunks.")

    embeddings = await asyncio.gather(
        *[get_embedding(client, chunk) for chunk in chunks]
    )

    async with session:
        for i, embedding in enumerate(embeddings):
            chunk = DocumentChunk(field=request.field, document=embedding[0], embedding=embedding[1])
            session.add(chunk)
        await session.commit()

    return [(embedding[0], embedding[1][:10]) for embedding in embeddings]


async def calculate_similar_vector_item(request, session):
    """
    [NOTE]: This is for testing purposes only.
    Calculate the cosine distance between the given embedding and all embeddings in the database.
    """
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
