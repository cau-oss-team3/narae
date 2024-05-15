from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Integer,
    PrimaryKeyConstraint,
    Text,
    Boolean,
)

from app.core.database import Base


class ChatHistory(Base):
    __tablename__ = "ChatHistory"
    user_id = Column(Integer, ForeignKey("User.id"), nullable=False)
    mentor_id = Column(Integer, ForeignKey("Mentor2.id"), nullable=False)
    seq = Column(Integer, nullable=False)
    type = Column(Integer, nullable=False)
    chat_data = Column(Text, nullable=False)
    visibility = Column(Boolean, nullable=False)
    candidates = Column(String, nullable=False)  # string 그대로 받아서 리스트를 파싱
