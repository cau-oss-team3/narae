from fastapi import APIRouter, Depends

import openai as OpenAI
from app.feats.moderation.service import check_moderation_violation, advanced_moderation
from app.feats.prompt.depends import get_openai_client

router = APIRouter(prefix="/moderation", tags=["moderation"])


@router.post("/violation")
def test_moderation_violation(user_input, client: OpenAI = Depends(get_openai_client)):
    """
    Test moderation violation and see detailed results.
    """
    return advanced_moderation(user_input, client)


@router.post("/check_input")
def check_input(user_input, client: OpenAI = Depends(get_openai_client)):
    """
    Check if the user input is a violation.
    """
    return check_moderation_violation(user_input, client)
