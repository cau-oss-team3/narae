from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


# mentor table 생성 (primary key = id)
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

    user_id = Column(Integer, nullable=False)

    situation = Column(String(256), nullable=False)
    task = Column(String(256), nullable=False)
    intent = Column(String(256), nullable=False)
    concern = Column(String(256), nullable=False)
    calibrate = Column(String(256), nullable=False)

    user = relationship("User", back_populates="limits")
