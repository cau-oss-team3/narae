from pydantic import BaseModel, validator
from app.core.exceptions import AuthenticationFailedException
import re


class UserInput(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            return v
        else:
            raise AuthenticationFailedException(
                status_code=401, message="입력 양식이 맞지 않음"
            )

    # 비어있는지 검사
    @validator("email", "password")
    def check_empty(cls, v):
        if not v or v.isspace():
            raise AuthenticationFailedException(
                status_code=401, message="입력 양식이 맞지 않음"
            )
        return v
