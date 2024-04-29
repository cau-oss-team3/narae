from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.core.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Item
from .schemas import ItemCreate

router = APIRouter(prefix='/items', tags=['Items'])


@router.get(
    "/",
    description="Read items",
    response_model=List[ItemCreate]
)
async def read_items(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    # items = session.query(Item).offset(skip).limit(limit).all()
    # items = session.query(Item).all()

    async with session:
        query = select(Item).offset(skip).limit(limit)
        result = await session.execute(query)
        items = result.scalars().all()
        return items

@router.get("/{item_id}")
def read_item(item_id: int, db = Depends(get_async_session)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item}

@router.post("")
def create_item(item: ItemCreate, db = Depends(get_async_session)):
    db_item = Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"item": db_item}
