from pydantic import BaseModel
from typing import Optional


class Response_Chat_Data(BaseModel):
    seq: int
    type: int
    chat_data: str
    candidate: list
    timestamp: int


class Request_Chat_Data(BaseModel):
    type: int
    chat_data: Optional[str] = None


class Systm_Request_Chat(BaseModel):
    type: int
    subtype: int
    chat_data: Optional[str] = None


class Systm_Response_Chat(BaseModel):
    type: int
    subtype: int
    chat_data: Optional[str] = None
