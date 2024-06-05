from fastapi import Depends
import json

import openai as OpenAI
from app.feats.prompt.depends import get_openai_client

moderation_tags = [
    "harassment",
    "harassment/threatening",
    "hate",
    "hate/threatening",
    "self-harm",
    "self-harm/instructions",
    "self-harm/intent",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def moderation_exist(user_input, client: OpenAI = Depends(get_openai_client)):
    response = client.moderations.create(input=user_input)
    moderation_output = response.model_dump()

    test = moderation_output["results"][0]["categories"]

    for tag in moderation_tags:
        if test[tag]:
            return True
    return False
