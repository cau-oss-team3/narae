from fastapi import APIRouter,Depends, HTTPException, Header, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from app.settings import settings
from app.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from datetime import timedelta, datetime
from sqlalchemy import select


from .models import User, PasswordException
from .schemas import UserInput, Token

#uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm

#{"access_token" : user.id} 으로 dict를 리스트 안에 넣을거임
login_user = []

router = APIRouter(prefix="/auth", tags=["auth"])

#TODO 그냥 custom error 가 전부... app임 fastapi 내부에서 발생시키는 500 에러는 처리가 불가능(일단 당장 서치는 app에서 처리하는거임)

#로그인이자 회원가입 // TODO 에러처리해주기
@router.post("/login")
async def login(input_user : UserInput, db: AsyncSession = Depends(get_async_session)):
    
    async with db:
         query = select(User).filter(input_user.email==User.email)
         result = await db.execute(query)
         found_user = result.scalar()

    if found_user is None:
         new_user = User(email=input_user.email, password = input_user.password)
         async with db:
            db.add(new_user)
            await db.commit()  
            await db.refresh(new_user)
         found_user = new_user
    elif input_user.password!=found_user.password:
        raise HTTPException( #TODO 양식 다름
        status_code=401,
        detail={"isSuccess" : False, "err": "Incorrect username or password"}
        )
     

    # make access token
    data = {
        "sub": found_user.email,
        "exp": datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    login_user.append({access_token : found_user.id})
    return {
        "isSuccess": True,
        "token" : access_token
    }

#for Check logout
@router.get(path="/getaccesstoken")
async def logout():    
    return login_user[0]


#TODO return 값 바꾸기
@router.post(path="/logout")
async def logout(access_token : str = Header(default=None)):
    for i in range(len(login_user)):
        if(list(login_user[i].keys())[0]==access_token):
            del login_user[i]
            break
    
    return {"isSuccess": True}


