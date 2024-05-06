
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.auth.service import UserService


def get_user_service(db: AsyncSession = Depends(get_async_session)):
    return UserService(db)
