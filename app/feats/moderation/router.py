from fastapi import APIRouter, Depends
from openai import AsyncOpenAI

from app.feats.moderation.service import advanced_moderation_async, check_moderation_violation_async
from app.feats.prompt.depends import get_openai_async_client

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.post("/violation")
async def test_moderation_violation(user_input, client: AsyncOpenAI = Depends(get_openai_async_client)):
    """
    Test moderation violation and see detailed results.
    """
    return await advanced_moderation_async(user_input, client)


@router.post("/check_input")
async def check_input(user_input, client: AsyncOpenAI = Depends(get_openai_async_client)):
    """
    Check if the user input is a violation.
    """
    return await check_moderation_violation_async(user_input, client)
