from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.core.exceptions import AuthenticationFailedException

MIN_LENGTH = 1


class ChatRequest(BaseModel):
    """
    {
        "seq": "int",
        "chat_type": "Chat Type Code <int>",
        "chat_data": "string",
        "candidates": [ "string" ],
        "timestamp": "UnixTime Milliseconds <int>",
        "visibility": "Boolean",
    }
    """

    seq: int = 0
    chat_type: int = Field(ge=0, le=8)
    chat_data: str = ""
    candidates: list[str] = []
    timestamp: int = int(datetime.now().timestamp() * 1000)
    visibility: bool = True

    def to_chat_history(self):
        return Chatting(
            seq=self.seq,
            chat_type=self.chat_type,
            chat_data=self.chat_data,
            timestamp=self.timestamp,
            visibility=self.visibility,
        )


class MentorInfoResponse(BaseModel):
    """
    seq: 0,
    chat_type: 2,
    chat_data: "멘토 정보 출력",
    candidates: [],
    timestamp: new Date().getTime(),
    visibility: true,
    """

    seq: int = 0
    chat_type: int = 2
    chat_data: str = ""
    candidates: list[str] = []
    timestamp: int = int(datetime.now().timestamp() * 1000)
    visibility: bool = True


class MentorChatResponse(BaseModel):
    """
    seq: 2,
    chat_type: 1,
    chat_data: "멘토 발화 테스트 1",
    candidates: [],
    timestamp: new Date().getTime(),
    visibility: true,
    """

    seq: int = 0
    chat_type: int = 1
    chat_data: str = ""
    candidates: list[str] = []
    timestamp: int = int(datetime.now().timestamp() * 1000)
    visibility: bool = True

    def to_chat_history(self):
        return Chatting(
            seq=self.seq,
            chat_type=self.chat_type,
            chat_data=self.chat_data,
            timestamp=self.timestamp,
            visibility=self.visibility,
        )


class ChatResponseFail(BaseModel):
    isSuccess: bool = False
    err: str


""" example data
[
    {
        seq: 0,
        chat_type: 2,
        chat_data: "멘토 정보 출력",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 1,
        chat_type: 3,
        chat_data: "이전 대화 요약",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 2,
        chat_type: 1,
        chat_data: "멘토 발화 테스트 1",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 3,
        chat_type: 0,
        chat_data: "유저 발화 테스트 1",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 4,
        chat_type: 4,
        chat_data: "Action 수락 요청",
        candidates: ["Action 1", "Action 2", "Action 3"],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 5,
        chat_type: 5,
        chat_data: "Action 결과 제출 요청",
        candidates: ["Action 1"], // 무조건 0번 index 사용
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 6,
        chat_type: 1,
        chat_data: "멘토 발화 테스트 2",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
];
"""


class Chatting(BaseModel):
    seq: int = 0  # id
    chat_type: int = Field(ge=0, le=8)
    chat_data: str = ""
    timestamp: int
    visibility: bool = True
