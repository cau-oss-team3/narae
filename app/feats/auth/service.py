import bcrypt
from datetime import datetime, timedelta
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt

from app.settings import settings
from app.core.exceptions import AuthenticationFailedException
from .models import User


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def generate_token(self, user: User):
        data = {
            "sub": user.email,
            "exp": datetime.now()
            + timedelta(minutes=settings.access_token_expire_minutes),
        }

        return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

    async def find_user_by_email(self, email: str):
        query = select(User).filter(User.email == email)
        result = await self.db.execute(query)
        return result.scalar()

    async def create_new_user(self, email: str, password: str):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User(email=email, password=hashed_password.decode())
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def login_user(self, email: str, password: str):
        user = await self.find_user_by_email(email)
        if user is None:
            """유저가 존재하지 않을 때"""
            user = await self.create_new_user(email, password)
        elif not bcrypt.checkpw(password.encode(), user.password.encode()):
            """비밀번호가 일치하지 않을 때"""
            raise AuthenticationFailedException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="틀린 비밀번호 혹은 입력 양식이 맞지 않음",
            )
        """로그인 성공 시 유저 반환"""
        return user
