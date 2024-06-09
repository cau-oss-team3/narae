from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class UserSituationRequest(BaseModel):
    situation: str = "The problem i have faced is xxx."
    task: str = "To solve this problem, we have to do xxx."
    intent: str = "The reason for this is xxx."
    concerns: str = "But there is something that we must aware and be cautious."
    calibration: str = (
        "Let's talk about things that we do not understand, or difficult, or we do not know, or should calibrate."
    )


class CurriculumRequest(BaseModel):
    field: str = Field(..., title="Field of Development",
                       description="The specific field of development the user wants to learn.")
    sticc: str = Field(..., title="STICC Information",
                       description="User's situation, task, intent, concerns, and calibration (STICC) information.")

    @field_validator('field', 'sticc')
    @classmethod
    def check_not_empty(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            is_empty = v.strip() == ''
            assert not is_empty, 'Field must not be empty'

        return v

    def to_dict(self) -> dict:
        return {
            "FIELD": self.field,
            "STICC": self.sticc
        }


class ActionSuggestionRequest(BaseModel):
    mentor_id: int
    hint: Optional[str] = None


class QuestionRequest(BaseModel):
    mentor_id: int
    question: str


class GPTResponse(BaseModel):
    curriculum: str
