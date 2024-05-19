from pydantic import BaseModel, field_validator
from app.core.exceptions import AuthenticationFailedException

MIN_LENGTH = 1


class Feedback_Recieved(BaseModel):
    type: int
    content: str
    context: str

    @field_validator("content", mode="before")
    @classmethod
    def validate_content_length(cls, v):
        if len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 작음"
            )
        return v

    @field_validator("context", mode="before")
    @classmethod
    def validate_context_length(cls, v):
        if len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 작음"
            )
        return v
