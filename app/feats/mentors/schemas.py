from pydantic import BaseModel, Field, validator
from app.core.exceptions import AuthenticationFailedException


class STICC(BaseModel):
    situation: str = Field(min_length=100, max_length=256)
    task: str = Field(min_length=100, max_length=256)
    intent: str = Field(min_length=100, max_length=256)
    concern: str = Field(min_length=100, max_length=256)
    calibrate: str = Field(min_length=100, max_length=256)

    # token length 제한
    @validator("situation", pre=True)
    def validate_situation_length(cls, v):
        if len(v) < 100 or len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v

    @validator("task", pre=True)
    def validate_task_length(cls, v):
        if len(v) < 100 or len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v

    @validator("intent", pre=True)
    def validate_intent_length(cls, v):
        if len(v) < 100 or len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v

    @validator("concern", pre=True)
    def validate_concern_length(cls, v):
        if len(v) < 100 or len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v

    @validator("calibrate", pre=True)
    def validate_calibrate_length(cls, v):
        if len(v) < 100 or len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v


class Mentor_Detail(BaseModel):
    mentor_name: str = Field(min_length=1, max_length=100)
    mentor_field: int
    mentor_sticc: STICC

    @validator("mentor_name", pre=True)
    def validate_calibrate_length(cls, v):
        if len(v) < 1 or len(v) > 100:
            raise AuthenticationFailedException(
                status_code=413, message="입력 양식을 지켜주세요"
            )
        return v
