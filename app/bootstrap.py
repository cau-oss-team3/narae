from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.settings import settings
from app.core.logger import set_logging
from app.middleware import apply_middleware
from app.routers import apply_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    set_logging(settings.base_dir)

    yield
    # Clean up code here


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