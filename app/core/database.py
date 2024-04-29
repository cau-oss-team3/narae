import logging
from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.settings import settings


logger = logging.getLogger('database')

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'ix': 'ix_%(table_name)s_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_to_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)

asyncio_engine = create_async_engine(settings.database.database_url, echo=settings.debug)
AsyncSessionFactory = async_sessionmaker(
    asyncio_engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)

# NOTE: Sync version
# engine = create_engine(settings.database.database_url)
# SyncBase = declarative_base()
# SyncBase.metadata.create_all(bind=engine)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        logger.debug(f"ASYNC Pool: {asyncio_engine.pool.status()}")
        yield session


Session = Annotated[AsyncSession, Depends(get_async_session)]
