from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Column, Text, Integer

from app.core.database import Base


class EmbeddingItem(Base):
    name = Column(String(255))
    embedding = Column(Vector(3))


class DocumentChunk(Base):
    field = Column(Integer)  # 0: backend, 1: frontend, 2: fullstack
    document = Column(Text)  # original text
    embedding = Column(Vector(1536))  # text-embedding-3-small dimension size
