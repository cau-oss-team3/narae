from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.settings import settings
from app.core.logger import set_logging
from app.middleware import apply_middleware
from app.routers import apply_routes

from app.core.database import Base, asyncio_engine  # Ensure you import your Base and async engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    set_logging(settings.base_dir)

    # Asynchronously create database tables at startup
    async with asyncio_engine.begin() as conn:
        # Create all tables stored in your metadata
        await conn.run_sync(Base.metadata.create_all)

    yield

    # async with asyncio_engine.begin() as conn:
    #     # WARN: Drop tables here if needed when app shuts down
    #     # await conn.run_sync(Base.metadata.drop_all)


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url='/docs',
        openapi_url='/docs.json',
    )

    app = apply_middleware(app)
    app = apply_routes(app)
    # use_route_names_as_operation_ids(app)

    return app