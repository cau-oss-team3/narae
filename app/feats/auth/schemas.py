from pydantic import BaseModel, EmailStr, validator, ValidationError,Field
from app.core.exceptions import AuthenticationFailedException
import re
#요런 느낌으로 베이스모델 모으기
class UserInput(BaseModel):
    email: str
    password : str

    @validator('email')
    def validate_email(cls, v):
        # v에는 해당 이메일 필드에 대한 값이 담겨 있습니다.
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            return v
        else:
            raise AuthenticationFailedException(status_code=401, message="입력 양식을 지켜주세요")
#비어있는지 검사
    @validator('email', 'password')
    def check_empty(cls, v):
        if not v or v.isspace():
            raise AuthenticationFailedException(status_code=401, message="입력 양식을 지켜주세요")
        return v
    
    
# class Token(BaseModel):
#     access_token: str
#     token_type: str
#     email: str