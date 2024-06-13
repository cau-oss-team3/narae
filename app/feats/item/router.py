import logging
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.websocket import WebsocketConnectionManager, get_websocket_manager
from app.feats.item.depends import get_cookie_or_token, test_page
from .models import Item
from .schemas import ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])


logger = logging.getLogger("fastapi")

@router.get("/", description="Read items", response_model=List[ItemCreate])
async def read_items(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    logger.info(f"Reading items from {skip} to {skip + limit}")
    async with session:
        query = select(Item).offset(skip).limit(limit)
        result = await session.execute(query)
        items = result.scalars().all()
        return items


@router.post("/")
async def create_item(
    item: ItemCreate, session: AsyncSession = Depends(get_async_session)
):
    async with session:
        new_item = Item(**item.model_dump())
        session.add(new_item)
        await session.commit()
        return new_item


@router.get("/ws")
async def get_test_page():
    return HTMLResponse(content=test_page, status_code=200)


@router.get("/{item_id}")
async def read_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    async with session:
        query = select(Item).filter(Item.id == item_id)
        result = await session.execute(query)
        item = result.scalar()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item


@router.websocket("/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
    manager: WebsocketConnectionManager = Depends(get_websocket_manager),
):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.send_direct_message(
            f"Session cookie or query token value is: {cookie_or_token}", websocket
        )
        if q is not None:
            await manager.send_direct_message(f"Query parameter q is: {q}", websocket)
        await manager.send_direct_message(
            f"Message text was: {data}, for item ID: {item_id}", websocket
        )
