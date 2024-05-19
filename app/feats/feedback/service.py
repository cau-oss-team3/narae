from sqlalchemy.ext.asyncio import AsyncSession

from app.feats.feedback.models import Feedback
from app.feats.feedback.schemas import Feedback_Recieved


async def create_feedback(
    user_id: int, mentor_id: int, feedback_recieved: Feedback_Recieved, db: AsyncSession
):
    new_feedback = Feedback(
        user_id=user_id,
        mentor_id=mentor_id,
        type=feedback_recieved.type,
        content=feedback_recieved.content,
        context=feedback_recieved.context,
    )

    db.add(new_feedback)
    await db.commit()
    await db.refresh(new_feedback)
