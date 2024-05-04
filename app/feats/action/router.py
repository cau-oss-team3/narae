from fastapi import APIRouter, Header
from typing import Optional

from .schemas import Chat_Data


router = APIRouter(prefix="/action", tags=["action"])


@router.get("/recommend/{id}")
async def recommendAction(id: str, Authorization: str = Header(default=None)):

    # TODO chat data 받아오기
    dummy_chat_data = Chat_Data()
    dummy_chat_data.seq = 0
    dummy_chat_data.type = 1
    dummy_chat_data.chat_data = "chat data"
    dummy_chat_data.candidate = ["candidate", "example"]
    dummy_chat_data.timestamp = 234
    return {"isSuccess": True, "chat_data": dummy_chat_data}


@router.get("/crrent/{id}")
async def currentAction(id: str, Authorization: str = Header(default=None)):

    # TODO 현재 수락한 Action list 조회하기

    return {"isSuccess": True, "action_list": ["actionlist", "example"]}


@router.post("/accept")
async def acceptAction(
    id: str,
    is_accept: bool,
    action: Optional[str] = None,
    Authorization: str = Header(default=None),
):

    # TODO API 설계 참고해서 기능 구현하기
    dummy_chat_data = Chat_Data()
    dummy_chat_data.seq = 0
    dummy_chat_data.type = 1
    dummy_chat_data.chat_data = "chat data"
    dummy_chat_data.candidate = ["candidate", "example"]
    dummy_chat_data.timestamp = 234
    return {"isSuccess": True, "chat_data": dummy_chat_data}


@router.post("/result")
async def postActionResult(
    id: str,
    reslt_code: int,
    action: str,
    chat_data: str,
    Authorization: str = Header(default=None),
):

    # TODO API 설계 참고해서 기능 구현하기
    dummy_chat_data = Chat_Data()
    dummy_chat_data.seq = 0
    dummy_chat_data.type = 1
    dummy_chat_data.chat_data = "chat data"
    dummy_chat_data.candidate = ["candidate", "example"]
    dummy_chat_data.timestamp = 234
    return {"isSuccess": True, "chat_data": dummy_chat_data}
