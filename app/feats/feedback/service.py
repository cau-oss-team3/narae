from sqlalchemy.ext.asyncio import AsyncSession

from app.feats.feedback.models import Feedback
from app.feats.feedback.schemas import FeedbackDTO


async def create_feedback(
    user_id: int, mentor_id: int, feedbackDTO: FeedbackDTO, db: AsyncSession
):
    new_feedback = Feedback(
        user_id=user_id,
        mentor_id=mentor_id,
        type=feedbackDTO.type,
        rate=feedbackDTO.rate,
        content=feedbackDTO.content,
        context=feedbackDTO.context,
    )

    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
