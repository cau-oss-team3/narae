from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user
from app.feats.feedback.schemas import FeedbackDTO
from app.feats.feedback.service import create_feedback
from app.settings import settings

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/{mentor_id}")
async def createFeedback(
    mentor_id: int,
    feedbackDTO: FeedbackDTO,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):
    if settings.env == "prod":
        return {"message": "프로덕션 환경에서는 사용할 수 없습니다."}

    await create_feedback(current_user.id, mentor_id, feedbackDTO, db)

    return {"isSuccess": True}
