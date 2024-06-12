from pydantic import BaseModel, field_validator, Field

from app.core.exceptions import AuthenticationFailedException

MIN_LENGTH = 1


class FeedbackDTO(BaseModel):
    type: int
    rate: int = Field(ge=0, le=5)
    content: str
    context: str = ""

    @field_validator("content", mode="before")
    @classmethod
    def validate_content_length(cls, v):
        if len(v) < MIN_LENGTH:
            raise AuthenticationFailedException(
                status_code=413, message="토큰 length가 작음"
            )
        return v
