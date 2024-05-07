import re

from pydantic import field_validator, BaseModel, SecretStr

from app.core.exceptions import AuthenticationFailedException

class TokenInJson(BaseModel):
    isSuccess: bool = True
    access_token: str
    token_type: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserLoginRequest(BaseModel):
    email: str
    password: SecretStr

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            return v
        else:
            raise AuthenticationFailedException(
                status_code=401, message="유요하지 않은 이메일 형식입니다."
            )

    # 비어있는지 검사
    @field_validator("email", "password")
    @classmethod
    def check_empty(cls, v):
        if not v:
            raise AuthenticationFailedException(
                status_code=401, message="이메일 혹은 비밀번호가 비어있습니다."
            )

        return v


class UserLoginResponse(BaseModel):
    isSuccess: bool
    token: str


class TokenResponse(BaseModel):
    remaining_tokens: int
