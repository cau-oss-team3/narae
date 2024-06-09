from datetime import datetime

from sqlalchemy import Column, ForeignKey, String, Integer, Text, BigInteger
from sqlalchemy.orm import relationship
from typing_extensions import deprecated

from app.core.database import Base


class Mentor(Base):
    __tablename__ = "Mentor"
    id = Column(String(100), primary_key=True, index=True, nullable=False)
    mentor_name = Column(String(45), nullable=False, unique=True)
    mentor_field = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    situation = Column(String(256), nullable=False)
    task = Column(String(256), nullable=False)
    intent = Column(String(256), nullable=False)
    concern = Column(String(256), nullable=False)
    calibrate = Column(String(256), nullable=False)


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

    action_id = Column(Integer, ForeignKey("Action.id"))
    actions = relationship("Action", back_populates="mentor")


class Action(Base):
    __tablename__ = "Action"
    mentor_id = Column(Integer, ForeignKey('Mentor2.id'), nullable=False)
    mentor = relationship("Mentor2", back_populates="actions")

    action = Column(Text, nullable=False)
    is_active = Column(Integer, nullable=False)
    
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
