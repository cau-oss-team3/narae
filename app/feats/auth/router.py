from fastapi import APIRouter, Depends, Header

from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.depends import get_user_service
from app.feats.auth.service import UserService
from app.feats.auth.schemas import UserLoginRequest, UserLoginResponse


# {"token" : user.id} 으로 dict를 리스트 안에 넣음
active_user = []

router = APIRouter(prefix="/auth", tags=["auth"])


# 로그인이자 회원가입
@router.post("/login", response_model=UserLoginResponse)
async def login(input_user: UserLoginRequest, user_service: UserService = Depends(get_user_service)):
    user = await user_service.login_user(input_user.email, input_user.password.get_secret_value())

    token = user_service.generate_token(user)
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
