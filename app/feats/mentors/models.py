from sqlalchemy import Column, String, Integer
from app.core.database import Base


# mentor table 생성 (primary key = id)
class Mentor(Base):
    __tablename__ = "Mentor"
    id = Column(String(50), primary_key=True, index=True, nullable=False)
    mentor_name = Column(String(45), nullable=False, unique=True)
    mentor_field = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    situation = Column(String(45), nullable=False)
    task = Column(String(45), nullable=False)
    intent = Column(String(45), nullable=False)
    concern = Column(String(45), nullable=False)
    calibrate = Column(String(45), nullable=False)
