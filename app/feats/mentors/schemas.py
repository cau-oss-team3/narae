from pydantic import field_validator, BaseModel, Field
from app.core.exceptions import AuthenticationFailedException

MIN_LENGTH = 1
MAX_LENGTH = 256

class STICC(BaseModel):
    situation: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    task: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    intent: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    concern: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    calibrate: str = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)

    # token length 제한
    @field_validator("situation", mode="before")
    @classmethod
    def validate_situation_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("task", mode="before")
    @classmethod
    def validate_task_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("intent", mode="before")
    @classmethod
    def validate_intent_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("concern", mode="before")
    @classmethod
    def validate_concern_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v

    @field_validator("calibrate", mode="before")
    @classmethod
    def validate_calibrate_length(cls, v):
        if len(v) > MAX_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 큼"
            )
        elif len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 너무 작음"
            )
        return v


class MentorDTO(BaseModel):
    mentor_name: str = Field(min_length=1, max_length=45)
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
