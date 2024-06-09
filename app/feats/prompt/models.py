from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


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


class GPTResponse(BaseModel):
    curriculum: str
