from typing import Optional

from pydantic import BaseModel


class UserSituationRequest(BaseModel):
    situation: str = "The problem i have faced is xxx."
    task: str = "To solve this problem, we have to do xxx."
    intent: str = "The reason for this is xxx."
    concerns: str = "But there is something that we must aware and be cautious."
    calibration: str = (
        "Let's talk about things that we do not understand, or difficult, or we do not know, or should calibrate."
    )


class CurriculumRequest(BaseModel):
    hint: Optional[str] = ''


class ActionSuggestRequest(BaseModel):
    hint: Optional[str] = None


class SetNewActionRequest(BaseModel):
    action: str


class CompleteActionResultRequest(BaseModel):
    result: str
    reason: str = ''


class QuestionRequest(BaseModel):
    question: str


class GPTResponse(BaseModel):
    curriculum: str
