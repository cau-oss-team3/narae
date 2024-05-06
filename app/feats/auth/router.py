from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_session
from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.models import User
from app.feats.auth.schemas import (
    TokenResponse,
    UserLoginRequest,
    UserLoginResponse,
    Token,
)
from app.feats.auth.service import (
    generate_token,
    get_current_token_count,
    get_current_user,
    increase_token_count,
    login_user,
)
from app.settings import settings


# {"token" : user.id} 으로 dict를 리스트 안에 넣음
active_user = []

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
) -> Token:
    user = await login_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = generate_token(user)
    return Token(access_token=token, token_type="bearer")


# 로그인이자 회원가입
@router.post("/login", response_model=UserLoginResponse)
async def login(input_user: UserLoginRequest):
    user = await login_user(input_user.email, input_user.password.get_secret_value())

    token = generate_token(user)
    active_user.append({token: user.id})

    return UserLoginResponse(isSuccess=True, token=token)


# 로그아웃
@router.post(path="/logout")
async def logout(token: str = Header(default=None, convert_underscores=False)):
    count = False
    print(token, type(token))
    for i in range(len(active_user)):
        if list(active_user[i].keys())[0] == token:
            del active_user[i]
            count = True
            break

    if count:
        return {"isSuccess": True}
    else:
        raise AuthenticationFailedException(
            status_code=412, message="존재하지 않는 토큰"
        )


@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_user),
):
    """
    Get current user
    """
    del current_user.password
    return current_user


@router.get("/me/daily-limit")
async def remaining_daily_limit(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> TokenResponse:
    """
    Get the number of remaining daily tokens
    """

    used_tokens = await get_current_token_count(db, current_user.id)
    remaining_tokens = settings.daily_token_limit - used_tokens

    return TokenResponse(remaining_tokens=remaining_tokens)

@router.post("/me/daily-limit")
async def use_daily_limit(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
) -> TokenResponse:
    """
    Use one of the daily tokens
    """

    used_tokens = await get_current_token_count(db, current_user.id)
    remaining_tokens = settings.daily_token_limit - used_tokens
    if remaining_tokens < 0:
        raise AuthenticationFailedException(
            status_code=412, message="이미 토큰을 모두 사용하였습니다."
        )

    await increase_token_count(db, current_user.id)
    return TokenResponse(remaining_tokens=remaining_tokens - 1)