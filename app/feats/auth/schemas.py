from pydantic import BaseModel, EmailStr, validator
from fastapi import  HTTPException
from typing import Optional


#요런 느낌으로 베이스모델 모으기
class UserInput(BaseModel):
    email: EmailStr
    password : str

#양식 검사, 이메일 양식 검사
    @validator('email', 'password')
    def check_empty(cls, v):
        if not v or v.isspace():
            raise HTTPException(status_code=422, detail="필수 항목을 입력해주세요.")
        return v
    
class Token(BaseModel):
    access_token: str
    token_type: str
    email: EmailStr