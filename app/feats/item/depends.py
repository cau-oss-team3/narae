from app.core.database import Session
from app.feats.item.schemas import ItemCreate


async def get_db() -> Session:
    async with Session() as session:
        yield session