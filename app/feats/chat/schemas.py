from datetime import datetime
from pydantic import BaseModel, Field


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
    timestamp: int = datetime.now().timestamp()
    visibility: bool = True

class MentorResponseSuccess(BaseModel):
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
    timestamp: int = datetime.now().timestamp()
    visibility: bool = True

class ChatResponseFail(BaseModel):
    isSuccess: bool = False
    err: str


""" example data
[
    {
        seq: 0,
        type: 2,
        chat_data: "멘토 정보 출력",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 1,
        type: 3,
        chat_data: "이전 대화 요약",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 2,
        type: 1,
        chat_data: "멘토 발화 테스트 1",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 3,
        type: 0,
        chat_data: "유저 발화 테스트 1",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 4,
        type: 4,
        chat_data: "Action 수락 요청",
        candidates: ["Action 1", "Action 2", "Action 3"],
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 5,
        type: 5,
        chat_data: "Action 결과 제출 요청",
        candidates: ["Action 1"], // 무조건 0번 index 사용
        timestamp: new Date().getTime(),
        visibility: true,
    },
    {
        seq: 6,
        type: 1,
        chat_data: "멘토 발화 테스트 2",
        candidates: [],
        timestamp: new Date().getTime(),
        visibility: true,
    },
];
"""