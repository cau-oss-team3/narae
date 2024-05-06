from pydantic import field_validator, BaseModel, Field
from app.core.exceptions import AuthenticationFailedException


class STICC(BaseModel):
    situation: str = Field(min_length=100, max_length=256)
    task: str = Field(min_length=100, max_length=256)
    intent: str = Field(min_length=100, max_length=256)
    concern: str = Field(min_length=100, max_length=256)
    calibrate: str = Field(min_length=100, max_length=256)

    # token length 제한
    @field_validator("situation", mode="before")
    @classmethod
    def validate_situation_length(cls, v):
        if len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 100:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("task", mode="before")
    @classmethod
    def validate_task_length(cls, v):
        if len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 100:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("intent", mode="before")
    @classmethod
    def validate_intent_length(cls, v):
        if len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 100:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("concern", mode="before")
    @classmethod
    def validate_concern_length(cls, v):
        if len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 100:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("calibrate", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > 256:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 100:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v


class Mentor_Detail(BaseModel):
    mentor_name: str = Field(min_length=1, max_length=100)
    mentor_field: int
    mentor_sticc: STICC

    @field_validator("mentor_name", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > 45:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < 1:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v
