from datetime import datetime
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    BigInteger,
)

from app.core.database import Base


class Feedback(Base):
    __tablename__ = "Feedback"
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("Mentor2.id"), nullable=False)
    type = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        BigInteger,
        default=lambda: int(datetime.now().timestamp() * 1000),
        nullable=False,
    )
    context = Column(Text, nullable=False)
