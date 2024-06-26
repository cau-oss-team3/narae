from fastapi import FastAPI

from app.feats.auth.router import router as auth_router
from app.feats.debug.router import router as debug_router
from app.feats.healthcheck.router import router as healthcheck_router
from app.feats.item.router import router as item_router
from app.feats.mentors.router2 import router as mentors_router2
from app.feats.prompt.router import router as prompt_router
from app.feats.chat.router import router as chat_router
from app.feats.feedback.router import router as feedback_router
from app.feats.moderation.router import router as moderation_router
from app.feats.embedding.router import router as embedding_router


def apply_routes(app: FastAPI) -> FastAPI:
    """
    Register all routers to the FastAPI app.
    """

    app.include_router(auth_router)
    app.include_router(mentors_router2)
    app.include_router(prompt_router)
    app.include_router(chat_router)
    app.include_router(feedback_router)
    app.include_router(moderation_router)
    app.include_router(healthcheck_router)
    app.include_router(embedding_router)

    # app.include_router(item_router)  # NOTE: For demonstration
    # app.include_router(debug_router)  # NOTE: For simple gpt api testing

    return app
