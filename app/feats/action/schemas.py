from pydantic import BaseModel
from typing import Optional


class Chat_Data(BaseModel):
    seq: int
    type: int
    chat_data: str
    candidate: list
    timestamp: int


class Request_Chat_Data(BaseModel):
    type: int
    chat_data: Optional[str] = None
