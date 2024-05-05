from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt

from app.core.exceptions import AuthenticationFailedException

from app.settings import settings
from app.core.database import get_async_session

from .models import User
from .schemas import UserInput

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

# {"token" : user.id} 으로 dict를 리스트 안에 넣음
login_user = []

router = APIRouter(prefix="/auth", tags=["auth"])


# 로그인이자 회원가입
@router.post("/login")
async def login(input_user: UserInput, db: AsyncSession = Depends(get_async_session)):
    async with db:
        query = select(User).filter(input_user.email == User.email)
        result = await db.execute(query)
        found_user = result.scalar()

    if found_user is None:
        new_user = User(email=input_user.email, password=input_user.password)
        async with db:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
        found_user = new_user
    elif input_user.password != found_user.password:
        raise AuthenticationFailedException(
            status_code=401, message="틀린 비밀번호 혹은 입력 양식이 맞지 않음"
        )

    # make access token(Authorization)
    data = {
        "sub": found_user.email,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    login_user.append({token: found_user.id})
    return {"isSuccess": True, "token": token}


# 로그아웃
@router.post(path="/logout")
async def logout(token: str = Header(default=None, convert_underscores=False)):
    count = False
    print(token, type(token))
    for i in range(len(login_user)):
        if list(login_user[i].keys())[0] == token:
            del login_user[i]
            count = True
            break

    if count:
        return {"isSuccess": True}
    else:
        raise AuthenticationFailedException(
            status_code=412, message="존재하지 않는 토큰"
        )
