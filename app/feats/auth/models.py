from sqlalchemy import Column, String
from app.core.database import Base


# user table 생성 (id는 자동으로 붙음, primary key = id)
class User(Base):
    __tablename__ = "User"
    email = Column(String(120), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)
