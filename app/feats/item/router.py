from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Item
from .schemas import ItemCreate

router = APIRouter(prefix="/items", tags=["Items"])


@router.get("/", description="Read items", response_model=List[ItemCreate])
async def read_items(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
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


@router.get("/{item_id}")
async def read_item(item_id: int, session: AsyncSession = Depends(get_async_session)):
    async with session:
        query = select(Item).filter(Item.id == item_id)
        result = await session.execute(query)
        item = result.scalar()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
