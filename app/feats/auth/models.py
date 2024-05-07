from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class Limit(Base):
    __tablename__ = "Limit"
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    request_date = Column(Date, default=datetime.utcnow, nullable=False)
    request_count = Column(Integer, default=0, nullable=False)

    # Optional: Relationship to User table to access user info easily
    user = relationship("User", back_populates="limits")


# user table 생성 (id는 자동으로 붙음, primary key = id)
class User(Base):
    __tablename__ = "User"
    email = Column(String(120), unique=True, index=True, nullable=False, autoincrement=True)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    limits = relationship("Limit", back_populates="user", cascade="all, delete-orphan")
    mentors = relationship("Mentor", back_populates="user", cascade="all, delete-orphan")
