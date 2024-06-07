from fastapi import APIRouter, Depends

import openai as OpenAI
from app.feats.moderation.service import upgrade_moderation
from app.feats.prompt.depends import get_openai_client


router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.post("/")
def test_get_moderation(user_input, client: OpenAI = Depends(get_openai_client)):
    return upgrade_moderation(user_input, client)
