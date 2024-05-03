from fastapi import APIRouter, Header
from typing import Optional

from .schemas import Chat_Data


router = APIRouter(prefix="/action", tags=["action"])


@router.get("/recommend/{id}")
async def recommendAction(id: str, access_token: str = Header(default=None)):

    # TODO action_list 받아오기

    return {"isSuccess": True, "action-list": '[ "string" ]'}


@router.get("/crrent/{id}")
async def currentAction(id: str, access_token: str = Header(default=None)):

    # TODO 현재 수락한 Action list 조회하기

    return {"isSuccess": True, "action-list": '[ "string" ]'}


@router.post("/accept")
async def acceptAction(
    id: str,
    is_accept: bool,
    action: Optional[str] = None,
    access_token: str = Header(default=None),
):

    # TODO API 설계 참고해서 기능 구현하기

    return {"isSuccess": True, "chat-data": "Chat Data <object>"}


@router.post("/result")
async def postActionResult(
    id: str,
    reslt_code: int,
    action: str,
    chat_data: str,
    access_token: str = Header(default=None),
):

    # TODO API 설계 참고해서 기능 구현하기

    return {"isSuccess": True, "chat-data": "Chat Data <object>"}
