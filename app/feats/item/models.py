from sqlalchemy import Column, String
from app.core.database import Base


class Item(Base):
    name = Column(String(255))
    description = Column(String(255))
