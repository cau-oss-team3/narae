import bcrypt
from typing import Annotated
from datetime import date, datetime, timedelta
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from app.core.database import get_async_session
from app.feats.auth.schemas import TokenData
from app.settings import settings
from app.core.exceptions import AuthenticationFailedException
from app.feats.auth.models import Limit, User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
credentials_exception = AuthenticationFailedException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    message="유효하지 않은 정보입니다.",
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception

        token_data = TokenData(email=user_email)
    except JWTError:
        raise credentials_exception

    user = await find_user_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception

    return user


def generate_token(user: User):
    data = {
        "sub": user.email,
        "exp": datetime.now() + timedelta(minutes=settings.access_token_expire_minutes),
    }

    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)


async def find_user_by_email(db: AsyncSession, email: str) -> User:
    query = select(User).filter(User.email == email)
    result = await db.execute(query)
    return result.scalar()


async def create_new_user(db: AsyncSession, email: str, password: str):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User(email=email, password=hashed_password.decode())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def login_user(db: AsyncSession, email: str, password: str):
    user = await find_user_by_email(db, email)
    if user is None:
        """유저가 존재하지 않을 때"""
        user = await create_new_user(db, email, password)
    elif not bcrypt.checkpw(password.encode(), user.password.encode()):
        """비밀번호가 일치하지 않을 때"""
        raise credentials_exception
    """로그인 성공 시 유저 반환"""
    return user


async def get_current_token_count(db: AsyncSession, user_id: int):
    # You need to adjust the database session according to your setup (e.g., using dependency injection)
    current_date = date.today()
    limit_entry = await db.execute(
        select(Limit).filter(Limit.user_id == user_id, Limit.request_date == current_date)
    )
    limit_entry = limit_entry.scalar()
    if limit_entry:
        return limit_entry.request_count

    db.add(Limit(user_id=user_id, request_date=current_date, request_count=0))
    await db.commit()

    return 0


async def increase_token_count(db: AsyncSession, user_id: int):
    current_date = date.today()
    limit_entry = await db.execute(
        select(Limit).filter(Limit.user_id == user_id, Limit.request_date == current_date)
    )
    limit_entry = limit_entry.scalar()
    if limit_entry:
        limit_entry.request_count += 1
        await db.commit()
        await db.refresh(limit_entry)

        return limit_entry.request_count

    db.add(Limit(user_id=user_id, request_date=current_date, request_count=1))
    await db.commit()
    await db.refresh(limit_entry)

    return limit_entry.request_count
