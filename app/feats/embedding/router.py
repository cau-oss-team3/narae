from fastapi import APIRouter, Depends

import openai as OpenAI
from app.feats.embedding.service import get_best_RAG
from app.feats.prompt.depends import get_openai_client


router = APIRouter(prefix="/embedding", tags=["embedding"])


@router.post("/")
def test_get_embedding(user_input, client: OpenAI = Depends(get_openai_client)):
    return get_best_RAG(user_input, client)
