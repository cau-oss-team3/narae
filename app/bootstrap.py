import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from alembic.config import Config
from alembic import command

from app.core.exceptions import CustomHTTPException, unhandled_custom_exception_handler
from app.settings import settings
from app.core.database import asyncio_engine
from app.core.logger import set_logging
from app.middleware import apply_middleware
from app.routers import apply_routes


def run_migrations(connection, init_location, script_location: str, dsn: str) -> None:
    print(f"INFO:     Running DB migrations in {script_location}")
    alembic_cfg = Config(init_location)
    alembic_cfg.attributes["connection"] = connection
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    alembic_cfg.set_main_option("script_location", script_location)

    # command.stamp(alembic_cfg, 'head')
    command.upgrade(alembic_cfg, "head")

    print("INFO:     DB migrations completed.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # DB Migrations
    async with asyncio_engine.begin() as conn:
        await conn.run_sync(
            run_migrations,
            settings.alembic_ini,
            settings.alembic_script_location,
            settings.database.database_url,
        )

    # Set logging configuration
    set_logging(settings.base_dir)
    logger = logging.getLogger("fastapi")

    logger.info("Application started.")

    yield

    logger.info("Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        docs_url="/docs",
        openapi_url="/docs.json",
    )
    app.add_exception_handler(CustomHTTPException, unhandled_custom_exception_handler)
    app = apply_middleware(app)
    app = apply_routes(app)

    return app
