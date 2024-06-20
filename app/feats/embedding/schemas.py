from typing import List

from pydantic import BaseModel, Field


class CreateDocumentRequest(BaseModel):
    field: int = Field(ge=0, le=2)
    document: str = "This is a document."


class CreateVectorItemRequest(BaseModel):
    name: str
    embedding: List[float] = [1.0, 2.0, 3.0]


class PatchVectorItemRequest(BaseModel):
    embedding: List[float] = [1.0, 2.0, 3.0]