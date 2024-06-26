from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, Text, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base


class Mentor2(Base):
    __tablename__ = "Mentor2"
    mentor_name = Column(String(45), nullable=False)
    mentor_field = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    user = relationship("User", back_populates="mentors")

    situation = Column(String(256), nullable=False)
    task = Column(String(256), nullable=False)
    intent = Column(String(256), nullable=False)
    concern = Column(String(256), nullable=False)
    calibrate = Column(String(256), nullable=False)

    curriculum = Column(Text)
    curriculum_phase = Column(Text)

    actions = relationship("Action", back_populates="mentor")
    chat_histories = relationship("ChatHistory", back_populates="mentor", cascade="all, delete-orphan")


class Action(Base):
    __tablename__ = "Action"
    mentor_id = Column(Integer, ForeignKey('Mentor2.id'), nullable=True)
    mentor = relationship("Mentor2", back_populates="actions")

    action = Column(Text, nullable=False)
    feedback = Column(Text, nullable=False, default="")
    is_active = Column(Boolean, nullable=False, default=False)
    is_done = Column(Boolean, nullable=False, default=False)

    created_at = Column(
        BigInteger,
        default=lambda: int(datetime.now().timestamp() * 1000),
        nullable=False,
    )
    updated_at = Column(
        BigInteger,
        default=lambda: int(datetime.now().timestamp() * 1000),
        onupdate=lambda: int(datetime.now().timestamp() * 1000),
        nullable=False,
    )
