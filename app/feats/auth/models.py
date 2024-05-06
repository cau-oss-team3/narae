from datetime import datetime
from sqlalchemy import Column, DateTime, String
from app.core.database import Base


# user table 생성 (id는 자동으로 붙음, primary key = id)
class User(Base):
    __tablename__ = "User"
    email = Column(String(120), unique=True, index=True, nullable=False, autoincrement=True)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
