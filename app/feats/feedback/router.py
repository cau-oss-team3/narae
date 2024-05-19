from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.feats.auth.models import User
from app.feats.auth.service import get_current_user

from app.feats.feedback.schemas import Feedback_Recieved
from app.feats.feedback.service import create_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/{mentor_id}")
async def createFeedback(
    mentor_id: int,
    feedback_recieved: Feedback_Recieved,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session),
):

    await create_feedback(current_user.id, mentor_id, feedback_recieved, db)

    return {"isSuccess": True}