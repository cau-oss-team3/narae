from fastapi import FastAPI

from app.feats.auth.router import router as auth_router
from app.feats.debug.router import router as debug_router
from app.feats.healthcheck.router import router as healthcheck_router
from app.feats.item.router import router as item_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Register all routers to the FastAPI app.
    """

    app.include_router(auth_router)
    app.include_router(healthcheck_router)
    app.include_router(item_router)  # NOTE: For demonstration
    app.include_router(debug_router)  # NOTE: For simple gpt api testing

    return app
