from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    {
        "seq": "int",
        "type": "Chat Type Code <int>",
        "chat_data": "string",
        "mentor": "int",
        "timestamp": "UnixTime Milliseconds <int>",
        "visibility": "Boolean"
    }

    ex)
    {
        "seq": 0,
        "type": 1,
        "chat_data": "Hello",
        "mentor": 1,
        "timestamp": 1618227561,
        "visibility": true
    }
    """

    seq: int = 0
    chat_type: int = Field(ge=0, le=8)
    chat_data: str = ""
    mentor: int = -1
    timestamp: int = datetime.now().timestamp()
    visibility: bool = True

class ChatResponseSuccess(BaseModel):
    isSuccess: bool = True
    chat_data: str

class ChatResponseFail(BaseModel):
    isSuccess: bool = False
    err: str