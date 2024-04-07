from sqlalchemy import Column, Integer, String
from app.database import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))