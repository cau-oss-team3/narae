from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
    Boolean,
    BigInteger,
)

from app.core.database import Base


class ChatHistory(Base):
    __tablename__ = "ChatHistory"
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("Mentor2.id"), nullable=False)
    type = Column(Integer, nullable=False)
    chat_data = Column(Text, nullable=False)
    visibility = Column(Boolean, nullable=False)
    timestamp = Column(BigInteger, nullable=False)
    created_at = Column(
        BigInteger,
        default=lambda: int(datetime.now().timestamp() * 1000),
        nullable=False,
    )
