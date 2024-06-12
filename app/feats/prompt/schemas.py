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
    mentor_id: int
    hint: Optional[str] = ''


class ActionSuggestionRequest(BaseModel):
    mentor_id: int
    hint: Optional[str] = None


class QuestionRequest(BaseModel):
    mentor_id: int
    question: str


class GPTResponse(BaseModel):
    curriculum: str
